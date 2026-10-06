# c

C handler for mkdocstrings.

Classes:

- **`CConfig`** – C handler configuration.
- **`CHandler`** – The C handler class.
- **`CInputConfig`** – C handler configuration.
- **`CInputOptions`** – Accepted input options.
- **`COptions`** – Final options passed as template context.
- **`CodeDoc`** – A parsed C source file.
- **`Comment`** – A comment extracted from the source code.
- **`DocFunc`** – A parsed function.
- **`DocGlobalVar`** – A parsed global variable.
- **`DocMacro`** – A parsed macro.
- **`DocType`** – A parsed typedef.
- **`Docstring`** – A parsed docstring.
- **`FuncParam`** – A parameter in a function signature.
- **`InOut`** – Enumeration for parameter direction.
- **`Macro`** – A macro extracted from the source code.
- **`Param`** – A parameter in a function signature.
- **`SupportsQualsAndType`** – A protocol for types that can have qualifiers and a type.
- **`TypeDecl`** – Enumeration for type declarations.
- **`TypeRef`** – A reference to a type in C.

Functions:

- **`ast_to_decl`** – Convert a pycparser AST node to a TypeRef.
- **`desc`** – Get the description from a docstring.
- **`extract_comments`** – Extract comments from the source code.
- **`extract_macros`** – Extract macros from the source code.
- **`get_handler`** – Simply return an instance of CHandler.
- **`lookup_type_html`** – Lookup a type and return an HTML representation.
- **`parse_docstring`** – Parse a docstring.
- **`tp_ref_to_str`** – Convert a TypeRef to a string.
- **`typedef_to_str`** – Convert a typedef to a string.

## CConfig

```
CConfig(*, options: dict[str, Any] = dict())
```

Bases: `CInputConfig`

C handler configuration.

Methods:

- **`coerce`** – Coerce data.
- **`from_data`** – Create an instance from a dictionary.

Attributes:

- **`options`** (`dict[str, Any]`) – Global options in mkdocs.yml.

### options

```
options: dict[str, Any] = field(default_factory=dict)
```

Global options in mkdocs.yml.

### coerce

```
coerce(**data: Any) -> MutableMapping[str, Any]
```

Coerce data.

Source code in `src/mkdocstrings_handlers/c/_internal/config.py`

```
@classmethod
def coerce(cls, **data: Any) -> MutableMapping[str, Any]:
    """Coerce data."""
    return super().coerce(**data)
```

### from_data

```
from_data(**data: Any) -> Self
```

Create an instance from a dictionary.

Source code in `src/mkdocstrings_handlers/c/_internal/config.py`

```
@classmethod
def from_data(cls, **data: Any) -> Self:
    """Create an instance from a dictionary."""
    return cls(**cls.coerce(**data))
```

## CHandler

```
CHandler(
    config: Mapping[str, Any], base_dir: Path, **kwargs: Any
)
```

Bases: `BaseHandler`

The C handler class.

Parameters:

- **`config`** (`Mapping[str, Any]`) – The handler configuration.
- **`base_dir`** (`Path`) – The base directory of the project.
- **`**kwargs`** (`Any`, default: `{}` ) – Arguments passed to the parent constructor.

Methods:

- **`collect`** – Collect data given an identifier and selection configuration.
- **`do_convert_markdown`** – Render Markdown text; for use inside templates.
- **`do_heading`** – Render an HTML heading and register it for the table of contents. For use inside templates.
- **`get_aliases`** – Return the possible aliases for a given identifier.
- **`get_extended_templates_dirs`** – Load template extensions for the given handler, return their templates directories.
- **`get_headings`** – Return and clear the headings gathered so far.
- **`get_inventory_urls`** – Return the URLs (and configuration options) of the inventory files to download.
- **`get_options`** – Combine configuration options.
- **`get_templates_dir`** – Return the path to the handler's templates directory.
- **`load_inventory`** – Yield items and their URLs from an inventory file streamed from in_file.
- **`render`** – Render a template using provided data and configuration options.
- **`render_backlinks`** – Render backlinks.
- **`teardown`** – Teardown the handler.
- **`update_env`** – Update the Jinja environment with any custom settings/filters/options for this handler.

Attributes:

- **`base_dir`** – The base directory of the project.
- **`config`** – The handler configuration.
- **`custom_templates`** – The path to custom templates.
- **`domain`** (`str`) – The cross-documentation domain/language for this handler.
- **`enable_inventory`** (`bool`) – Whether this handler is interested in enabling the creation of the objects.inv Sphinx inventory file.
- **`env`** – The Jinja environment.
- **`extra_css`** (`str`) – Extra CSS.
- **`fallback_theme`** (`str`) – The theme to fallback to.
- **`global_options`** – The global options for the handler.
- **`md`** (`Markdown`) – The Markdown instance.
- **`mdx`** – The Markdown extensions to use.
- **`mdx_config`** – The configuration for the Markdown extensions.
- **`name`** (`str`) – The handler's name.
- **`outer_layer`** (`bool`) – Whether we're in the outer Markdown conversion layer.
- **`theme`** – The selected theme.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
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
```

### base_dir

```
base_dir = base_dir
```

The base directory of the project.

### config

```
config = config
```

The handler configuration.

### custom_templates

```
custom_templates = custom_templates
```

The path to custom templates.

### domain

```
domain: str = 'c'
```

The cross-documentation domain/language for this handler.

### enable_inventory

```
enable_inventory: bool = False
```

Whether this handler is interested in enabling the creation of the `objects.inv` Sphinx inventory file.

### env

```
env = Environment(
    autoescape=True,
    loader=FileSystemLoader(paths),
    auto_reload=False,
)
```

The Jinja environment.

### extra_css

```
extra_css: str = ''
```

Extra CSS.

### fallback_theme

```
fallback_theme: str = 'material'
```

The theme to fallback to.

### global_options

```
global_options = config.get('options', {})
```

The global options for the handler.

### md

```
md: Markdown
```

The Markdown instance.

Raises:

- `RuntimeError` – When the Markdown instance is not set yet.

### mdx

```
mdx = mdx
```

The Markdown extensions to use.

### mdx_config

```
mdx_config = mdx_config
```

The configuration for the Markdown extensions.

### name

```
name: str = 'c'
```

The handler's name.

### outer_layer

```
outer_layer: bool
```

Whether we're in the outer Markdown conversion layer.

### theme

```
theme = theme
```

The selected theme.

### collect

```
collect(
    identifier: str, options: COptions
) -> CollectorItem
```

Collect data given an identifier and selection configuration.

In the implementation, you typically call a subprocess that returns JSON, and load that JSON again into a Python dictionary for example, though the implementation is completely free.

Parameters:

- **`identifier`** (`str`) – An identifier that was found in a markdown document for which to collect data. For example, in Python, it would be 'mkdocstrings.handlers' to collect documentation about the handlers module. It can be anything that you can feed to the tool of your choice.
- **`options`** (`COptions`) – All configuration options for this handler either defined globally in mkdocs.yml or locally overridden in an identifier block by the user.

Returns:

- `CollectorItem` – Anything you want, as long as you can feed it to the render method.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
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

                for param_ref, param in zip(ref.params, node.type.args.params, strict=False):  # type: ignore[arg-type]
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
```

### do_convert_markdown

```
do_convert_markdown(
    text: str,
    heading_level: int,
    html_id: str = "",
    *,
    strip_paragraph: bool = False,
    autoref_hook: AutorefsHookInterface | None = None,
) -> Markup
```

Render Markdown text; for use inside templates.

Parameters:

- **`text`** (`str`) – The text to convert.
- **`heading_level`** (`int`) – The base heading level to start all Markdown headings from.
- **`html_id`** (`str`, default: `''` ) – The HTML id of the element that's considered the parent of this element.
- **`strip_paragraph`** (`bool`, default: `False` ) – Whether to exclude the <p> tag from around the whole output.

Returns:

- `Markup` – An HTML string.

Source code in `mkdocstrings/_internal/handlers/base.py`

```
def do_convert_markdown(
    self,
    text: str,
    heading_level: int,
    html_id: str = "",
    *,
    strip_paragraph: bool = False,
    autoref_hook: AutorefsHookInterface | None = None,
) -> Markup:
    """Render Markdown text; for use inside templates.

    Arguments:
        text: The text to convert.
        heading_level: The base heading level to start all Markdown headings from.
        html_id: The HTML id of the element that's considered the parent of this element.
        strip_paragraph: Whether to exclude the `<p>` tag from around the whole output.

    Returns:
        An HTML string.
    """
    global _markdown_conversion_layer  # noqa: PLW0603
    _markdown_conversion_layer += 1
    treeprocessors = self.md.treeprocessors
    treeprocessors[HeadingShiftingTreeprocessor.name].shift_by = heading_level
    treeprocessors[IdPrependingTreeprocessor.name].id_prefix = html_id and html_id + "--"
    treeprocessors[ParagraphStrippingTreeprocessor.name].strip = strip_paragraph
    if BacklinksTreeProcessor.name in treeprocessors:
        treeprocessors[BacklinksTreeProcessor.name].initial_id = html_id
    if autoref_hook and AutorefsInlineProcessor.name in self.md.inlinePatterns:
        self.md.inlinePatterns[AutorefsInlineProcessor.name].hook = autoref_hook  # ty: ignore[unresolved-attribute]

    try:
        return Markup(self.md.convert(text))
    finally:
        treeprocessors[HeadingShiftingTreeprocessor.name].shift_by = 0
        treeprocessors[IdPrependingTreeprocessor.name].id_prefix = ""
        treeprocessors[ParagraphStrippingTreeprocessor.name].strip = False
        if BacklinksTreeProcessor.name in treeprocessors:
            treeprocessors[BacklinksTreeProcessor.name].initial_id = None
        if AutorefsInlineProcessor.name in self.md.inlinePatterns:
            self.md.inlinePatterns[AutorefsInlineProcessor.name].hook = None  # ty: ignore[unresolved-attribute]
        self.md.reset()
        _markdown_conversion_layer -= 1
```

### do_heading

```
do_heading(
    content: Markup,
    heading_level: int,
    *,
    role: str | None = None,
    hidden: bool = False,
    toc_label: str | None = None,
    skip_inventory: bool = False,
    **attributes: str,
) -> Markup
```

Render an HTML heading and register it for the table of contents. For use inside templates.

Parameters:

- **`content`** (`Markup`) – The HTML within the heading.
- **`heading_level`** (`int`) – The level of heading (e.g. 3 -> h3).
- **`role`** (`str | None`, default: `None` ) – An optional role for the object bound to this heading.
- **`hidden`** (`bool`, default: `False` ) – If True, only register it for the table of contents, don't render anything.
- **`toc_label`** (`str | None`, default: `None` ) – The title to use in the table of contents ('data-toc-label' attribute).
- **`skip_inventory`** (`bool`, default: `False` ) – Flag element to not be registered in the inventory (by setting a data-skip-inventory attribute).
- **`**attributes`** (`str`, default: `{}` ) – Any extra HTML attributes of the heading.

Returns:

- `Markup` – An HTML string.

Source code in `mkdocstrings/_internal/handlers/base.py`

```
def do_heading(
    self,
    content: Markup,
    heading_level: int,
    *,
    role: str | None = None,
    hidden: bool = False,
    toc_label: str | None = None,
    skip_inventory: bool = False,
    **attributes: str,
) -> Markup:
    """Render an HTML heading and register it for the table of contents. For use inside templates.

    Arguments:
        content: The HTML within the heading.
        heading_level: The level of heading (e.g. 3 -> `h3`).
        role: An optional role for the object bound to this heading.
        hidden: If True, only register it for the table of contents, don't render anything.
        toc_label: The title to use in the table of contents ('data-toc-label' attribute).
        skip_inventory: Flag element to not be registered in the inventory (by setting a `data-skip-inventory` attribute).
        **attributes: Any extra HTML attributes of the heading.

    Returns:
        An HTML string.
    """
    # Produce a heading element that will be used later, in `AutoDocProcessor.run`, to:
    # - register it in the ToC: right now we're in the inner Markdown conversion layer,
    #   so we have to bubble up the information to the outer Markdown conversion layer,
    #   for the ToC extension to pick it up.
    # - register it in autorefs: right now we don't know what page is being rendered,
    #   so we bubble up the information again to where autorefs knows the page,
    #   and can correctly register the heading anchor (id) to its full URL.
    # - register it in the objects inventory: same as for autorefs,
    #   we don't know the page here, or the handler (and its domain),
    #   so we bubble up the information to where the mkdocstrings extension knows that.
    el = Element(f"h{heading_level}", attributes)
    if toc_label is None:
        toc_label = content.unescape() if isinstance(content, Markup) else content
    el.set("data-toc-label", toc_label)
    if skip_inventory:
        el.set("data-skip-inventory", "true")
    if role:
        el.set("data-role", role)
    if content:
        el.text = str(content).strip()
    self._headings.append(el)

    if hidden:
        return Markup('<a id="{0}"></a>').format(attributes["id"])

    # Now produce the actual HTML to be rendered. The goal is to wrap the HTML content into a heading.
    # Start with a heading that has just attributes (no text), and add a placeholder into it.
    el = Element(f"h{heading_level}", attributes)
    el.append(Element("mkdocstrings-placeholder"))
    # Tell the inner 'toc' extension to make its additions if configured so.
    toc = cast("TocTreeprocessor", self.md.treeprocessors["toc"])
    if toc.use_anchors:
        toc.add_anchor(el, attributes["id"])
    if toc.use_permalinks:
        toc.add_permalink(el, attributes["id"])

    # The content we received is HTML, so it can't just be inserted into the tree. We had marked the middle
    # of the heading with a placeholder that can never occur (text can't directly contain angle brackets).
    # Now this HTML wrapper can be "filled" by replacing the placeholder.
    html_with_placeholder = tostring(el, encoding="unicode")
    assert (  # noqa: S101
        html_with_placeholder.count("<mkdocstrings-placeholder />") == 1
    ), f"Bug in mkdocstrings: failed to replace in {html_with_placeholder!r}"
    html = html_with_placeholder.replace("<mkdocstrings-placeholder />", content)
    return Markup(html)
```

### get_aliases

```
get_aliases(identifier: str) -> tuple[str, ...]
```

Return the possible aliases for a given identifier.

Parameters:

- **`identifier`** (`str`) – The identifier to get the aliases of.

Returns:

- `tuple[str, ...]` – A tuple of strings - aliases.

Source code in `mkdocstrings/_internal/handlers/base.py`

```
def get_aliases(self, identifier: str) -> tuple[str, ...]:  # noqa: ARG002
    """Return the possible aliases for a given identifier.

    Arguments:
        identifier: The identifier to get the aliases of.

    Returns:
        A tuple of strings - aliases.
    """
    return ()
```

### get_extended_templates_dirs

```
get_extended_templates_dirs(handler: str) -> list[Path]
```

Load template extensions for the given handler, return their templates directories.

Parameters:

- **`handler`** (`str`) – The name of the handler to get the extended templates directory of.

Returns:

- `list[Path]` – The extensions templates directories.

Source code in `mkdocstrings/_internal/handlers/base.py`

```
def get_extended_templates_dirs(self, handler: str) -> list[Path]:
    """Load template extensions for the given handler, return their templates directories.

    Arguments:
        handler: The name of the handler to get the extended templates directory of.

    Returns:
        The extensions templates directories.
    """
    discovered_extensions = entry_points(group=f"mkdocstrings.{handler}.templates")
    return [extension.load()() for extension in discovered_extensions]
```

### get_headings

```
get_headings() -> Sequence[Element]
```

Return and clear the headings gathered so far.

Returns:

- `Sequence[Element]` – A list of HTML elements.

Source code in `mkdocstrings/_internal/handlers/base.py`

```
def get_headings(self) -> Sequence[Element]:
    """Return and clear the headings gathered so far.

    Returns:
        A list of HTML elements.
    """
    result = list(self._headings)
    self._headings.clear()
    return result
```

### get_inventory_urls

```
get_inventory_urls() -> list[tuple[str, dict[str, Any]]]
```

Return the URLs (and configuration options) of the inventory files to download.

Source code in `mkdocstrings/_internal/handlers/base.py`

```
def get_inventory_urls(self) -> list[tuple[str, dict[str, Any]]]:
    """Return the URLs (and configuration options) of the inventory files to download."""
    return []
```

### get_options

```
get_options(local_options: Mapping[str, Any]) -> COptions
```

Combine configuration options.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
def get_options(self, local_options: Mapping[str, Any]) -> COptions:
    """Combine configuration options."""
    extra = {**self.global_options.get("extra", {}), **local_options.get("extra", {})}
    options = {**self.global_options, **local_options, "extra": extra}
    try:
        return COptions.from_data(**options)
    except Exception as error:
        raise PluginError(f"Invalid options: {error}") from error
```

### get_templates_dir

```
get_templates_dir(handler: str | None = None) -> Path
```

Return the path to the handler's templates directory.

Override to customize how the templates directory is found.

Parameters:

- **`handler`** (`str | None`, default: `None` ) – The name of the handler to get the templates directory of.

Raises:

- `ModuleNotFoundError` – When no such handler is installed.
- `FileNotFoundError` – When the templates directory cannot be found.

Returns:

- `Path` – The templates directory path.

Source code in `mkdocstrings/_internal/handlers/base.py`

```
def get_templates_dir(self, handler: str | None = None) -> Path:
    """Return the path to the handler's templates directory.

    Override to customize how the templates directory is found.

    Arguments:
        handler: The name of the handler to get the templates directory of.

    Raises:
        ModuleNotFoundError: When no such handler is installed.
        FileNotFoundError: When the templates directory cannot be found.

    Returns:
        The templates directory path.
    """
    handler = handler or self.name
    try:
        import mkdocstrings_handlers  # noqa: PLC0415
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError(f"Handler '{handler}' not found, is it installed?") from error

    for path in mkdocstrings_handlers.__path__:
        theme_path = Path(path, handler, "templates")
        if theme_path.exists():
            return theme_path

    raise FileNotFoundError(f"Can't find 'templates' folder for handler '{handler}'")
```

### load_inventory

```
load_inventory(
    in_file: BinaryIO,
    url: str,
    base_url: str | None = None,
    **kwargs: Any,
) -> Iterator[tuple[str, str]]
```

Yield items and their URLs from an inventory file streamed from `in_file`.

Parameters:

- **`in_file`** (`BinaryIO`) – The binary file-like object to read the inventory from.
- **`url`** (`str`) – The URL that this file is being streamed from (used to guess base_url).
- **`base_url`** (`str | None`, default: `None` ) – The URL that this inventory's sub-paths are relative to.
- **`**kwargs`** (`Any`, default: `{}` ) – Ignore additional arguments passed from the config.

Yields:

- `tuple[str, str]` – Tuples of (item identifier, item URL).

Source code in `mkdocstrings/_internal/handlers/base.py`

```
@classmethod
def load_inventory(
    cls,
    in_file: BinaryIO,  # noqa: ARG003
    url: str,  # noqa: ARG003
    base_url: str | None = None,  # noqa: ARG003
    **kwargs: Any,  # noqa: ARG003
) -> Iterator[tuple[str, str]]:
    """Yield items and their URLs from an inventory file streamed from `in_file`.

    Arguments:
        in_file: The binary file-like object to read the inventory from.
        url: The URL that this file is being streamed from (used to guess `base_url`).
        base_url: The URL that this inventory's sub-paths are relative to.
        **kwargs: Ignore additional arguments passed from the config.

    Yields:
        Tuples of (item identifier, item URL).
    """
    yield from ()
```

### render

```
render(data: CodeDoc, options: COptions) -> str
```

Render a template using provided data and configuration options.

Parameters:

- **`data`** (`CodeDoc`) – The data to render that was collected above in collect().
- **`options`** (`COptions`) – All configuration options for this handler either defined globally in mkdocs.yml or locally overridden in an identifier block by the user.

Returns:

- `str` – The rendered template as HTML.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
def render(self, data: CodeDoc, options: COptions) -> str:  # type: ignore[override]
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
```

### render_backlinks

```
render_backlinks(
    backlinks: Mapping[str, Iterable[Backlink]],
    *,
    locale: str | None = None,
) -> str
```

Render backlinks.

Parameters:

- **`backlinks`** (`Mapping[str, Iterable[Backlink]]`) – A mapping of identifiers to backlinks.
- **`locale`** (`str | None`, default: `None` ) – The locale to use for translations, if any.

Returns:

- `str` – The rendered backlinks as HTML.

Source code in `mkdocstrings/_internal/handlers/base.py`

```
def render_backlinks(self, backlinks: Mapping[str, Iterable[Backlink]], *, locale: str | None = None) -> str:  # noqa: ARG002
    """Render backlinks.

    Parameters:
        backlinks: A mapping of identifiers to backlinks.
        locale: The locale to use for translations, if any.

    Returns:
        The rendered backlinks as HTML.
    """
    return ""
```

### teardown

```
teardown() -> None
```

Teardown the handler.

This method should be implemented to, for example, terminate a subprocess that was started when creating the handler instance.

Source code in `mkdocstrings/_internal/handlers/base.py`

```
def teardown(self) -> None:
    """Teardown the handler.

    This method should be implemented to, for example, terminate a subprocess
    that was started when creating the handler instance.
    """
```

### update_env

```
update_env(config: dict) -> None
```

Update the Jinja environment with any custom settings/filters/options for this handler.

Parameters:

- **`config`** (`dict`) – Configuration options for mkdocs and mkdocstrings, read from mkdocs.yml. See the source code of mkdocstrings.MkdocstringsPlugin.on_config to see what's in this dictionary.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
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
```

## CInputConfig

```
CInputConfig(
    *,
    options: Annotated[
        CInputOptions,
        _Field(
            description="Configuration options for collecting and rendering objects."
        ),
    ] = CInputOptions(),
)
```

C handler configuration.

Methods:

- **`coerce`** – Coerce data.
- **`from_data`** – Create an instance from a dictionary.

Attributes:

- **`options`** (`Annotated[CInputOptions, _Field(description='Configuration options for collecting and rendering objects.')]`) – Configuration options for collecting and rendering objects.

### options

```
options: Annotated[
    CInputOptions,
    _Field(
        description="Configuration options for collecting and rendering objects."
    ),
] = field(default_factory=CInputOptions)
```

Configuration options for collecting and rendering objects.

### coerce

```
coerce(**data: Any) -> MutableMapping[str, Any]
```

Coerce data.

Source code in `src/mkdocstrings_handlers/c/_internal/config.py`

```
@classmethod
def coerce(cls, **data: Any) -> MutableMapping[str, Any]:
    """Coerce data."""
    return data
```

### from_data

```
from_data(**data: Any) -> Self
```

Create an instance from a dictionary.

Source code in `src/mkdocstrings_handlers/c/_internal/config.py`

```
@classmethod
def from_data(cls, **data: Any) -> Self:
    """Create an instance from a dictionary."""
    return cls(**cls.coerce(**data))
```

## CInputOptions

```
CInputOptions(
    *,
    extra: Annotated[
        dict[str, Any],
        _Field(
            group="general", description="Extra options."
        ),
    ] = dict(),
    heading: Annotated[
        str,
        _Field(
            group="headings",
            description="A custom string to override the autogenerated heading of the root object.",
        ),
    ] = "",
    heading_level: Annotated[
        int,
        _Field(
            group="headings",
            description="The initial heading level to use.",
        ),
    ] = 2,
    show_symbol_type_heading: Annotated[
        bool,
        _Field(
            group="headings",
            description="Show the symbol type in headings (e.g. mod, class, meth, func and attr).",
        ),
    ] = False,
    show_symbol_type_toc: Annotated[
        bool,
        _Field(
            group="headings",
            description="Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).",
        ),
    ] = False,
    toc_label: Annotated[
        str,
        _Field(
            group="headings",
            description="A custom string to override the autogenerated toc label of the root object.",
        ),
    ] = "",
)
```

Accepted input options.

Methods:

- **`coerce`** – Coerce data.
- **`from_data`** – Create an instance from a dictionary.

Attributes:

- **`extra`** (`Annotated[dict[str, Any], _Field(group='general', description='Extra options.')]`) – Extra options.
- **`heading`** (`Annotated[str, _Field(group='headings', description='A custom string to override the autogenerated heading of the root object.')]`) – A custom string to override the autogenerated heading of the root object.
- **`heading_level`** (`Annotated[int, _Field(group='headings', description='The initial heading level to use.')]`) – The initial heading level to use.
- **`show_symbol_type_heading`** (`Annotated[bool, _Field(group='headings', description='Show the symbol type in headings (e.g. mod, class, meth, func and attr).')]`) – Show the symbol type in headings (e.g. mod, class, meth, func and attr).
- **`show_symbol_type_toc`** (`Annotated[bool, _Field(group='headings', description='Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).')]`) – Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).
- **`toc_label`** (`Annotated[str, _Field(group='headings', description='A custom string to override the autogenerated toc label of the root object.')]`) – A custom string to override the autogenerated toc label of the root object.

### extra

```
extra: Annotated[
    dict[str, Any],
    _Field(group="general", description="Extra options."),
] = field(default_factory=dict)
```

Extra options.

### heading

```
heading: Annotated[
    str,
    _Field(
        group="headings",
        description="A custom string to override the autogenerated heading of the root object.",
    ),
] = ""
```

A custom string to override the autogenerated heading of the root object.

### heading_level

```
heading_level: Annotated[
    int,
    _Field(
        group="headings",
        description="The initial heading level to use.",
    ),
] = 2
```

The initial heading level to use.

### show_symbol_type_heading

```
show_symbol_type_heading: Annotated[
    bool,
    _Field(
        group="headings",
        description="Show the symbol type in headings (e.g. mod, class, meth, func and attr).",
    ),
] = False
```

Show the symbol type in headings (e.g. mod, class, meth, func and attr).

### show_symbol_type_toc

```
show_symbol_type_toc: Annotated[
    bool,
    _Field(
        group="headings",
        description="Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).",
    ),
] = False
```

Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).

### toc_label

```
toc_label: Annotated[
    str,
    _Field(
        group="headings",
        description="A custom string to override the autogenerated toc label of the root object.",
    ),
] = ""
```

A custom string to override the autogenerated toc label of the root object.

### coerce

```
coerce(**data: Any) -> MutableMapping[str, Any]
```

Coerce data.

Source code in `src/mkdocstrings_handlers/c/_internal/config.py`

```
@classmethod
def coerce(cls, **data: Any) -> MutableMapping[str, Any]:
    """Coerce data."""
    return data
```

### from_data

```
from_data(**data: Any) -> Self
```

Create an instance from a dictionary.

Source code in `src/mkdocstrings_handlers/c/_internal/config.py`

```
@classmethod
def from_data(cls, **data: Any) -> Self:
    """Create an instance from a dictionary."""
    return cls(**cls.coerce(**data))
```

## COptions

```
COptions(
    *,
    extra: Annotated[
        dict[str, Any],
        _Field(
            group="general", description="Extra options."
        ),
    ] = dict(),
    heading: Annotated[
        str,
        _Field(
            group="headings",
            description="A custom string to override the autogenerated heading of the root object.",
        ),
    ] = "",
    heading_level: Annotated[
        int,
        _Field(
            group="headings",
            description="The initial heading level to use.",
        ),
    ] = 2,
    show_symbol_type_heading: Annotated[
        bool,
        _Field(
            group="headings",
            description="Show the symbol type in headings (e.g. mod, class, meth, func and attr).",
        ),
    ] = False,
    show_symbol_type_toc: Annotated[
        bool,
        _Field(
            group="headings",
            description="Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).",
        ),
    ] = False,
    toc_label: Annotated[
        str,
        _Field(
            group="headings",
            description="A custom string to override the autogenerated toc label of the root object.",
        ),
    ] = "",
)
```

Bases: `CInputOptions`

Final options passed as template context.

Methods:

- **`coerce`** – Create an instance from a dictionary.
- **`from_data`** – Create an instance from a dictionary.

Attributes:

- **`extra`** (`Annotated[dict[str, Any], _Field(group='general', description='Extra options.')]`) – Extra options.
- **`heading`** (`Annotated[str, _Field(group='headings', description='A custom string to override the autogenerated heading of the root object.')]`) – A custom string to override the autogenerated heading of the root object.
- **`heading_level`** (`Annotated[int, _Field(group='headings', description='The initial heading level to use.')]`) – The initial heading level to use.
- **`show_symbol_type_heading`** (`Annotated[bool, _Field(group='headings', description='Show the symbol type in headings (e.g. mod, class, meth, func and attr).')]`) – Show the symbol type in headings (e.g. mod, class, meth, func and attr).
- **`show_symbol_type_toc`** (`Annotated[bool, _Field(group='headings', description='Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).')]`) – Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).
- **`toc_label`** (`Annotated[str, _Field(group='headings', description='A custom string to override the autogenerated toc label of the root object.')]`) – A custom string to override the autogenerated toc label of the root object.

### extra

```
extra: Annotated[
    dict[str, Any],
    _Field(group="general", description="Extra options."),
] = field(default_factory=dict)
```

Extra options.

### heading

```
heading: Annotated[
    str,
    _Field(
        group="headings",
        description="A custom string to override the autogenerated heading of the root object.",
    ),
] = ""
```

A custom string to override the autogenerated heading of the root object.

### heading_level

```
heading_level: Annotated[
    int,
    _Field(
        group="headings",
        description="The initial heading level to use.",
    ),
] = 2
```

The initial heading level to use.

### show_symbol_type_heading

```
show_symbol_type_heading: Annotated[
    bool,
    _Field(
        group="headings",
        description="Show the symbol type in headings (e.g. mod, class, meth, func and attr).",
    ),
] = False
```

Show the symbol type in headings (e.g. mod, class, meth, func and attr).

### show_symbol_type_toc

```
show_symbol_type_toc: Annotated[
    bool,
    _Field(
        group="headings",
        description="Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).",
    ),
] = False
```

Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).

### toc_label

```
toc_label: Annotated[
    str,
    _Field(
        group="headings",
        description="A custom string to override the autogenerated toc label of the root object.",
    ),
] = ""
```

A custom string to override the autogenerated toc label of the root object.

### coerce

```
coerce(**data: Any) -> MutableMapping[str, Any]
```

Create an instance from a dictionary.

Source code in `src/mkdocstrings_handlers/c/_internal/config.py`

```
@classmethod
def coerce(cls, **data: Any) -> MutableMapping[str, Any]:
    """Create an instance from a dictionary."""
    # Coerce any field into its final form.
    return super().coerce(**data)
```

### from_data

```
from_data(**data: Any) -> Self
```

Create an instance from a dictionary.

Source code in `src/mkdocstrings_handlers/c/_internal/config.py`

```
@classmethod
def from_data(cls, **data: Any) -> Self:
    """Create an instance from a dictionary."""
    return cls(**cls.coerce(**data))
```

## CodeDoc

```
CodeDoc(
    macros: list[DocMacro],
    functions: list[DocFunc],
    global_vars: list[DocGlobalVar],
    typedefs: dict[str, DocType],
)
```

A parsed C source file.

Attributes:

- **`functions`** (`list[DocFunc]`) – "List of functions in the source file.
- **`global_vars`** (`list[DocGlobalVar]`) – List of global variables in the source file.
- **`macros`** (`list[DocMacro]`) – List of macros in the source file.
- **`typedefs`** (`dict[str, DocType]`) – List of typedefs in the source file.

### functions

```
functions: list[DocFunc]
```

"List of functions in the source file.

### global_vars

```
global_vars: list[DocGlobalVar]
```

List of global variables in the source file.

### macros

```
macros: list[DocMacro]
```

List of macros in the source file.

### typedefs

```
typedefs: dict[str, DocType]
```

List of typedefs in the source file.

## Comment

```
Comment(text: str, last_line_number: int)
```

A comment extracted from the source code.

Attributes:

- **`last_line_number`** (`int`) – The last line number of the comment in the source code.
- **`text`** (`str`) – The text of the comment.

### last_line_number

```
last_line_number: int
```

The last line number of the comment in the source code.

### text

```
text: str
```

The text of the comment.

## DocFunc

```
DocFunc(
    name: str,
    args: list[FuncParam],
    ret: TypeRef,
    doc: Docstring | None,
)
```

A parsed function.

Attributes:

- **`args`** (`list[FuncParam]`) – The arguments of the function.
- **`doc`** (`Docstring | None`) – The docstring of the function.
- **`name`** (`str`) – The name of the function.
- **`ret`** (`TypeRef`) – The return type of the function.

### args

```
args: list[FuncParam]
```

The arguments of the function.

### doc

```
doc: Docstring | None
```

The docstring of the function.

### name

```
name: str
```

The name of the function.

### ret

```
ret: TypeRef
```

The return type of the function.

## DocGlobalVar

```
DocGlobalVar(
    name: str,
    tp: TypeRef,
    doc: Docstring | None,
    quals: list[str],
)
```

A parsed global variable.

Attributes:

- **`doc`** (`Docstring | None`) – The docstring of the global variable.
- **`name`** (`str`) – The name of the global variable.
- **`quals`** (`list[str]`) – The qualifiers of the global variable.
- **`tp`** (`TypeRef`) – The type reference of the global variable.

### doc

```
doc: Docstring | None
```

The docstring of the global variable.

### name

```
name: str
```

The name of the global variable.

### quals

```
quals: list[str]
```

The qualifiers of the global variable.

### tp

```
tp: TypeRef
```

The type reference of the global variable.

## DocMacro

```
DocMacro(
    name: str, content: str | None, doc: Docstring | None
)
```

A parsed macro.

Attributes:

- **`content`** (`str | None`) – The content of the macro.
- **`doc`** (`Docstring | None`) – The docstring of the macro.
- **`name`** (`str`) – The name of the macro.

### content

```
content: str | None
```

The content of the macro.

### doc

```
doc: Docstring | None
```

The docstring of the macro.

### name

```
name: str
```

The name of the macro.

## DocType

```
DocType(
    name: str,
    tp: TypeRef,
    doc: Docstring | None,
    quals: list[str],
)
```

A parsed typedef.

Attributes:

- **`doc`** (`Docstring | None`) – The docstring of the typedef.
- **`name`** (`str`) – The name of the typedef.
- **`quals`** (`list[str]`) – The qualifiers of the typedef.
- **`tp`** (`TypeRef`) – The type reference of the typedef.

### doc

```
doc: Docstring | None
```

The docstring of the typedef.

### name

```
name: str
```

The name of the typedef.

### quals

```
quals: list[str]
```

The qualifiers of the typedef.

### tp

```
tp: TypeRef
```

The type reference of the typedef.

## Docstring

```
Docstring(
    desc: str,
    params: list[Param] | None = None,
    ret: str | None = None,
)
```

A parsed docstring.

Attributes:

- **`desc`** (`str`) – The description of the docstring.
- **`params`** (`list[Param] | None`) – The parameters of the docstring.
- **`ret`** (`str | None`) – The return value of the docstring.

### desc

```
desc: str
```

The description of the docstring.

### params

```
params: list[Param] | None = None
```

The parameters of the docstring.

### ret

```
ret: str | None = None
```

The return value of the docstring.

## FuncParam

```
FuncParam(name: str, tp: TypeRef)
```

A parameter in a function signature.

Attributes:

- **`name`** (`str`) – The name of the parameter.
- **`tp`** (`TypeRef`) – The type reference of the parameter.

### name

```
name: str
```

The name of the parameter.

### tp

```
tp: TypeRef
```

The type reference of the parameter.

## InOut

Bases: `StrEnum`

Enumeration for parameter direction.

Attributes:

- **`IN`** – The parameter is an input.
- **`OUT`** – The parameter is an output.
- **`UNSPECIFIED`** – The direction is unspecified.

### IN

```
IN = 'in'
```

The parameter is an input.

### OUT

```
OUT = 'out'
```

The parameter is an output.

### UNSPECIFIED

```
UNSPECIFIED = 'unspecified'
```

The direction is unspecified.

## Macro

```
Macro(text: str, line_number: int)
```

A macro extracted from the source code.

Attributes:

- **`line_number`** (`int`) – The line number of the macro in the source code.
- **`text`** (`str`) – The text of the macro.

### line_number

```
line_number: int
```

The line number of the macro in the source code.

### text

```
text: str
```

The text of the macro.

## Param

```
Param(name: str, desc: str, in_out: InOut)
```

A parameter in a function signature.

Attributes:

- **`desc`** (`str`) – The description of the parameter.
- **`in_out`** (`InOut`) – The direction of the parameter (input, output, or unspecified).
- **`name`** (`str`) – The name of the parameter.

### desc

```
desc: str
```

The description of the parameter.

### in_out

```
in_out: InOut
```

The direction of the parameter (input, output, or unspecified).

### name

```
name: str
```

The name of the parameter.

## SupportsQualsAndType

Bases: `Protocol`

A protocol for types that can have qualifiers and a type.

Attributes:

- **`quals`** (`list[str]`) – The qualifiers of the type.
- **`type`** (`SupportsQualsAndType | TypeDecl | IdentifierType`) – The type of the node.

### quals

```
quals: list[str]
```

The qualifiers of the type.

### type

```
type: SupportsQualsAndType | TypeDecl | IdentifierType
```

The type of the node.

## TypeDecl

Bases: `StrEnum`

Enumeration for type declarations.

Attributes:

- **`ARRAY`** – An array type declaration.
- **`FUNCTION`** – A function type declaration.
- **`NORMAL`** – A normal type declaration.
- **`POINTER`** – A pointer type declaration.

### ARRAY

```
ARRAY = 'array'
```

An array type declaration.

### FUNCTION

```
FUNCTION = 'function'
```

A function type declaration.

### NORMAL

```
NORMAL = 'normal'
```

A normal type declaration.

### POINTER

```
POINTER = 'pointer'
```

A pointer type declaration.

## TypeRef

```
TypeRef(
    name: TypeRef | str,
    decl: TypeDecl,
    quals: list[str],
    params: list[TypeRef] | None = None,
)
```

A reference to a type in C.

Attributes:

- **`decl`** (`TypeDecl`) – The type declaration of the type reference.
- **`name`** (`TypeRef | str`) – The name of the type reference.
- **`params`** (`list[TypeRef] | None`) – The parameters of the type reference.
- **`quals`** (`list[str]`) – The qualifiers of the type reference.

### decl

```
decl: TypeDecl
```

The type declaration of the type reference.

### name

```
name: TypeRef | str
```

The name of the type reference.

### params

```
params: list[TypeRef] | None = None
```

The parameters of the type reference.

### quals

```
quals: list[str]
```

The qualifiers of the type reference.

## ast_to_decl

```
ast_to_decl(
    node: SupportsQualsAndType, types: dict[str, DocType]
) -> TypeRef
```

Convert a pycparser AST node to a TypeRef.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
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
```

## desc

```
desc(doc: Docstring | None) -> str
```

Get the description from a docstring.

Parameters:

- **`doc`** (`Docstring | None`) – The docstring to get the description from.

Returns:

- `str` – The description.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
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
```

## extract_comments

```
extract_comments(code: str) -> tuple[list[Comment], str]
```

Extract comments from the source code.

Parameters:

- **`code`** (`str`) – The source code to extract comments from.

Returns:

- `tuple[list[Comment], str]` – A tuple containing a list of comments and the source code with comments removed.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
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
```

## extract_macros

```
extract_macros(code: str) -> tuple[list[Macro], str]
```

Extract macros from the source code.

Parameters:

- **`code`** (`str`) – The source code to extract macros from.

Returns:

- `tuple[list[Macro], str]` – A tuple containing a list of macros and the source code with macros removed.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
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
```

## get_handler

```
get_handler(
    handler_config: MutableMapping[str, Any],
    tool_config: MkDocsConfig,
    **kwargs: Any,
) -> CHandler
```

Simply return an instance of `CHandler`.

Parameters:

- **`handler_config`** (`MutableMapping[str, Any]`) – The handler configuration.
- **`tool_config`** (`MkDocsConfig`) – The tool (SSG) configuration.

Returns:

- `CHandler` – An instance of CHandler.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
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
```

## lookup_type_html

```
lookup_type_html(
    data: CodeDoc, tp: TypeRef, *, name: str | None = None
) -> str
```

Lookup a type and return an HTML representation.

Parameters:

- **`data`** (`CodeDoc`) – The parsed C source file.
- **`tp`** (`TypeRef`) – The type to lookup.
- **`name`** (`str | None`, default: `None` ) – The name of the type.

Returns:

- `str` – The HTML representation of the type.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
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
```

## parse_docstring

```
parse_docstring(content: str) -> Docstring
```

Parse a docstring.

Parameters:

- **`content`** (`str`) – The content of the docstring.

Returns:

- `Docstring` – A parsed docstring.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
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
```

## tp_ref_to_str

```
tp_ref_to_str(ref: TypeRef, qualname: str) -> str
```

Convert a TypeRef to a string.

Parameters:

- **`ref`** (`TypeRef`) – The TypeRef to convert.
- **`qualname`** (`str`) – The name of the type.

Returns:

- `str` – The string representation of the TypeRef.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
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
```

## typedef_to_str

```
typedef_to_str(decl: DocType) -> str
```

Convert a typedef to a string.

Parameters:

- **`decl`** (`DocType`) – The typedef to convert.

Returns:

- `str` – The string representation of the typedef.

Source code in `src/mkdocstrings_handlers/c/_internal/handler.py`

```
def typedef_to_str(decl: DocType) -> str:
    """Convert a typedef to a string.

    Parameters:
        decl: The typedef to convert.

    Returns:
        The string representation of the typedef.
    """
    return tp_ref_to_str(decl.tp, decl.name)
```
