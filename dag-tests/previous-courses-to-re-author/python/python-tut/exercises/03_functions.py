"""Lesson 03 — Functions, scope, closures, recursion.

Run: python3 -m pytest exercises/03_functions.py

For every recursive function, name the base case and the measure that
strictly decreases at each call. Those are the proof.
"""


def apply_n(f, x, n):
    """Return f applied n times to x: f(f(...f(x)...)).

    Precondition: n is an int with n >= 0; f is callable on x and on its
    own output.
    Postcondition: apply_n(f, x, 0) == x, and
    apply_n(f, x, n) == f(apply_n(f, x, n - 1)) for n > 0.
    """
    raise NotImplementedError


def make_counter(start=0):
    """Return a zero-argument function that returns start+1, start+2, ...

    Precondition: start is an int.
    Postcondition: successive calls of the returned function yield
    consecutive integers; two counters made by two calls are independent.
    Use a closure over a local of make_counter plus nonlocal, not a global.
    """
    raise NotImplementedError


def compose(*funcs):
    """Return the composition of funcs, applied right to left.

    Precondition: every element of funcs is a one-argument callable.
    Postcondition: compose(f, g, h)(x) == f(g(h(x))); compose()(x) == x.
    """
    raise NotImplementedError


def with_defaults(func, **defaults):
    """Return a wrapper over func that supplies defaults for missing keywords.

    Precondition: func is callable; defaults maps parameter names to values.
    Postcondition: the wrapper forwards all positional arguments unchanged,
    and passes each key of defaults whose name the caller did not supply.
    An explicit keyword argument always wins over the default.
    """
    raise NotImplementedError


def factorial(n):
    """Return n! recursively.

    Precondition: n is an int with n >= 0.
    Postcondition: result == 1 for n == 0, else n * factorial(n-1).
    Base case n == 0; measure n, which drops by 1 per call.
    """
    raise NotImplementedError


def sum_list(items):
    """Return the sum of items, by structural recursion (no loop, no sum()).

    Precondition: items is a list of numbers.
    Postcondition: result == 0 for the empty list, else
    items[0] + sum_list(items[1:]).
    Measure: len(items).
    """
    raise NotImplementedError


def fib(n, memo=None):
    """Return the n-th Fibonacci number, F(0)=0, F(1)=1, memoized.

    Precondition: n is an int with n >= 0.
    Postcondition: result == F(n), computed with O(n) additions and each
    subproblem solved once. The memo must NOT be a mutable default, and a
    memo passed by the caller may be reused across calls.
    """
    raise NotImplementedError


def flatten(nested):
    """Return a flat list of the non-list leaves of nested, left to right.

    Precondition: nested is a list whose elements are leaves or lists
    (arbitrarily deep, finite, and not self-referential).
    Postcondition: flatten([1, [2, [3]], []]) == [1, 2, 3].
    Measure: the number of list objects reachable from nested.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- tests

def test_apply_n():
    inc = lambda x: x + 1
    assert apply_n(inc, 0, 0) == 0
    assert apply_n(inc, 0, 5) == 5
    assert apply_n(lambda s: s + "!", "hi", 3) == "hi!!!"
    assert apply_n(lambda x: x * 2, 1, 10) == 1024


def test_make_counter():
    c = make_counter()
    assert (c(), c(), c()) == (1, 2, 3)
    d = make_counter(10)
    assert (d(), d()) == (11, 12)
    assert c() == 4                      # independent cells
    assert make_counter(10)() == 11


def test_compose():
    inc = lambda x: x + 1
    dbl = lambda x: x * 2
    assert compose()(7) == 7
    assert compose(inc)(7) == 8
    assert compose(inc, dbl)(7) == 15    # inc(dbl(7))
    assert compose(dbl, inc)(7) == 16    # dbl(inc(7))
    assert compose(inc, inc, inc)(0) == 3


def test_with_defaults():
    def greet(name, greeting="hi", punct="."):
        return f"{greeting}, {name}{punct}"

    loud = with_defaults(greet, greeting="HEY", punct="!")
    assert loud("amy") == "HEY, amy!"
    assert loud("amy", greeting="yo") == "yo, amy!"
    assert greet("amy") == "hi, amy."     # original untouched
    plain = with_defaults(greet)
    assert plain("bob") == "hi, bob."


def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(20) == 2432902008176640000


def test_sum_list():
    assert sum_list([]) == 0
    assert sum_list([7]) == 7
    assert sum_list([1, 2, 3, 4]) == 10
    assert sum_list([-1, 1, -1]) == -1


def test_fib():
    assert [fib(i) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fib(70) == 190392490709135      # would be hopeless unmemoized
    shared = {}
    assert fib(30, shared) == 832040
    assert shared[30] == 832040
    assert fib(5) == 5                     # no leaked state between calls


def test_flatten():
    assert flatten([]) == []
    assert flatten([1, 2, 3]) == [1, 2, 3]
    assert flatten([1, [2, [3, [4]]], 5]) == [1, 2, 3, 4, 5]
    assert flatten([[], [[]], [[1], []]]) == [1]
    assert flatten(["a", ["b", ["c"]]]) == ["a", "b", "c"]
