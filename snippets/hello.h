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
