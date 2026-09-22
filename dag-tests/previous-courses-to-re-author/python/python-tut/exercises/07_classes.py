"""Lesson 07 — Classes, dunder methods, dataclasses.

Run: python3 -m pytest exercises/07_classes.py
"""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    """A 2-D vector. Frozen, so it is immutable and therefore hashable:
    equal fields imply equal hash, and the fields can never change.

    @dataclass supplies __init__, __repr__, __eq__, and __hash__.
    You supply the arithmetic.
    """

    x: float
    y: float

    def __add__(self, other):
        """Return the componentwise sum as a NEW Vector (never mutate self)."""
        raise NotImplementedError

    def __sub__(self, other):
        """Return the componentwise difference as a new Vector."""
        raise NotImplementedError

    def __abs__(self):
        """Return the Euclidean length, so abs(v) works."""
        raise NotImplementedError

    def dot(self, other):
        """Return the dot product self.x*other.x + self.y*other.y."""
        raise NotImplementedError


class Stack:
    """LIFO stack over a list.

    Representation invariant: self._items is a list whose LAST element is
    the top of the stack. Every method assumes this on entry and restores
    it on exit. All operations are O(1) amortized.
    """

    def __init__(self, items=()):
        """Build a stack from an iterable, treating its last item as the top.

        Postcondition: len(self) == len(list(items)) and the stack owns its
        own list (mutating the argument later must not affect the stack).
        """
        raise NotImplementedError

    def push(self, value):
        """Add value on top. Postcondition: self.peek() == value."""
        raise NotImplementedError

    def pop(self):
        """Remove and return the top.

        Precondition: len(self) > 0, else raise IndexError.
        """
        raise NotImplementedError

    def peek(self):
        """Return the top without removing it.

        Precondition: len(self) > 0, else raise IndexError.
        """
        raise NotImplementedError

    def __len__(self):
        """Number of items, so len(s) and truthiness both work."""
        raise NotImplementedError

    def __iter__(self):
        """Iterate from the top down (pop order), without mutating."""
        raise NotImplementedError

    def __contains__(self, value):
        """Membership by ==, so `x in s` works. O(n)."""
        raise NotImplementedError

    def __repr__(self):
        """Unambiguous: Stack([bottom, ..., top])."""
        raise NotImplementedError


class MinStack:
    """A stack that also reports its minimum in O(1).

    Representation invariant I over fields items and mins:
      (1) len(mins) == len(items)
      (2) for every k, mins[k] == min(items[0..k])
    Every method must preserve I; get_min then returns mins[-1] by (2).
    """

    def __init__(self):
        """Postcondition: both lists empty, so I holds vacuously."""
        raise NotImplementedError

    def push(self, value):
        """Push value. Postcondition: I holds; both lists grew by one."""
        raise NotImplementedError

    def pop(self):
        """Remove and return the top.

        Precondition: len(self) > 0, else raise IndexError.
        Postcondition: I holds — the surviving prefixes are unchanged.
        """
        raise NotImplementedError

    def get_min(self):
        """Return the smallest value on the stack in O(1).

        Precondition: len(self) > 0, else raise IndexError.
        """
        raise NotImplementedError

    def __len__(self):
        """Number of items pushed and not yet popped."""
        raise NotImplementedError


class ListNode:
    """A singly linked list node, in LeetCode's exact shape."""

    def __init__(self, val=0, next=None):
        """Store val and the successor (None terminates the list)."""
        raise NotImplementedError

    def __repr__(self):
        """Show this node and its successors: ListNode(1 -> 2 -> 3)."""
        raise NotImplementedError


def from_list(values):
    """Build a linked list from a Python list; return its head.

    Postcondition: from_list([]) is None, and to_list(from_list(v)) == v.
    """
    raise NotImplementedError


def to_list(head):
    """Return the values of the linked list starting at head, as a list.

    Precondition: the list is acyclic (else this does not terminate).
    """
    raise NotImplementedError


class Interval:
    """A closed interval [start, end] of ints.

    Representation invariant: start <= end.
    Hand-written __eq__ and __hash__ show the contract from the lesson:
    equal intervals must hash equally, so both use the same two fields.
    """

    def __init__(self, start, end):
        """Precondition: start <= end, else raise ValueError."""
        raise NotImplementedError

    def __repr__(self):
        """Evaluable form: Interval(1, 3)."""
        raise NotImplementedError

    def __eq__(self, other):
        """Equal iff both endpoints match. Return NotImplemented for
        non-Intervals so Python can try the reflected comparison."""
        raise NotImplementedError

    def __hash__(self):
        """Must agree with __eq__: equal endpoints imply equal hash."""
        raise NotImplementedError

    def __lt__(self, other):
        """Order by start, then end — a strict weak order, so sorted() and
        heapq behave. Postcondition: not (a < a) for every a."""
        raise NotImplementedError

    def overlaps(self, other):
        """Return True iff the closed intervals share at least one point.

        Postcondition: symmetric — a.overlaps(b) == b.overlaps(a).
        """
        raise NotImplementedError


def merge_intervals(intervals):
    """Merge every overlapping or touching pair; return a new sorted list.

    Precondition: intervals is a list of Interval.
    Postcondition: the result is sorted by start, its members are pairwise
    non-overlapping, and it covers exactly the same points as the input.
    Cost: O(n log n), dominated by the sort.
    """
    raise NotImplementedError


class Bag:
    """A multiset: like a set, but it remembers multiplicities.

    Representation invariant: self._counts maps each item present to an int
    >= 1 (never 0), and self._n == sum of the counts.
    """

    def __init__(self, items=()):
        """Build a bag from an iterable of hashable items."""
        raise NotImplementedError

    def add(self, item, count=1):
        """Add count copies of item.

        Precondition: count >= 1 and item is hashable.
        Postcondition: self[item] grew by count; the invariant holds.
        """
        raise NotImplementedError

    def __getitem__(self, item):
        """Return the multiplicity of item — 0 if absent, never KeyError.

        Postcondition: reading an absent item does NOT insert it.
        """
        raise NotImplementedError

    def __len__(self):
        """Total number of items counted with multiplicity."""
        raise NotImplementedError

    def __contains__(self, item):
        """True iff the multiplicity is at least 1. O(1) expected."""
        raise NotImplementedError

    def distinct(self):
        """Return the number of distinct items."""
        raise NotImplementedError


class TreeNode:
    """A binary tree node, in LeetCode's exact shape."""

    def __init__(self, val=0, left=None, right=None):
        """Store the value and the two subtrees (None means empty)."""
        raise NotImplementedError


def tree_height(root):
    """Return the number of nodes on the longest root-to-leaf path.

    Postcondition: 0 for the empty tree, 1 for a single node.
    Proof by structural induction: correct on None; assuming it is correct
    on both (strictly smaller) subtrees, 1 + max(left, right) is the longest
    path through root.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- tests

def test_vector_arithmetic():
    a, b = Vector(1, 2), Vector(3, 4)
    assert a + b == Vector(4, 6)
    assert b - a == Vector(2, 2)
    assert abs(Vector(3, 4)) == 5.0
    assert a.dot(b) == 11
    assert a + b is not a


def test_vector_is_frozen_and_hashable():
    v = Vector(0, 0)
    assert {v, Vector(0, 0)} == {Vector(0, 0)}      # equal ⇒ same set member
    assert {Vector(1, 2) + v} == {Vector(1, 2)}     # results are hashable too
    assert hash(v) == hash(Vector(0, 0))
    assert repr(Vector(1, 2)) == "Vector(x=1, y=2)"
    try:
        v.x = 9
    except Exception as exc:                        # FrozenInstanceError
        assert "frozen" in type(exc).__name__.lower() or isinstance(exc, AttributeError)
    else:
        raise AssertionError("frozen dataclass allowed assignment")


def test_stack_protocol():
    s = Stack()
    assert len(s) == 0 and not s
    s.push(1)
    s.push(2)
    assert len(s) == 2
    assert s.peek() == 2
    assert list(s) == [2, 1]                        # iterates top-down
    assert 1 in s and 99 not in s
    assert s.pop() == 2
    assert s.pop() == 1
    for method in (Stack().pop, Stack().peek):
        try:
            method()
        except IndexError:
            pass
        else:
            raise AssertionError("empty stack must raise IndexError")


def test_stack_owns_its_list():
    src = [1, 2]
    s = Stack(src)
    src.append(3)
    assert len(s) == 2
    assert repr(Stack([1, 2])) == "Stack([1, 2])"


def test_min_stack_invariant():
    m = MinStack()
    for v in (5, 3, 7, 3, 9):
        m.push(v)
    assert len(m) == 5
    assert m.get_min() == 3
    assert m.pop() == 9
    assert m.get_min() == 3
    assert m.pop() == 3
    assert m.get_min() == 3
    assert m.pop() == 7
    assert m.get_min() == 3
    assert m.pop() == 3
    assert m.get_min() == 5


def test_min_stack_matches_min():
    import random
    random.seed(0)
    m, model = MinStack(), []
    for _ in range(200):
        if model and random.random() < 0.4:
            assert m.pop() == model.pop()
        else:
            v = random.randint(-50, 50)
            m.push(v)
            model.append(v)
        assert len(m) == len(model)
        if model:
            assert m.get_min() == min(model)


def test_linked_list_round_trip():
    for values in ([], [1], [1, 2, 3]):
        assert to_list(from_list(values)) == values
    assert from_list([]) is None
    head = from_list([1, 2, 3])
    assert head.val == 1 and head.next.val == 2
    assert repr(head) == "ListNode(1 -> 2 -> 3)"


def test_interval_eq_hash_lt():
    a, b = Interval(1, 3), Interval(1, 3)
    assert a == b and hash(a) == hash(b)
    assert len({a, b}) == 1
    assert a != Interval(1, 4)
    assert a != "not an interval"
    assert Interval(1, 3) < Interval(2, 2)
    assert Interval(1, 3) < Interval(1, 4)
    assert not (a < b)
    assert sorted([Interval(5, 6), Interval(1, 9), Interval(1, 3)]) == [
        Interval(1, 3), Interval(1, 9), Interval(5, 6)]
    try:
        Interval(3, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("start > end must raise ValueError")


def test_interval_overlaps():
    assert Interval(1, 3).overlaps(Interval(2, 5))
    assert Interval(1, 3).overlaps(Interval(3, 5))      # closed: touching counts
    assert not Interval(1, 3).overlaps(Interval(4, 5))
    assert Interval(2, 5).overlaps(Interval(1, 3))      # symmetric


def test_merge_intervals():
    ivs = [Interval(1, 3), Interval(2, 6), Interval(8, 10), Interval(15, 18)]
    assert merge_intervals(ivs) == [
        Interval(1, 6), Interval(8, 10), Interval(15, 18)]
    assert merge_intervals([Interval(1, 4), Interval(4, 5)]) == [Interval(1, 5)]
    assert merge_intervals([Interval(1, 4), Interval(2, 3)]) == [Interval(1, 4)]
    assert merge_intervals([]) == []
    original = [Interval(1, 3), Interval(2, 6)]
    merge_intervals(original)
    assert original == [Interval(1, 3), Interval(2, 6)]  # input untouched


def test_bag():
    b = Bag("mississippi")
    assert len(b) == 11
    assert b["s"] == 4
    assert b["z"] == 0
    assert "z" not in b                                  # reading did not insert
    assert b.distinct() == 4
    b.add("z", 3)
    assert b["z"] == 3 and "z" in b and len(b) == 14
    assert len(Bag()) == 0


def test_tree_height():
    assert tree_height(None) == 0
    assert tree_height(TreeNode(1)) == 1
    root = TreeNode(1, TreeNode(2, TreeNode(4)), TreeNode(3))
    assert tree_height(root) == 3
    chain = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))))
    assert tree_height(chain) == 4
