# lambdak

Expressive functional programming in Python with continuations

Lambdak is pronounced 'lambda-k'.

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

circumference = given_(lambda r:
  import_("math", lambda m:
  2 * m.pi * r)

print circumference(5)
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
lambdas. Another way to think about it is as composing lots of little
anonymous functions together to make a single, powerful anonymous
function.

## Reference

Contents:

  - [`given_`](#given_)

  - [`let_`](#let_)

  - [`do_`](#do_)

  - [`print_`](#print_)

  - [`assert_`](#assert_)

  - [`raise_`](#raise_)

The `lambdak` module is designed to be 'star-imported' (`from lambdak
import *`): the functions below have all been named with an underscore
character ('_') as the last character.

### `given_`

Receive arguments at the beginning of a lambdak chain so you can call
the lambdak with those arguments.

#### Arguments

  - `k`. A callable (usually a lambda) that takes any number of
    arguments and returns either a final value or another lambdak (to
    continue the computation).

#### Returns

A lambdak that can be called with the same number of arguments that are
accepted by the `k` parameter.

#### Example

```python
f = given_(lambda x:
  let_(x * 2, lambda y:
  print_(y)))

f(2)
```

Output:

    4

You can think of this as, 'Given `x`, let `y` be twice `x`; print `y`'.

### `let_`

#### Arguments

  - `expr`. Any value that we want to bind to a name.

  - `k`. Must be a callable which accepts a single argument and returns
    a value of any type. It represents the rest of the computation and
    will be called with the value of `expr`.

#### Returns

A lambdak that can be called with no arguments or passed into another
chain of lambdaks.

#### Example

Since `lambdak`s can be nested to an arbitrary level, you can take this
example as just a small sample of what's possible.

```python
test = (
  let_(5, lambda x:
  let_(2 * x, lambda y:
  print_("About to return the answer!", lambda:
  y - 9))))

print test()
```

Output:

    About to return the answer!
    1

Think of the above as saying, `test` is a `lambdak` that does the
following:

  - Binds the value `5` to the name `x`

  - Binds the value of the expression `2 * x` to the name `y`

  - Returns the value of the expression `y - 9`.

Behind the scenes, all of the above are joined into a single callable.
You can then call that to run all of its contained actions and
calculations.

Note that we didn't have to assign the `lambdak` to the variable `test`.
We could have passed it in to a function, stored it in a list or other
structure, and treated it any way we'd treat a normal lambda function.
The difference is of course that it contains a lot more than a normal
lambda function would.

### `do_`

Meant to be used when you just want to evaluate an expression which has
a side effect, and then optionally carry on with other actions or
calculations.

#### Arguments

  - `expr`. Any expression that we want to evaluate for its side
    effects.

  - `k`. Optional. If supplied, must be a callable which does not accept
    any arguments and returns any value. This contains the rest of the
    computation (i.e. the rest of the lambdak chain).

#### Returns

The same as `let_` would return.

#### Example

```python
def hello(): print "Hello!"
def hi(): print "Hi!"

test = (
  # Note: we don't really use x here, so the let_ function call is
  # redundant.
  let_(5, lambda x:
  do_(hello(), lambda:
  do_(hi()))))

test()
```

Output:

    Hello!
    Hi!

### `print_`

Print a single expression and optionally carry on the computation.

#### Arguments

  - `x`. The expression to print. This is passed to [Python's `print`
    statement](https://docs.python.org/2/reference/simple_stmts.html#the-print-statement).

  - `k`. Optional. The same as `do_`.

#### Returns

The same as `let_`.

### `assert_`

#### Arguments

  - `expr`. The expression to assert. This is passed to [Python's
    `assert`
    statement](https://docs.python.org/2/reference/simple_stmts.html#the-assert-statement).

  - `k`. Optional. The same as `do_`.

#### Returns

The same as `let_`.

#### Example

```python
f = (
  assert_(True, lambda:
  print_("OK!")))
f()
```

Output:

  OK!

### `raise_`

Behaves the same way as Python's
[`raise`](https://docs.python.org/2/reference/simple_stmts.html#the-raise-statement)
statement. For details on the arguments below, see the documentation
linked.

#### Arguments

  - `ex_type`. Optional.

  - `ex_val`. Optional.

  - `tb_val`. Optional.

#### Returns

`None`.

<!--
### `x_`
#### Arguments
#### Returns
#### Example
-->

