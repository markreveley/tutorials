"""Lesson 04 — Lists, tuples, mutability, aliasing.

Run: python3 -m pytest exercises/04_lists.py

Every question in this file is answered by one rule: a name binds to an
object, assignment copies the reference, and mutation is visible through
every name that shares it.
"""

import copy


def make_grid(m, n, fill=0):
    """Return an m x n grid (list of m lists of n cells), all cells `fill`.

    Precondition: m >= 0, n >= 0.
    Postcondition: len(result) == m and len(row) == n for every row; no two
    rows are the same object, and no two cells alias the same mutable
    object -- mutating result[i][j] must not change any other cell.
    [[fill] * n] * m is wrong; explain to yourself why before fixing it.
    """
    raise NotImplementedError


def rotate_left(lst, k):
    """Return a NEW list equal to lst rotated left by k positions.

    Precondition: lst is a list; k is any int (it may exceed len(lst) or
    be negative -- k % len(lst) with Python's floor rule normalizes both).
    Postcondition: result[i] == lst[(i + k) % len(lst)] for all i;
    lst is unchanged; result is not lst. The empty list rotates to [].
    """
    raise NotImplementedError


def append_safe(item, lst=None):
    """Append item to lst and return lst; with no lst, start a fresh list.

    Precondition: lst is a list or None.
    Postcondition: append_safe(1) == [1] on EVERY call -- no state leaks
    between calls. When lst is given, it is mutated in place and returned.
    """
    raise NotImplementedError


def remove_duplicates_preserve_order(lst):
    """Return a new list keeping the first occurrence of each element.

    Precondition: every element of lst is hashable -- tuples are, lists
    are not, and a list element must raise TypeError here rather than be
    silently compared in O(n) time.
    Postcondition: result is a subsequence of lst, has no repeats, and
    preserves the order of first appearance.
    """
    raise NotImplementedError


def swap_pairs_in_place(lst):
    """Swap lst[0] with lst[1], lst[2] with lst[3], ... and return None.

    Precondition: lst is a MUTABLE sequence. Passing a tuple must raise
    TypeError -- tuples support no item assignment.
    Postcondition: returns None (like list.sort); lst is mutated; a final
    odd element keeps its position.
    """
    raise NotImplementedError


def merge_sorted(a, b):
    """Merge two sorted lists into one sorted list, in O(len(a)+len(b)).

    Precondition: a and b are each sorted non-decreasing.
    Postcondition: result is sorted, len(result) == len(a) + len(b), and
    is a permutation of a + b. a and b are unchanged. Ties take from a
    first, which makes the merge stable.
    Invariant: out holds the sorted merge of a[0..i) and b[0..j).
    """
    raise NotImplementedError


def second_largest(lst):
    """Return the second-largest DISTINCT value in lst, or None.

    Precondition: lst is a sequence of mutually comparable values.
    Postcondition: None if lst has fewer than two distinct values;
    otherwise the largest value strictly smaller than max(lst).
    One pass, O(1) extra space -- do not sort.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- tests

def test_make_grid_rows_are_independent():
    g = make_grid(3, 2)
    assert g == [[0, 0], [0, 0], [0, 0]]
    g[0][0] = 9
    assert g == [[9, 0], [0, 0], [0, 0]]
    assert g[0] is not g[1]
    assert make_grid(0, 5) == []
    assert make_grid(2, 0) == [[], []]


def test_make_grid_cells_are_independent_when_fill_is_mutable():
    g = make_grid(2, 2, [])
    g[0][0].append(1)
    assert g == [[[1], []], [[], []]]
    assert g[0][0] is not g[0][1]


def test_rotate_left():
    a = [1, 2, 3, 4, 5]
    assert rotate_left(a, 2) == [3, 4, 5, 1, 2]
    assert a == [1, 2, 3, 4, 5]              # not mutated
    assert rotate_left(a, 0) is not a
    assert rotate_left(a, 5) == a
    assert rotate_left(a, 7) == [3, 4, 5, 1, 2]
    assert rotate_left(a, -1) == [5, 1, 2, 3, 4]
    assert rotate_left([], 3) == []


def test_append_safe_has_no_shared_default():
    assert append_safe(1) == [1]
    assert append_safe(2) == [2]             # NOT [1, 2]
    assert append_safe(3) == [3]
    target = [0]
    got = append_safe(1, target)
    assert got == [0, 1] and got is target   # mutates and returns the same list


def test_remove_duplicates_preserve_order():
    assert remove_duplicates_preserve_order([]) == []
    assert remove_duplicates_preserve_order([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert remove_duplicates_preserve_order(["a", "b", "a", "c"]) == ["a", "b", "c"]
    # tuples are hashable, so they work as keys; lists are not
    assert remove_duplicates_preserve_order([(1, 2), (1, 2), (2, 1)]) == [(1, 2), (2, 1)]
    try:
        remove_duplicates_preserve_order([[1], [1]])
    except TypeError:
        pass
    else:
        raise AssertionError("a list element must be rejected as unhashable")


def test_swap_pairs_in_place():
    a = [1, 2, 3, 4]
    assert swap_pairs_in_place(a) is None
    assert a == [2, 1, 4, 3]
    b = [1, 2, 3]
    swap_pairs_in_place(b)
    assert b == [2, 1, 3]                    # odd tail untouched
    c = []
    swap_pairs_in_place(c)
    assert c == []
    try:
        swap_pairs_in_place((1, 2))
    except TypeError:
        pass
    else:
        raise AssertionError("a tuple must reject item assignment")


def test_merge_sorted():
    a, b = [1, 3, 5], [2, 3, 6, 7]
    assert merge_sorted(a, b) == [1, 2, 3, 3, 5, 6, 7]
    assert a == [1, 3, 5] and b == [2, 3, 6, 7]
    assert merge_sorted([], []) == []
    assert merge_sorted([], [1, 2]) == [1, 2]
    assert merge_sorted([1, 2], []) == [1, 2]
    assert merge_sorted([1, 1], [1]) == [1, 1, 1]


def test_second_largest():
    assert second_largest([]) is None
    assert second_largest([4]) is None
    assert second_largest([4, 4, 4]) is None
    assert second_largest([1, 2]) == 1
    assert second_largest([3, 1, 4, 1, 5, 9, 2, 6]) == 6
    assert second_largest([-5, -2, -9]) == -5
    assert second_largest((7, 7, 3)) == 3
