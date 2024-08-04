# mkdocstrings-c

[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://mkdocstrings.github.io/c/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-708FCC.svg?style=flat)](https://gitpod.io/#https://github.com/mkdocstrings/c)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#c:gitter.im)

A C handler for mkdocstrings.

WARNING: **Still in prototyping phase!**
Feedback is welcome.

## Installation

This project is available to sponsors only, through my Insiders program.
See Insiders [explanation](https://mkdocstrings.github.io/c/insiders/)
and [installation instructions](https://mkdocstrings.github.io/c/insiders/installation/).

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
