# 04. Lists, Tuples, Mutability, Aliasing

## Concept

A **list** is a mutable, ordered sequence of object references. A **tuple**
is the immutable counterpart. Both index from 0 and accept negative indices
(`a[-1]` is the last element, `a[-k]` is `a[len(a) - k]`).

```python
a = [3, 1, 2]
a.append(4)        # [3, 1, 2, 4]        O(1) amortized
a.pop()            # returns 4            O(1)
a.pop(0)           # returns 3            O(n)  (shifts everything left)
a.insert(0, 9)     # [9, 1, 2]            O(n)
a.extend([7, 8])   # [9, 1, 2, 7, 8]      O(k)
a.index(2)         # 2                    O(n)
a.sort()           # in place, returns None
b = sorted(a)      # new list, a unchanged
a.sort(key=lambda x: -x)          # descending via key
a.sort(key=len)                   # for lists of strings/lists
t = (1, 2, 3)      # tuple; t[0] = 5 raises TypeError
x, y, z = t        # unpacking
first, *rest = [1, 2, 3, 4]       # first=1, rest=[2, 3, 4]
```

`sort` and `sorted` are stable: equal keys keep their original relative
order. This matters when you sort by one field after another.

## Why

### Names, objects, and the heap

Model the runtime as two functions:

- **env**: name → id (the environment; what a scope's names point to)
- **heap**: id → object (the store; what lives at each id)

`a = [1, 2]` allocates a new object at some id k, sets heap(k) = [1, 2],
and sets env(a) = k. `b = a` sets env(b) = env(a) = k. It copies the *id*,
not the object. Now `a.append(3)` does heap(k) := heap(k) + [3]. Since
env(b) = k too, `b` observes the change. This is **aliasing**: two names,
one object. `a is b` is exactly the test env(a) == env(b).

Nothing is copied by assignment. Ever. Copies are explicit:

```python
c = a[:]            # shallow copy: new list, same element ids
c = list(a)         # same
c = a.copy()        # same
import copy
d = copy.deepcopy(a)   # recursively copies nested mutable objects
```

A shallow copy gives a new outer list whose slots hold the same ids as the
original. If the elements are immutable (ints, strs, tuples of immutables)
that is indistinguishable from a deep copy. If they are lists, it is not.

### The `[[0]*n]*m` bug, proved

Claim: `g = [[0]*n]*m` produces m references to **one** row.

Proof. `[0]*n` is evaluated once, yielding a list at id r. `[row]*m` builds
a list of m slots, each holding the id of the single operand, i.e. r.
So ∀ i, j < m: `g[i] is g[j]`. Therefore `g[0][0] = 1` sets heap(r)[0] = 1,
and every `g[i][0]` reads heap(r)[0] = 1. ∎

Fix: evaluate `[0]*n` m times, once per row.

```python
g = [[0] * n for _ in range(m)]   # m distinct row objects
```

### Mutable default arguments, derived

Rule: a default value expression is evaluated **once, when `def` runs**,
and the resulting object is stored on the function object.

```python
def f(x, acc=[]):
    acc.append(x)
    return acc
```

At `def` time, `[]` is evaluated → id d; `f.__defaults__ == ([],)` holds
that id. Every call that omits `acc` binds env(acc) = d. Since `append`
mutates heap(d), the second call sees the first call's element: `f(1)`
→ `[1]`, `f(2)` → `[1, 2]`. The bug is not a quirk; it is forced by the
rule that defaults are evaluated once plus the rule that assignment copies
ids. The idiom:

```python
def f(x, acc=None):
    if acc is None:
        acc = []          # fresh object per call
    acc.append(x)
    return acc
```

`None` is immutable, so sharing it across calls is harmless.

### Why tuples can be dict keys and lists cannot (preview)

A dict locates a key by `hash(key)`. The lookup is sound only if the hash of
a stored key never changes. A list can be mutated after insertion, which
could change its hash, so lists define no `__hash__`. A tuple of hashable
items cannot change, so its hash is stable. Lesson 06 makes this precise.

### Amortized O(1) append

Python lists are arrays with spare capacity. When full, the list grows by a
constant factor (roughly ×1.125 in CPython; assume ×2 for the argument).

Claim: n appends cost O(n) total. Proof sketch with doubling: resizes happen
at sizes 1, 2, 4, …, 2^k ≤ n, each copying that many elements. Total copy
work Σ_{i=0}^{k} 2^i = 2^{k+1} − 1 < 2n. Plus n unit writes. Total < 3n,
so O(1) per append on average. The same argument works for any growth
factor c > 1 with the geometric sum bounded by n·c/(c−1). ∎

`insert(0, x)` and `pop(0)` shift n elements; use `collections.deque` if
you need O(1) at both ends.

### List as stack

`append` pushes, `pop()` pops, `a[-1]` peeks. All O(1). Most LeetCode
"stack" problems use a plain list.

## Worked examples

```python
>>> a = [1, 2, 3]
>>> b = a
>>> b.append(4)
>>> a
[1, 2, 3, 4]
>>> a is b
True
>>> c = a[:]
>>> c is a, c == a
(False, True)
```

Nested shallow copy:

```python
>>> m = [[1], [2]]
>>> s = m[:]
>>> s[0].append(99)
>>> m
[[1, 99], [2]]        # inner list shared
>>> s[1] = [0]
>>> m
[[1, 99], [2]]        # outer slot reassigned, m unaffected
```

Unpacking and swapping:

```python
>>> a, b = 1, 2
>>> a, b = b, a          # right side evaluated fully first, then bound
>>> pairs = [(1, 'a'), (2, 'b')]
>>> for num, ch in pairs: print(num, ch)
```

Sorting by multiple keys (stable sort, one pass):

```python
>>> people = [("bob", 25), ("amy", 30), ("cat", 25)]
>>> sorted(people, key=lambda p: (p[1], p[0]))
[('bob', 25), ('cat', 25), ('amy', 30)]
```

Stack for bracket matching:

```python
def balanced(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in s:
        if ch in '([{':
            st.append(ch)
        elif not st or st.pop() != pairs[ch]:
            return False
    return not st
```

Invariant: after processing s[0..i), `st` holds exactly the unmatched
openers in order. Each close either matches the top (pop) or proves a
mismatch. At the end, balanced ⇔ no unmatched openers remain.

In-place vs new: a function that mutates its argument should return
`None` (like `list.sort`) so callers cannot confuse the two styles.

## Exercises

Open `exercises/04_lists.py`; run `python3 -m pytest exercises/04_lists.py`.

- `make_grid(m, n, fill)` — m×n grid with independent rows.
- `rotate_left(lst, k)` — new list rotated left by k (k may exceed len).
- `append_safe(item, lst=None)` — append without a shared default.
- `remove_duplicates_preserve_order(lst)` — first occurrence wins.
- `swap_pairs_in_place(lst)` — swap adjacent pairs, mutate, return None.
- `merge_sorted(a, b)` — merge two sorted lists in O(len(a)+len(b)).
- `second_largest(lst)` — second-largest distinct value, or None.

## LeetCode

- 1 Two Sum — brute force with nested loops first; hashing in lesson 06.
- 20 Valid Parentheses — list as stack.
- 26 Remove Duplicates from Sorted Array — in-place write pointer.
- 88 Merge Sorted Array — merge from the back to avoid shifting.
- 189 Rotate Array — slicing, or three reversals in place.
- 169 Majority Element — sort then middle, or Boyer–Moore.
- 118 Pascal's Triangle — building rows; beware `*` aliasing.
- 48 Rotate Image — in-place 2D mutation; transpose then reverse rows.

## Next

Lesson 05: strings, which are immutable sequences — same indexing and
slicing, no in-place mutation.
