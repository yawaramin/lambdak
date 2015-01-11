# lambdak

Expressive functional programming in Python with continuations

The goal is to wrap up all Python statements inside functions so that
they can be run in places which require expressions, e.g. the body of a
`lambda` expression. And, using continuations lets us build expressions
which are effectively composed of multiple statements.

This lets us create the [Holy Grail of
Python](http://en.wikipedia.org/wiki/Monty_Python_and_the_Holy_Grail),
_multi-line lambdas._ Some examples:

```python
actions = {
  "hello":
    print_("Hello, World!", lambda:

    import_("math", lambda m:
    print_("The area of my circle is:", lambda:
    print_(m.pi * 5 * 5)))),

  "goodbye":
    print_("Goodbye, Cruel World!", lambda:

    try_(lambda:
      1 / 0, lambda:
      print_("Danger, Will Robinson!"))) }

actions["hello"]()
actions["goodbye"]()

circumference = (
  import_("math", lambda m:
  2 * m.pi * 5))

print circumference()
```

(Note: I highly recommend using an editor extension like
[vim-cute-python](https://github.com/ehamberg/vim-cute-python) to
prettify the code for readability. For example, it would represent the
keyword 'lambda' with the symbol 'λ', without changing the underlying
source code.)

Anyway, what's with all the lambdas?

We can't escape the fact that Python allows only one expression inside a
lambda block. So, we use _more_ lambdas inside that one expression to
'continue' our computations for as long as we want. Internally, the
functions are designed to conserve stack space and avoid stack overflow.
With this one last construct in Python, all the pieces are in place and
you can fully express your code in _exactly_ the way you want.

## Overview

The central concept in this module is the `lambdak`. This is a callable
type which behaves like a normal Python lambda, except that it can be
composed with more `lambdak`s (or with normal lambdas!) to be extended
so that it can execute an unlimited number of statements and
expressions. And it does so in a way that preserves memory.

The implementation details of the `lambdak` type are not important,
because the functions detailed below work like a set of combinators to
let you compose together a `lambdak` that does exactly what you want
(with some restrictions).

You can think of `lambdak` as a
[DSL](https://en.wikipedia.org/wiki/Domain-specific_language) on top of
normal Python which extends basic lambdas into more powerful multi-line
lambdas.

## Reference

### `let_`

Arguments:

  - `expr`. Any value that we want to bind to a name.

  - `k`. Must be a callable which accepts a single argument and returns
    a value of any type. It will be called with the value of `expr`.

Returns:

The last value returned by the chain of `lambdak`s.

