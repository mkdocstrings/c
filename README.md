# mkdocstrings-c

[![ci](https://github.com/mkdocstrings/c/workflows/ci/badge.svg)](https://github.com/mkdocstrings/c/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://mkdocstrings.github.io/c/)
[![pypi version](https://img.shields.io/pypi/v/mkdocstrings-c.svg)](https://pypi.org/project/mkdocstrings-c/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#c:gitter.im)

A C handler for mkdocstrings.

WARNING: **Still in prototyping phase!**
Feedback is welcome.

NOTE: **C99 full support, C11 partial support**
Since data is extraced with [pycparser](https://github.com/eliben/pycparser), only C99 is fully supported, while C11 is partially supported.

## Installation

```bash
pip install mkdocstrings-c
```

## Usage

With the following header file:

```c title="hello.h"
--8<-- "docs/snippets/hello.h"
```

Generate docs for this file with this instruction in one of your Markdown page:

```md
::: path/to/hello.h
```

This will generate the following HTML:

::: docs/snippets/hello.h
    handler: c
