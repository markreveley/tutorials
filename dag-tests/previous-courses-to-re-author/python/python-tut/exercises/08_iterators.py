"""Lesson 08 — Iterators, generators, and laziness.

Run: python3 -m pytest exercises/08_iterators.py
"""

from itertools import count


def manual_iterate(iterable):
    """Return list(iterable), written as the for loop desugars.

    Precondition: iterable is any iterable.
    Postcondition: result == list(iterable).
    Use only iter(), next(), and an explicit StopIteration handler — no for
    loop, no list(), no comprehension.
    """
    raise NotImplementedError


class Countdown:
    """An iterator yielding n, n-1, ..., 1.

    Precondition: n is an int; n <= 0 yields nothing.
    Postcondition: list(Countdown(n)) == list(range(n, 0, -1)). The object is
    its own iterator (iter(c) is c), so it is exhausted after one pass.
    Implement __iter__ and __next__ directly; do not use yield.
    """

    def __init__(self, n):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


def take(iterable, k):
    """Return a list of the first k items of iterable.

    Precondition: k >= 0; iterable may be infinite.
    Postcondition: result == list(islice(iterable, k)), and at most k items
    are drawn from the source — laziness is tested.
    """
    raise NotImplementedError


def evens():
    """Yield 0, 2, 4, 6, ... forever.

    Postcondition: take(evens(), k) == [2 * i for i in range(k)] for all k >= 0.
    """
    raise NotImplementedError


def running_max(iterable):
    """Yield the maximum of every non-empty prefix, lazily.

    Precondition: the items are mutually comparable with >.
    Postcondition: the i-th yielded value equals max(items[0..i]); the
    generator makes one pass and holds O(1) state.
    """
    raise NotImplementedError


def unique_everseen(iterable):
    """Yield the items of iterable in order, skipping any already seen.

    Precondition: the items are hashable.
    Postcondition: the output is the subsequence of first occurrences, and it
    is lazy — item k is yielded before item k+1 is read from the source.
    """
    raise NotImplementedError


def chunk(iterable, size):
    """Yield consecutive lists of length size; the final chunk may be shorter.

    Precondition: size >= 1; iterable may be infinite.
    Postcondition: concatenating the chunks reproduces list(iterable), every
    chunk is non-empty, and all but possibly the last have length == size.
    """
    raise NotImplementedError


def sum_of_squares_of_evens(iterable):
    """Return the sum of x*x over the even ints of iterable.

    Precondition: iterable yields ints; it is consumed exactly once, so it may
    be an iterator.
    Postcondition: result == sum(x * x for x in iterable if x % 2 == 0),
    computed in O(1) auxiliary space — build no list.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- tests

def _logged(n, log):
    """A source that records every item it actually produces."""
    for i in range(n):
        log.append(i)
        yield i


def test_manual_iterate():
    assert manual_iterate([]) == []
    assert manual_iterate([1, 2, 3]) == [1, 2, 3]
    assert manual_iterate("abc") == ["a", "b", "c"]
    assert manual_iterate(iter((4, 5))) == [4, 5]
    assert manual_iterate({"a": 1, "b": 2}) == ["a", "b"]


def test_countdown():
    assert list(Countdown(3)) == [3, 2, 1]
    assert list(Countdown(0)) == []
    assert list(Countdown(-2)) == []
    c = Countdown(2)
    assert iter(c) is c
    assert next(c) == 2
    assert list(c) == [1]
    assert list(c) == []


def test_take():
    assert take([1, 2, 3], 0) == []
    assert take([1, 2, 3], 2) == [1, 2]
    assert take([1, 2, 3], 9) == [1, 2, 3]
    assert take(count(10), 3) == [10, 11, 12]
    log = []
    assert take(_logged(1000, log), 4) == [0, 1, 2, 3]
    assert log == [0, 1, 2, 3]          # exactly k items were computed


def test_evens():
    assert take(evens(), 5) == [0, 2, 4, 6, 8]
    g = evens()
    assert next(g) == 0 and next(g) == 2


def test_running_max():
    assert list(running_max([])) == []
    assert list(running_max([3, 1, 4, 1, 5, 9, 2])) == [3, 3, 4, 4, 5, 9, 9]
    assert list(running_max([2])) == [2]
    assert take(running_max(count(0)), 4) == [0, 1, 2, 3]


def test_unique_everseen():
    assert list(unique_everseen([])) == []
    assert list(unique_everseen("abracadabra")) == ["a", "b", "r", "c", "d"]
    assert list(unique_everseen([1, 1, 2, 3, 2, 1])) == [1, 2, 3]
    log = []
    assert take(unique_everseen(_logged(1000, log)), 3) == [0, 1, 2]
    assert log == [0, 1, 2]             # lazy: no lookahead


def test_chunk():
    assert list(chunk([], 3)) == []
    assert list(chunk([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(chunk([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]
    assert list(chunk("abcde", 1)) == [["a"], ["b"], ["c"], ["d"], ["e"]]
    assert take(chunk(count(0), 3), 2) == [[0, 1, 2], [3, 4, 5]]


def test_sum_of_squares_of_evens():
    assert sum_of_squares_of_evens([]) == 0
    assert sum_of_squares_of_evens(range(10)) == 120
    assert sum_of_squares_of_evens([1, 3, 5]) == 0
    n = 100_000
    assert sum_of_squares_of_evens(iter(range(n))) == sum(
        x * x for x in range(0, n, 2)
    )
