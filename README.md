# lambdak

Full anonymous functions for Python

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

    try_(lambda: 1 / 0,
      except_ = lambda: print_("Danger, Will Robinson!"))) }

actions["hello"]()
actions["goodbye"]()

circumference = given_(lambda r:
  import_("math", lambda m:
  2 * m.pi * r))

print circumference(5)
```

(Note: I highly recommend using an editor extension like
[vim-cute-python](https://github.com/yawaramin/vim-cute-python) to
prettify the code for readability. For example, it would represent the
keyword `lambda` with the symbol 'λ', without changing the underlying
source code.)

Anyway, what's with all the lambdas?

We can't escape the fact that Python allows only one expression inside a
lambda block. So, we use _more_ lambdas inside that one expression to
'continue' our computations for as long as we want. Internally, the
functions are designed to conserve stack space and avoid stack overflow.

## News

  - 2015-01-17: just published a page gathering [tips and
    tricks](https://github.com/yawaramin/lambdak/wiki/Vim-Tips-for-Functional-Pythonistas)
    for Pythonistas using Vim.

## Overview

The central concept in this module is the `lambdak`. This is a callable
type which behaves like a normal Python lambda, except that it can be
composed with more `lambdak`s (or with other values) so that it can
execute an unlimited number of statements and expressions. And it does
so in a way that preserves memory.

The lambdak functions that you'll see below mostly follow this pattern:

```python
def something_(..., k = None): ...
```

They mostly take some arguments up front that they need to carry out
some action; and then they take a final optional argument (`k`, the
'continuation'), which can be either:

  - A function that returns another lambdak, to indicate that we want to
    continue the computation; or

  - Anything else, to indicate that this should be the final result of
    the computation.

You can imagine a chain of lambdaks, each one calling the next one in
the chain and passing on any relevant values from its computation.
Sometimes there is no relevant value; for example if you print two
things one after the other there's no useful value from the first print
action that can be passed on the the next print action. Lambdaks
automatically handle all of that. You just compose them with the
required values, and lots of lambdas.

## Reference

The `lambdak` module is designed to be 'star-imported' (`from lambdak
import *`): the functions below have all been named with an underscore
character ('_') as the last character.

<!-- Reminder: vim bookmark 'r -->

### Contents

  - [`call_(k)`](#call_)

  - [`given_(k)`](#given_)

  - [`do_(expr_k, k = None)`](#do_)

  - [`print_(x, k = None)`](#print_)

  - [`assert_(expr, k = None)`](#assert_)

  - [`for_(seq, act_k, k = None)`](#for_)

  - [`while_(seq, act_k, k = None)`](#while_)

  - [`with_(expr_k, act_k, k = None)`](#with_)

  - [`cond_(test_pairs, default_expr, k = None)`](#cond_)

  - [`import_(mod_name, k)`](#import_)

  - [`try_(expr_k, except_, else_ = None, finally_ = None)`](#try_)

  - [`raise_(ex_type = None, ex_val = None, tb_val = None)`](#raise_)

  - [`assign_(nm, v, d, k = None)`](#assign_)

  - [`get_(nm, d)`](#get_)

  - [`mod_(nm, f, d, k = None)`](#mod_)

  - [`del_(nm, d, k = None)`](#del_)

  - More (both pending documentation and implementation)

### `call_`

Call the given function with no arguments.

#### Arguments

  - `k`. The function to call. It will be called with no arguments.

#### Returns

The result returned by `k`, or `None` if `k` is `None`.

### `given_`

Receive arguments at the beginning of a lambdak chain so you can call
the lambdak with those arguments. These arguments can also have default
values, which effectively lets you bind names to values for the duration
of the `k` closure's scope.

#### Arguments

  - `k`. A callable (usually a lambda) that takes any number of
    arguments and returns either a final value or another lambdak (to
    continue the computation).

#### Returns

A lambdak that can be called with the same number of arguments that are
accepted by the `k` parameter. If the lambdak is called with no
arguments, it will call `k` with no arguments.

#### Example

This example shows both uses of `given_`: providing a way to pass in
arguments to call the outermost lambdak with, and also providing a way
to bind names to values inside a lambdak.

```python
f = given_(lambda x:
  given_(lambda y = 2 * x:
    print_(y)))

f(2)
```

Output:

    4

You can think of this as, 'Given `x`, let `y` be twice `x`; print `y`'.

### `do_`

Meant to be used when you just want to evaluate an expression which has
a side effect, and then optionally carry on with other actions or
calculations.

#### Arguments

  - `expr_k`. Any expression that we want to evaluate for its side
    effects. Must be a callable (usually a lambda expression wrapping a
    value or function call). Will be called (evaluated) when the `do_`
    lambdak is eventually run. We want to delay evaluation because the
    expression may have side effects, so we want to keep them in
    sequence.

  - `k`. Optional (default `None`). If supplied, must be a callable
    which does not accept any arguments and returns any value. This
    contains the rest of the computation (i.e. the rest of the lambdak
    chain).

#### Returns

The same as `given_` would return.

#### Example

```python
def hello(): print "Hello!"
def hi(): print "Hi!"

test = (
  do_(lambda: hello(), lambda:
  do_(lambda: hi())))
```

Output: nothing yet.

```python
test()
```

Output:

    Hello!
    Hi!

### `print_`

Print a single expression and optionally carry on the computation.

#### Arguments

  - `x`. The expression to print. This is passed to Python's
    [`print`](https://docs.python.org/2/reference/simple_stmts.html#the-print-statement)
    statement.

  - `k`. Optional (default `None`). The same as `do_`.

#### Returns

The same as `given_`.

### `assert_`

#### Arguments

  - `expr`. The expression to assert. This is passed to Python's
    [`assert`](https://docs.python.org/2/reference/simple_stmts.html#the-assert-statement)
    statement.

  - `k`. Optional. The same as `do_`.

#### Returns

The same as `given_`.

#### Example

```python
f = (
  assert_(True, lambda:
  print_("OK!")))

f()
```

Output:

    OK!

### `for_`

Wraps Python's
[`for`](https://docs.python.org/2/reference/compound_stmts.html#the-for-statement)
statement. Fully functional, including the ability to break out of the
loop and 'continue' (skip) to the next iteration.

To break out of the loop, simply return an object of type `break_`
from the `act_k` function. To continue (skip), return an object of type
`continue_`. These objects can be constructed using default
constructors, i.e. they will look like normal function calls in your
code. See examples below.

#### Arguments

  - `seq`. An iterable.

  - `act_k`. A function that takes one argument and returns the same
    thing as `k` (below). It will be called on each iteration of the
    loop with the value obtained from the iterable.

  - `k`. Optional (default `None`). A function that takes no arguments
    and returns either a lambdak or a final value. It will be called
    after the loop is finished to let you continue with something else
    or stop this chain of the computation.

#### Returns

The same as `given_`.

#### Example

Print some numbers:

```python
for_(range(1, 6), lambda i:
  print_("Number: %s" % i), lambda:
print_("Finished!"))()
```

Output:

    Number: 1
    Number: 2
    Number: 3
    Number: 4
    Number: 5
    Finished!

Break out of the loop:

```python
for_(range(1, 6), lambda i:
  break_() if i == 3
  else print_("Number: %s" % i), lambda:
print_("Finished!"))()
```

Output:

    Number: 1
    Number: 2
    Finished!

Continue to the next iteration:

```python
for_(range(1, 6), lambda i:
  continue_() if i == 3
  else print_("Number: %s" % i), lambda:
print_("Finished!"))()

    Number: 1
    Number: 2
    Number: 4
    Number: 5
    Finished!
```

Notice how nothing is printed when `i` is 3!

### `while_`

Wraps Python's
[`while`](https://docs.python.org/2/reference/compound_stmts.html#the-while-statement)
statement. Like `for_`, fully supports breaking and continuing.

#### Arguments

  - `expr_k`. A function that takes no arguments and returns a boolean
    value. This function is called at each iteration of the loop and the
    resulting value is used as the test for whether to carry out the
    loop action.

  - `act_k`. A function that takes no arguments and returns either a
    lambdak to continue the computation, or a final value to finish this
    iteration of the loop. This is the loop action. As with the `for_`
    lambdak, you can break or continue by returning values of type
    `break_` or `continue_`. See the examples in the `for_` lambdak
    (above).

  - `k`. Optional (default `None`). The same as `for_`.

#### Returns

The same as `for_`.

#### Example

Simple loop:

```python
d = { 1: 1 }
inc = lambda x: x + 1

while_(lambda: d[1] < 5, lambda:
  print_(d[1], lambda:
  mod_(1, inc, d)))()
```

Output:

    1
    2
    3
    4

### `with_`

Wraps Python's
[`with`](https://docs.python.org/2/reference/compound_stmts.html#with)
statement, but is limited to only a single context binding at a time.

#### Arguments

  - `expr_k`. Something that can be called with no arguments to get the
    context manager.

  - `act_k`. Something that will be called with either one argument, or
    none, depending on whether context manager binds a value or not.

    If the context manager doesn't bind a value, i.e. if the equivalent
    `with` block in normal Python would have been `with x: ...` instead
    of `with x as y: ...`, then `act_k` will be called without any
    arguments.

    If the context manager _does_ bind a value, then `act_k` will be
    called with that value as the argument.

  - `k`. Optional (default `None`). The same as for `do_`.

#### Returns

The same as for `given_`.

#### Example

First, the imports.

```python
from contextlib import closing, contextmanager
from lambdak import *
import StringIO
```

The example of a context manager not binding a value. Here we define a
spurious context manager that just prints some text at the start and
finish.

```python
@contextmanager
def ctx():
  print "Start!"
  yield
  print "End!"

with_(ctx, lambda: None)()
```

Output:

    Start!
    End!

The example of a context manager binding a value. Here we show a more
real-world scenario, of opening a resource within the context manager,
doing something to it, and then getting its final value before the
context manager automatically closes it.

```python
with_(lambda: closing(StringIO.StringIO()), lambda s:
  do_(lambda: s.write("Hello, World!"), lambda:
  print_(s.getvalue())))()
```

Output:

    Hello, World!

### `cond_`

Evaluate a list of tests one by one until one of them evaluates to
`True`, and evaluate and return its corresponding value expression.

Short-circuiting: if one of the condition tests evaluates to `True`, it
won't try to evaluate any of the other tests and value expressions after
that one.

Should be used in the same way as Python's `if: ... elif: ... else:`
statement would be, or a switch statement in some other language.

#### Arguments

  - `test_pairs`. Must be a sequence (i.e. iterable, like a list) of
    tuples of (`test_expr`, `then_expr`).

    `test_expr` will be called with no arguments to get a boolean value
    to be tested.

    If the value is `True`, `then_expr` will be called with no arguments
    and the result will be passed on to the `k` function (see below).

    If the value is `False`, the next `test_expr` in the sequence will
    be called, and so on.

  - `default_expr`. If none of the `test_expr`s evaluated to `True`,
    then this expression will be called with no arguments and the result
    passed on to the `k` function. This argument is required as a way to
    force the developer to think about all possible cases. But as a
    convenience, you can pass in `None` and it will do the right thing.

  - `k`. Optional (default `None`). This must be a function which takes
    no arguments and returns either a lambdak (to indicate a continuing
    computation), or anything else (to indicate stopping).

    If you have effectful code in your `then_expr`s, you won't
    necessarily return a meaningful value from them; rather you will be
    returning the actions (lambdaks) themselves. As a convenience, you
    can use the handy `return_` function as this argument in those cases
    to just pass along that lambdak and carry out the action. See the
    second example below.

#### Returns

The same as `given_`. You can think of this as a let binding where one
binding will ultimately be chosen out of multiple possible bindings.

#### Example

A 'pure' value calculated and returned:

```python
cond_(
  [ (lambda: False, lambda: 0),
    (lambda: True, lambda: 1) ],
  None, # Default
  lambda val: # The computed value.
print_(val))()
```

Output:

    1

An 'effectful' action (lambdak) computed and returned:

```python
cond_(
  [ (lambda: False, lambda: print_(0)),
    (lambda: True, lambda: print_(1)) ],
  None,
return_)()
```

Output:

    1

The `return_` function works because it's the exact same thing as
`lambda x: x`, which is what we need as the last argument of `cond_` to
pass on the computed lambdak (action).

### `import_`

Import a module and bind the module object to the parameter name of the
`k` function (see below).

#### Arguments

  - `mod_name`. A string containing the name of the module to import.

  - `k`. A function that takes one argument and returns a lambdak (to
    continue the computation) or a final result (to stop). It will be
    called with the value of the imported module. Thus, the argument
    will be bound to the module object.

#### Returns

The same as `given_`.

#### Example

To print the area of a circle with radius 5 units:

```python
import_("math", lambda m:
print_(m.pi * 5 * 5))()
```

Output:

    78.5398...

### `try_`

Wrapper for Python's
[`try`](https://docs.python.org/2/reference/compound_stmts.html#the-try-statement)
statement. The last three arguments are meant to be named when `try_` is
called; this is different from the other lambdak functions' usual call
still but because of the different permutations of the arguments, it's
more unambiguous to name the arguments and also it looks more naturally
like Python's normal `try` statement. See the example below.

#### Arguments

  - `expr_k`. A function that takes no arguments and returns an
    expression to try.

  - `except_`. A function that takes no arguments and does anything. You
    can think of this as the same as the `do_` lambdak's `k` parameter.
    It is only run if the `expr_k` function raises an exceptio.

  - `else_`. Optional (default `None`). A function that takes no
    argument and does anything. It is only called if the `expr_k`
    function does _not_ raise an exception.

  - `finally_`. Optional (default `None`). A function that takes no
    arguments and returns either a lambdak or a final result. Doubles as
    the `finally` block of the `try` statement and as the continuation
    function, because the `finally` block is _always_ executed whether
    or not an exception occurred.

#### Returns

The same as `given_`.

#### Example

```python
try_(lambda: 1 / 0,
  except_ = lambda: print_("Error!"),
  else_ = lambda: print_("No error."),
  finally_ = lambda: print_("Cleanup."))()
```

Output:

    Error!
    Cleanup.

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

Theoretically `None`, but actually never returns because the `raise`
statement jumps control flow to whichever `except: ...` block is
closest, or failing that it crashes the program.

### `assign_`

Assign a value to a dict object given its key. This function can
be used to manipulate the module's global variables. Example shown
below.

#### Arguments

  - `nm`. The key to look up in the dict.

  - `v`. The value to assign to the corresponding object.

  - `d`. The dict to look in.

  - `k`. Optional (default `None`). Same as for `do_`.

#### Returns

The same as `given_`.

#### Example

To potentially change a global variable `x` to some value:

```python
test = assign_("x", 1, globals())
```

To actually change the value:

```python
test()
```

### `get_`

Get the value of an object in a dict given its key. Note that this
function doesn't have a continuation. It's a pure function with no side
effects (unless someone has changed the very mechanism of dict
lookups themselves), so it doesn't need one.

#### Arguments

  - `nm`. The key to look for.

  - `d`. The dict to look in.

#### Returns

The value corresponding to the given key `nm`.

#### Example

```python
x = get_("x", { "x": 1 })
print x
```

Output:

    1

### `mod_`

Modify in-place the value of an object in a dict given its key.

#### Arguments

  - `nm`. The key.

  - `f`. The modification function. For example, if the function is
    `lambda x: x + 1`, then the value will be incremented by one.

  - `d`. The dict to look in.

  - `k`. Optional (default `None`). The same as `assign_`.

#### Returns

The same as `assign_`.

#### Example

See the example in [`while_`](#while_).

### `del_`

Delete a key-value pair from a dict. This can also be used to delete a
global variable. See example below.

#### Arguments

  - `nm`. The key to look for.

  - `d`. The dict to look in.

  - `k`. Optional (default `None`). Same as for `do_`.

#### Returns

The same as `given_`.

#### Example

To immediately delete a global variable:

```python
# In global scope
x = 1

del_("x", globals())()
print x
```

Output:

    NameError: name 'x' is not defined

_Made with λ by yawaramin._

<!--
### `x_`
#### Arguments
#### Returns
#### Example

-->

