sequential
==========

Sequential wrappers for python functions.  A library that allows you to define the order of function execution independent of the functions themselves.


The Decorators
--------------

Sequential provides three different convenience decorators:
- `before` executes its argument before the decorated function
- `after` executes its argument after the decorated function
- `during` executes its argument in a separate thread while the decorated function runs (waiting for both to finish)

Each of these takes the same arguments as the decorated function.


Chaining
--------

`before` and `after` can be used in a chain with the decorated function, passing the result of one into the result of the next:

    def add_c(word=''):
        return word + 'c'

    def add_b(word=''):
        return word + 'b'

    @before(add_c, chain=True)
    @after(add_b, chain=True)
    def add_a(word=''):
        return word + 'a'

    print(add_a()) # 'cab'

Otherwise, the functions are simply run in order and the result of the decorated function is returned.
