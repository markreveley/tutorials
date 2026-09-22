# 07. Classes, Dunder Methods, Dataclasses

## Concept

A class is a factory for objects that share behaviour. An instance is a
namespace (`__dict__`) plus a pointer to its class.

```python
class Point:
    dims = 2                      # class attribute: one object, shared

    def __init__(self, x, y):     # runs on Point(…); self is the new instance
        self.x = x                # instance attributes: per-object
        self.y = y

    def dist2(self):              # method: a function whose first arg is self
        return self.x ** 2 + self.y ** 2

p = Point(3, 4)
p.dist2()        # 25   — sugar for Point.dist2(p)
```

**Attribute lookup order** for `p.name`: instance `__dict__` → class →
base classes. Assignment `p.name = v` always writes the instance dict.
That asymmetry is the whole story behind the shared-mutable trap:

```python
class Bad:
    items = []                    # one list, owned by the class
    def add(self, v):
        self.items.append(v)      # lookup finds the class list; mutates it

a, b = Bad(), Bad()
a.add(1)
b.items                           # [1]  — b sees a's change
```

`self.items.append` reads (finds the class attribute) then mutates in
place. Had the method done `self.items = self.items + [v]`, the *write*
would have created an instance attribute and the trap would not fire.
Rule: mutable per-instance state is created in `__init__`.

**Dunder (double-underscore) methods** let your objects participate in the
language's operators and protocols:

| You write        | Python calls              |
|------------------|---------------------------|
| `repr(o)`, REPL  | `o.__repr__()`            |
| `str(o)`, print  | `o.__str__()` (falls back to `__repr__`) |
| `a == b`         | `a.__eq__(b)`             |
| `a < b`          | `a.__lt__(b)`             |
| `hash(o)`        | `o.__hash__()`            |
| `len(o)`         | `o.__len__()`             |
| `o[k]`           | `o.__getitem__(k)`        |
| `x in o`         | `o.__contains__(x)` (else iterates) |
| `for x in o`     | `o.__iter__()`            |
| `a + b`          | `a.__add__(b)`            |

**Dataclasses** generate the boilerplate from field declarations:

```python
from dataclasses import dataclass, field

@dataclass(order=True)          # __init__, __repr__, __eq__, __lt__ … from fields
class Task:
    priority: int
    name: str = ""
    tags: list = field(default_factory=list)   # fresh list per instance

@dataclass(frozen=True)         # immutable ⇒ hashable
class Pt:
    x: int
    y: int
```

## Why

### The `__eq__` / `__hash__` contract

Lesson 6 established the dict/set invariant: if `a == b` then
`hash(a) == hash(b)`. A set locates an element by hash first, then
confirms with `==`. If equal objects could hash differently, `x in s`
could look in the wrong bucket and miss an element that `==` says is
present — the set would lie.

Python enforces this at class-definition time: **if you define `__eq__`
and not `__hash__`, `__hash__` is set to `None`** and instances become
unhashable. Proof that the default would violate the invariant: the
default `__hash__` is `id`-based; the default `__eq__` is `is`. Those
agree. Once you override `__eq__` to compare by value, two distinct
objects (different ids, different default hashes) can be equal — the
invariant breaks. Removing `__hash__` is the only safe default.

Corollary for dataclasses: `@dataclass` defines `__eq__` by fields, so by
default instances are unhashable. `frozen=True` makes fields read-only
and defines `__hash__` over the same fields, which satisfies the invariant
(equal fields ⇒ equal hash) *and* keeps it satisfied over time, since the
fields cannot change after insertion.

### Why mutability and hashing conflict

Suppose `o` is hashable, mutable, and hashed by value. Insert `o` into a
set (bucket chosen by `hash(o)`), then mutate `o`. Now `hash(o)` may point
elsewhere; `o in s` searches the wrong bucket and returns `False`, yet
`o` is physically in `s`. The invariant "x ∈ s ⇔ lookup finds x" has
broken. Hence: hash by value only what cannot change (tuples, frozen
dataclasses, strings), or hash by identity.

### Class invariants

A **representation invariant** is a predicate on an object's fields that
every public method assumes on entry and re-establishes on exit. Design
a class by stating it first. Example — `MinStack`:

    Fields:   items: list, mins: list
    Invariant I:
      (1) len(mins) == len(items)
      (2) ∀ k: mins[k] == min(items[0..k])

Proof that every method preserves I:

- `__init__`: both lists empty; (1) trivially, (2) vacuously.
- `push(v)`: append `v` to items and `min(v, mins[-1])` (or `v` if empty)
  to mins. (1) both grew by one. (2) for the new index n,
  `min(items[0..n]) = min(min(items[0..n-1]), v) = min(mins[n-1], v)` by
  the inductive hypothesis (2) on the old state. Old indices unchanged.
- `pop()`: remove the last of each. (1) holds; (2) holds for the
  remaining indices since they were unchanged.
- `get_min()`: returns `mins[-1]`; by (2) it equals `min(items)`. No
  mutation, so I is preserved.

All four are O(1). The invariant is what makes O(1) `get_min` *correct*,
not just fast.

### `__lt__` and ordering

`sorted`, `min`, `heapq` need only `__lt__`. For these to behave, `<`
must be a strict weak order: irreflexive (`not a < a`), transitive, and
incomparability transitive. `order=True` on a dataclass compares fields
lexicographically as a tuple, which is such an order whenever each field's
`<` is. If you hand-write `__lt__`, keep it a pure function of state.

## Worked examples

### A point with operators

```python
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Vec:
    x: float
    y: float
    def __add__(self, o):  return Vec(self.x + o.x, self.y + o.y)
    def __abs__(self):     return math.hypot(self.x, self.y)

Vec(1, 2) + Vec(3, 4)     # Vec(x=4, y=6)
abs(Vec(3, 4))            # 5.0
{Vec(0, 0)}               # works: frozen ⇒ hashable
```

### A container via the sequence protocol

```python
class Ring:
    """Fixed-size ring; index wraps. Invariant: len(self._buf) == self.n."""
    def __init__(self, n):
        self.n = n
        self._buf = [None] * n
    def __len__(self):           return self.n
    def __getitem__(self, i):    return self._buf[i % self.n]
    def __setitem__(self, i, v): self._buf[i % self.n] = v
    def __iter__(self):          return iter(self._buf)
    def __contains__(self, v):   return v in self._buf
    def __repr__(self):          return f"Ring({self._buf!r})"
```

`__repr__` should be unambiguous, ideally evaluable. `__str__` is for
humans; omit it unless they differ.

### LeetCode node conventions

LeetCode hands you these exact shapes. Memorize them.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

Helpers you will write once and reuse: list ↔ linked list converters, and
a level-order builder for trees. Write tests against plain Python lists,
convert at the boundary.

### Sorting objects

```python
@dataclass(order=True)
class Interval:
    start: int
    end: int

ivs = sorted([Interval(5, 6), Interval(1, 3), Interval(2, 4)])
# by start, then end — exactly the order merge-intervals needs
```

Alternative without `order=True`: `sorted(ivs, key=lambda iv: iv.start)`.
Prefer `key=` when the order is problem-specific rather than intrinsic.

### Heap of objects

`heapq` compares elements with `<`. Either give the class `__lt__` or push
tuples `(priority, tiebreak, obj)`; the tiebreak (a counter) stops the heap
from ever comparing two `obj`s.

## Exercises

Open `exercises/07_classes.py`; run `python3 -m pytest exercises/07_classes.py`.

- `Vector` — frozen dataclass with `__add__`, `__sub__`, `__abs__`, `dot`.
- `Stack` — invariant-documented stack with `__len__`, `__iter__`, `__contains__`.
- `MinStack` — O(1) `get_min` via the parallel-mins invariant proved above.
- `ListNode`, `from_list`, `to_list` — LeetCode conversion helpers.
- `Interval` — `__lt__` and `overlaps`; `merge_intervals` using them.
- `Bag` — multiset with `__len__`, `__contains__`, `__getitem__`, `add`.
- `TreeNode`, `tree_height` — recursive height with induction on the tree.

## LeetCode

- 155 Min Stack — the invariant in this lesson, verbatim.
- 706 Design HashMap — buckets of (key, value); state the invariant.
- 707 Design Linked List — ListNode conventions; sentinel head.
- 1603 Design Parking System — trivial class; get the shape right.
- 56 Merge Intervals — sort by `__lt__`, sweep.
- 232 Implement Queue using Stacks — two-stack invariant: queue order = reversed(in) + out.
- 146 LRU Cache — dict + doubly linked list; invariant relates the two.
- 295 Find Median from Data Stream — two heaps; invariant: sizes differ by ≤ 1.

## Next

Lesson 08 — iterators and generators: the `__iter__` protocol you just
used, lazy sequences, and why pipelines run in constant memory.
