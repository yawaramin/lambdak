# lambdak

Expressive functional programming in Python with continuations

The goal is to wrap up all Python statements inside functions so that
they can be run in places which require expressions, e.g. the body of a
`lambda` expression. And, using continuations lets us build expressions
which are effectively composed of multiple statements.

This lets us create the [Holy Grail of
Python](http://en.wikipedia.org/wiki/Monty_Python_and_the_Holy_Grail),
multi-line lambdas. Here's an example:

    actions = {
      "hello":
        print_("Hello, World!", λ:

        import_("math", λ m:
        print_("The area of my circle is:", λ:
        print_(m.pi * 5 * 5)))),

      "goodbye":
        print_("Goodbye, Cruel World!", λ:

        try_(λ:
          1 / 0, λ:
          print_("Danger, Will Robinson!"))) }

    actions["hello"]()
    actions["goodbye"]()

(Note: for aesthetic reasons, λ means lambda.)

What's with all the lambdas?

We can't escape the fact that Python allows only one expression inside a
lambda block. So, we use _more_ lambdas to 'continue' our computations
for as long as we want. Internally, the functions are designed to
conserve stack space and avoid stack overflow. With this one last
construct in Python, all the pieces are in place and you can fully
express your code in _exactly_ the way you want.

