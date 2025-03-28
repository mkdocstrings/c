# This module implements a handler for the C language.

from __future__ import annotations

import re
from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Protocol

from mkdocs.exceptions import PluginError
from mkdocstrings import BaseHandler, CollectionError, CollectorItem, get_logger
from pycparser import CParser, c_ast

from mkdocstrings_handlers.c._internal.config import COptions

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping

    from mkdocs.config.defaults import MkDocsConfig
    from pycparser.c_ast import FileAST


_logger = get_logger(__name__)


@dataclass
class Comment:
    """A comment extracted from the source code."""

    text: str
    """The text of the comment."""
    last_line_number: int
    """The last line number of the comment in the source code."""


@dataclass
class Macro:
    """A macro extracted from the source code."""

    text: str
    """The text of the macro."""
    line_number: int
    """The line number of the macro in the source code."""


_C_PARSER = CParser()
_END_COMMENT = re.compile(r'^(?!").+; *((\/\/.*)|(\/\*.*\*\/))$')
_END_COMMENT_MACRO = re.compile(r"#.+ *((\/\/.*)|(\/\*.*\*\/))$")
_SINGLE_COMMENT = re.compile(r" *\/\/ ?(.*)")
_SINGLE_COMMENT_ALT = re.compile(r"\/\* *(.+) *\*\/")
_FULL_DOC = re.compile(r"\/\*!?\n((.|\n)+)\n *\*\/")
_DESC = re.compile(r" *\* *(.+)")
_DIRECTIVE = re.compile(r" *\* *@(\w+)(\[.+\])? *(.+)")
_PARAM_BODY = re.compile(r"(\w+) *(.+)")
_DEFINE = re.compile(r"# *define (\w+) *(\w*)")


def extract_comments(code: str) -> tuple[list[Comment], str]:
    """Extract comments from the source code.

    Parameters:
        code: The source code to extract comments from.

    Returns:
        A tuple containing a list of comments and the source code with comments removed.
    """
    comments: list[Comment] = []
    extracted: list[str] = []
    in_comment: bool = False
    buffer = StringIO()

    for index, line in enumerate(code.split("\n")):
        content = line.lstrip(" ").rstrip(" ")
        if content.startswith("//") or (content.startswith("/*") and content.endswith("*/")):
            # single line comment
            comments.append(Comment(content, index + 1))
            extracted.append("")  # preserve line count
        elif match := _END_COMMENT_MACRO.match(line):
            # comment at end of preprocessor directive
            comments.append(Comment(match.group(2), index + 1))
            extracted.append(line[: match.start(2)])
            continue
        elif match := _END_COMMENT.match(line):
            # comment at end of line
            comments.append(Comment(match.group(1), index + 1))
            extracted.append(line[: match.start(1)])
            continue
        elif content.startswith("/*"):
            # start of multiline comment
            in_comment = True
            buffer.write(content + "\n")
        elif content.endswith("*/"):
            # end of multiline comment
            if not in_comment:
                raise CollectionError("Found close to multiline comment without a start!")

            in_comment = False
            buffer.write(line)
            bufval = buffer.getvalue()
            comments.append(Comment(bufval, index + 1))
            buffer.truncate(0)

            for _ in range(bufval.count("\n") + 1):
                extracted.append("")  # preserve line count
        elif in_comment:
            # we want to preserve the indentation
            # here, so use line instead of content
            buffer.write(line + "\n")
        else:
            # not a comment
            extracted.append(line)

    if in_comment:
        raise CollectionError("Unterminated comment!")

    return comments, "\n".join(extracted)


def extract_macros(code: str) -> tuple[list[Macro], str]:
    """Extract macros from the source code.

    Parameters:
        code: The source code to extract macros from.

    Returns:
        A tuple containing a list of macros and the source code with macros removed.
    """
    extracted: list[str] = []
    macros: list[Macro] = []

    # buffer variables
    next_is_macro: bool = False
    buffer = StringIO()
    start_line = -1

    for index, line in enumerate(code.split("\n")):
        content = line.lstrip(" ").rstrip(" ")

        if (not content.startswith("#")) and (not next_is_macro):
            extracted.append(line)
            continue

        extracted.append("")

        if next_is_macro:
            next_is_macro = False
            buffer.write("\n" + content)

        if content.endswith("\\"):
            if not next_is_macro:
                # start of macro
                start_line = index + 1
                buffer.write(content)

            next_is_macro = True

        bufval = buffer.getvalue()
        if (not next_is_macro) and (bufval):
            # multiline macro has ended
            macros.append(Macro(bufval, start_line))
            start_line = -1
            buffer.truncate(0)
        else:
            # single line macro
            macros.append(Macro(content, index + 1))

    return macros, "\n".join(extracted)


class InOut(str, Enum):
    """Enumeration for parameter direction."""

    UNSPECIFIED = "unspecified"
    """The direction is unspecified."""
    IN = "in"
    """The parameter is an input."""
    OUT = "out"
    """The parameter is an output."""


@dataclass
class Param:
    """A parameter in a function signature."""

    name: str
    """The name of the parameter."""
    desc: str
    """The description of the parameter."""
    in_out: InOut
    """The direction of the parameter (input, output, or unspecified)."""


@dataclass
class Docstring:
    """A parsed docstring."""

    desc: str
    """The description of the docstring."""
    params: list[Param] | None = None
    """The parameters of the docstring."""
    ret: str | None = None
    """The return value of the docstring."""


def parse_docstring(content: str) -> Docstring:
    """Parse a docstring.

    Parameters:
        content: The content of the docstring.

    Returns:
        A parsed docstring.
    """
    single = _SINGLE_COMMENT.match(content)

    if single:
        return Docstring(single.group(1))

    single_alt = _SINGLE_COMMENT_ALT.match(content)
    if single_alt:
        return Docstring(single_alt.group(1))

    full = _FULL_DOC.match(content)
    if not full:
        raise CollectionError(f"Could not parse docstring! {content}")

    text = full.group(1)
    desc = StringIO()
    split = text.split("\n")
    start_index = -1
    params: list[Param] = []
    returns: str | None = None

    for index, i in enumerate(split):
        if "@" in i:
            start_index = index
            break

        match = _DESC.match(i)
        if not match:
            raise CollectionError(f"Invalid docstring syntax: {i}")

        desc.write(match.group(1) + " ")

    for directive in split[start_index:]:
        match = _DIRECTIVE.match(directive)

        if not match:
            raise CollectionError(f"Invalid docstring syntax: {directive}")

        name = match.group(1)

        if name == "param":
            in_out_str = match.group(2)

            if in_out_str == "[in]":
                in_out = InOut.IN
            elif in_out_str == "[out]":
                in_out = InOut.OUT
            else:
                in_out = InOut.UNSPECIFIED

            body = _PARAM_BODY.match(match.group(3))

            if not body:
                raise CollectionError(f"Invalid @param body: {body}")

            name = body.group(1)
            param_desc = body.group(2)
            params.append(Param(name, param_desc, in_out))
        elif name in {"return", "returns"}:
            if returns:
                raise CollectionError("Multiple @returns found!")
            returns = match.group(3)
        else:
            raise CollectionError(f"Invalid directive in docstring: {name}")

    return Docstring(desc.getvalue(), params, returns)


@dataclass
class DocMacro:
    """A parsed macro."""

    name: str
    """The name of the macro."""
    content: str | None
    """The content of the macro."""
    doc: Docstring | None
    """The docstring of the macro."""


@dataclass
class DocType:
    """A parsed typedef."""

    name: str
    """The name of the typedef."""
    tp: TypeRef
    """The type reference of the typedef."""
    doc: Docstring | None
    """The docstring of the typedef."""
    quals: list[str]
    """The qualifiers of the typedef."""


@dataclass
class DocGlobalVar:
    """A parsed global variable."""

    name: str
    """The name of the global variable."""
    tp: TypeRef
    """The type reference of the global variable."""
    doc: Docstring | None
    """The docstring of the global variable."""
    quals: list[str]
    """The qualifiers of the global variable."""


@dataclass
class FuncParam:
    """A parameter in a function signature."""

    name: str
    """The name of the parameter."""
    tp: TypeRef
    """The type reference of the parameter."""


@dataclass
class DocFunc:
    """A parsed function."""

    name: str
    """The name of the function."""
    args: list[FuncParam]
    """The arguments of the function."""
    ret: TypeRef
    """The return type of the function."""
    doc: Docstring | None
    """The docstring of the function."""


@dataclass
class CodeDoc:
    """A parsed C source file."""

    macros: list[DocMacro]
    """List of macros in the source file."""
    functions: list[DocFunc]
    """"List of functions in the source file."""
    global_vars: list[DocGlobalVar]
    """List of global variables in the source file."""
    typedefs: dict[str, DocType]
    """List of typedefs in the source file."""


class TypeDecl(str, Enum):
    """Enumeration for type declarations."""

    NORMAL = "normal"
    """A normal type declaration."""
    POINTER = "pointer"
    """A pointer type declaration."""
    ARRAY = "array"
    """An array type declaration."""
    FUNCTION = "function"
    """A function type declaration."""


@dataclass
class TypeRef:
    """A reference to a type in C."""

    name: TypeRef | str
    """The name of the type reference."""
    decl: TypeDecl
    """The type declaration of the type reference."""
    quals: list[str]
    """The qualifiers of the type reference."""
    params: list[TypeRef] | None = None  # only in functions
    """The parameters of the type reference."""


class SupportsQualsAndType(Protocol):
    """A protocol for types that can have qualifiers and a type."""

    quals: list[str]
    """The qualifiers of the type."""
    type: SupportsQualsAndType | c_ast.TypeDecl | c_ast.IdentifierType
    """The type of the node."""


def ast_to_decl(node: SupportsQualsAndType, types: dict[str, DocType]) -> TypeRef:
    """Convert a pycparser AST node to a TypeRef."""
    if isinstance(node, c_ast.TypeDecl):
        # assert isinstance(node.type, c_ast.IdentifierType)
        name = node.type.names[0]
        existing = types.get(name)

        if existing:
            return existing.tp

        return TypeRef(name, TypeDecl.NORMAL, node.quals)

    if isinstance(node, c_ast.PtrDecl):
        # assert not isinstance(node.type, c_ast.IdentifierType)
        return TypeRef(ast_to_decl(node.type, types), TypeDecl.POINTER, node.quals)

    if isinstance(node, c_ast.ArrayDecl):
        return TypeRef(ast_to_decl(node.type, types), TypeDecl.ARRAY, node.quals)

    # assert isinstance(node, c_ast.FuncDecl), f"expected a FuncDecl, got {node}"
    return TypeRef(
        ast_to_decl(node.type, types),
        TypeDecl.FUNCTION,
        [],
        [ast_to_decl(decl.type, types) for decl in node.args.params],  # type: ignore[attr-defined]
    )


def _tp_ref_format_char(ref: TypeRef, char: str, qualname: str) -> str:
    # assert isinstance(ref.name, TypeRef)
    content = tp_ref_to_str(ref.name, qualname)  # type: ignore[arg-type]
    if ref.quals:
        return f"({' '.join(ref.quals)} {content}{char})"
    return f"{content}{char}"


def tp_ref_to_str(ref: TypeRef, qualname: str) -> str:
    """Convert a TypeRef to a string.

    Parameters:
        ref: The TypeRef to convert.
        qualname: The name of the type.

    Returns:
        The string representation of the TypeRef.
    """
    if ref.decl == TypeDecl.NORMAL:
        if ref.quals:
            return f"{' '.join(ref.quals)} {ref.name}"

        return ref.name  # type: ignore[return-value]

    if ref.decl == TypeDecl.POINTER:
        return _tp_ref_format_char(ref, "*", qualname)

    if ref.decl == TypeDecl.ARRAY:
        return _tp_ref_format_char(ref, "[]", qualname)

    # assert ref.decl == TypeDecl.FUNCTION
    # assert ref.params is not None

    params: list[str] = [tp_ref_to_str(i, qualname) for i in ref.params]  # type: ignore[union-attr]
    ret = tp_ref_to_str(ref.name, qualname) if isinstance(ref.name, TypeRef) else ref.name

    return f"{ret} (*{qualname})({', '.join(params)})"


def typedef_to_str(decl: DocType) -> str:
    """Convert a typedef to a string.

    Parameters:
        decl: The typedef to convert.

    Returns:
        The string representation of the typedef.
    """
    return tp_ref_to_str(decl.tp, decl.name)


def desc(doc: Docstring | None) -> str:
    """Get the description from a docstring.

    Parameters:
        doc: The docstring to get the description from.

    Returns:
        The description.
    """
    if not doc:
        return "No description specified."

    return doc.desc


def lookup_type_html(data: CodeDoc, tp: TypeRef, *, name: str | None = None) -> str:
    """Lookup a type and return an HTML representation.

    Parameters:
        data: The parsed C source file.
        tp: The type to lookup.
        name: The name of the type.

    Returns:
        The HTML representation of the type.
    """
    tp_str = ""

    for type_name, doctype in data.typedefs.items():
        if doctype.tp == tp:
            tp_str = f'<a href="#type-{type_name}">{type_name}</a>'

    return f"<code>{tp_str or tp_ref_to_str(tp, name or 'unknown')}</code>"


class CHandler(BaseHandler):
    """The C handler class."""

    name: ClassVar[str] = "c"
    """The handler's name."""

    domain: ClassVar[str] = "c"
    """The cross-documentation domain/language for this handler."""

    enable_inventory: ClassVar[bool] = False
    """Whether this handler is interested in enabling the creation of the `objects.inv` Sphinx inventory file."""

    fallback_theme: ClassVar[str] = "material"
    """The theme to fallback to."""

    def __init__(self, config: Mapping[str, Any], base_dir: Path, **kwargs: Any) -> None:
        """Initialize the handler.

        Parameters:
            config: The handler configuration.
            base_dir: The base directory of the project.
            **kwargs: Arguments passed to the parent constructor.
        """
        super().__init__(**kwargs)

        self.config = config
        """The handler configuration."""
        self.base_dir = base_dir
        """The base directory of the project."""
        self.global_options = config.get("options", {})
        """The global options for the handler."""

    def get_options(self, local_options: Mapping[str, Any]) -> COptions:
        """Combine configuration options."""
        extra = {**self.global_options.get("extra", {}), **local_options.get("extra", {})}
        options = {**self.global_options, **local_options, "extra": extra}
        try:
            return COptions.from_data(**options)
        except Exception as error:
            raise PluginError(f"Invalid options: {error}") from error

    def collect(self, identifier: str, options: COptions) -> CollectorItem:
        """Collect data given an identifier and selection configuration.

        In the implementation, you typically call a subprocess that returns JSON, and load that JSON again into
        a Python dictionary for example, though the implementation is completely free.

        Parameters:
            identifier: An identifier that was found in a markdown document for which to collect data. For example,
                in Python, it would be 'mkdocstrings.handlers' to collect documentation about the handlers module.
                It can be anything that you can feed to the tool of your choice.
            options: All configuration options for this handler either defined globally in `mkdocs.yml` or
                locally overridden in an identifier block by the user.

        Returns:
            Anything you want, as long as you can feed it to the `render` method.
        """
        if options == {}:
            raise CollectionError("Not loading additional headers during fallback")

        source = Path(identifier).read_text(encoding="utf-8")
        comments_list, source = extract_comments(source)
        macros_list, source = extract_macros(source)
        code: FileAST = _C_PARSER.parse(source)

        comments: dict[int, Comment] = {comment.last_line_number: comment for comment in comments_list}
        types: dict[str, DocType] = {}
        global_vars: list[DocGlobalVar] = []
        funcs: list[DocFunc] = []

        for node in code.ext:
            if not isinstance(node, (c_ast.Typedef, c_ast.Decl)):
                continue

            # assert node.coord, "node.coord is None"
            lineno = node.coord.line

            raw_doc: Comment | None = None
            if lineno in comments:
                raw_doc = comments.pop(lineno)
            elif (lineno - 1) in comments:
                raw_doc = comments.pop(lineno - 1)

            docstring: Docstring | None = None

            if raw_doc:
                docstring = parse_docstring(raw_doc.text)

            if isinstance(node, c_ast.Typedef):
                types[node.name] = DocType(node.name, ast_to_decl(node.type, types), docstring, node.quals)

            elif type(node) is c_ast.Decl:  # we dont want the subclasses
                if isinstance(node.type, c_ast.FuncDecl):
                    ref = ast_to_decl(node.type, types)
                    # assert ref.decl is TypeDecl.FUNCTION, "decl is not TypeDecl.FUNCTION"
                    # assert ref.params is not None, "function typeref does not have parameters"
                    params: list[FuncParam] = []

                    for param_ref, param in zip(ref.params, node.type.args.params):  # type: ignore[arg-type]
                        params.append(FuncParam(param.name, param_ref))

                    funcs.append(DocFunc(node.name, params, ref.name, docstring))  # type: ignore[arg-type]
                else:
                    global_vars.append(
                        DocGlobalVar(
                            node.name,
                            ast_to_decl(node.type, types),
                            docstring,
                            node.quals,
                        ),
                    )

        macros: list[DocMacro] = []

        for macro in macros_list:
            match = _DEFINE.match(macro.text)

            if not match:
                continue

            lineno = macro.line_number

            raw_doc = None

            if lineno in comments:
                raw_doc = comments.pop(lineno)
            elif (lineno - 1) in comments:
                raw_doc = comments.pop(lineno - 1)

            docstring = parse_docstring(raw_doc.text) if raw_doc else None
            macros.append(DocMacro(match.group(1).rstrip(" "), match.group(2) or None, docstring))

        return CodeDoc(macros, funcs, global_vars, types)

    def render(self, data: CodeDoc, options: COptions) -> str:
        """Render a template using provided data and configuration options.

        Parameters:
            data: The data to render that was collected above in `collect()`.
            options: All configuration options for this handler either defined globally in `mkdocs.yml` or
                locally overridden in an identifier block by the user.

        Returns:
            The rendered template as HTML.
        """
        heading_level = options.heading_level
        template = self.env.get_template("header.html.jinja")
        return template.render(
            config=options,
            header=data,
            heading_level=heading_level,
            root=True,
        )

    def update_env(self, config: dict) -> None:  # noqa: ARG002
        """Update the Jinja environment with any custom settings/filters/options for this handler.

        Parameters:
            config: Configuration options for `mkdocs` and `mkdocstrings`, read from `mkdocs.yml`. See the source code
                of [mkdocstrings.MkdocstringsPlugin.on_config][] to see what's in this dictionary.
        """
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.keep_trailing_newline = False
        self.env.filters["typedef_to_str"] = typedef_to_str
        self.env.filters["lookup_type_html"] = lookup_type_html
        self.env.filters["zip"] = zip


def get_handler(
    handler_config: MutableMapping[str, Any],
    tool_config: MkDocsConfig,
    **kwargs: Any,
) -> CHandler:
    """Simply return an instance of `CHandler`.

    Arguments:
        handler_config: The handler configuration.
        tool_config: The tool (SSG) configuration.

    Returns:
        An instance of `CHandler`.
    """
    base_dir = Path(tool_config.config_file_path or "./mkdocs.yml").parent
    return CHandler(config=handler_config, base_dir=base_dir, **kwargs)
