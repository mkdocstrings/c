# mkdocstrings-c

A C handler for mkdocstrings.

Still in prototyping phase!

Feedback is welcome.

C99 full support, C11 partial support

Since data is extraced with [pycparser](https://github.com/eliben/pycparser), only C99 is fully supported, while C11 is partially supported.

## Installation

```
pip install mkdocstrings-c
```

## Usage

With the following header file:

hello.h

```
#ifndef HELLO_H
#define HELLO_H // Header guard for `hello.h`.

// Some macro that holds something.
#define SOME_MACRO 123

// Pointer to an integer.
typedef const int* foo_t;

/*
 * My cool function that does something **cool**!
 * 
 * @param[in] x Input thingy!
 * @param[out] y Output thingy!
 * @param z Some other thing
 */
void foo(int* x, int* y, foo_t z);

const foo_t x = ((foo_t) 0); // Random NULL pointer

#endif
```

Generate docs for this file with this instruction in one of your Markdown page:

```
::: path/to/hello.h
```

This will generate the following HTML:

## `HELLO_H`

Header guard for `hello.h`.

## `SOME_MACRO` `123`

Some macro that holds something.

## `foo_t` `const int*`

Pointer to an integer.

## `foo_t` `x`

Random NULL pointer

## `void` `foo` ( ``` int*``x ```, ``` int*``y ```, ``` foo_t``z ``` )

My cool function that does something **cool**!

| Name | Type        | Description      |
| ---- | ----------- | ---------------- |
| x    | `int*`[in]  | Input thingy!    |
| y    | `int*`[out] | Output thingy!   |
| z    | `foo_t`     | Some other thing |

## Sponsors
