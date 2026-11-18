# 06. Dicts, Sets, and Hashing

## Concept

A `dict` maps **hashable** keys to arbitrary values. A `set` is a dict with
no values: a membership test. Both answer "is this key here?" in expected
constant time, which is the single most useful cost profile in the whole
language.

```python
d = {"a": 1, "b": 2}
d["a"]                 # 1        KeyError if missing
d.get("z")             # None     no exception
d.get("z", 0)          # 0        default
d["c"] = 3             # insert or overwrite
del d["c"]             # remove; KeyError if missing
d.pop("c", None)       # remove and return, or default
"a" in d               # True     membership tests KEYS
len(d)                 # 2
d.setdefault("k", [])  # get, inserting the default if absent

for k in d: ...            # keys, in insertion order
for k, v in d.items(): ... # pairs
d.keys(), d.values(), d.items()      # dynamic views, not copies
{k: v * 2 for k, v in d.items()}     # dict comprehension
```

```python
s = {1, 2, 3}          # set literal; {} alone is an empty DICT, use set()
s.add(4); s.discard(9) # discard is silent, remove raises
s | t                  # union            s.union(t)
s & t                  # intersection     s.intersection(t)
s - t                  # difference
s ^ t                  # symmetric difference (in exactly one)
s <= t                 # subset           s.issubset(t)
s.isdisjoint(t)        # no shared element
frozenset([1, 2])      # immutable, hashable — usable as a dict key
```

Two containers from `collections` that remove boilerplate:

```python
from collections import Counter, defaultdict

c = Counter("mississippi")      # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
c["z"]                          # 0 — missing keys count zero, no insert
c.most_common(2)                # [('i', 4), ('s', 4)]
c1 + c2, c1 - c2                # multiset add / saturating subtract

g = defaultdict(list)           # missing key CALLS list() and INSERTS it
g["x"].append(1)                # no KeyError, no setdefault
```

`defaultdict` inserts on read; `Counter` does not. Reading `g["nope"]`
grows `g`. That difference bites during iteration.

## Why

### The hash invariant

A hash table stores a key in a bucket chosen by its hash, and finds it by
looking in that same bucket and comparing with `==`. Two obligations
follow, and every rule about hashing in Python is a consequence.

**(H1) Equal objects hash equal.**   ∀ x, y:  x == y ⇒ hash(x) == hash(y)

Why it is forced: suppose x == y but hash(x) ≠ hash(y), and they land in
different buckets. Insert x, then ask for y. The lookup searches y's
bucket, does not find x there, and reports absent — yet `x == y` says the
key *is* present. The container would contradict `==`. ∎

**(H2) The converse is false, and must be.** hash(x) == hash(y) does not
imply x == y. There are infinitely many distinct strings and only 2⁶⁴
hash values, so by pigeonhole some distinct keys collide. A **collision**
is not a bug; it is inevitable, and the table handles it by comparing with
`==` after finding a candidate. In CPython you can see one directly:

```python
>>> hash(-1) == hash(-2), -1 == -2
(True, False)
```

Consequences:

- Hash is a *filter*, never a decision. `hash(a) == hash(b)` means "maybe";
  only `a == b` decides.
- If you override `__eq__` you **must** override `__hash__` to agree, or
  make the type unhashable. Python's default is to make it unhashable —
  see lesson 7.
- Equal-but-different-typed values share a hash: `1 == 1.0 == True`, so
  `{1: 'a', 1.0: 'b', True: 'c'}` is a one-entry dict. The first key
  inserted is kept; only the value is overwritten.

### Why mutable objects must not be hashable

Model the table as m buckets with bucket index b(x) = hash(x) mod m.

Insert x: place x in bucket b(x).
Lookup y: scan bucket b(y) only.

Soundness of lookup requires that the bucket computed at query time equals
the bucket computed at insert time — i.e. **hash(x) must be constant over
the lifetime of x while x is in the table**.

Now suppose a type hashes by value and can be mutated. Insert x with
hash h₁, stored in bucket h₁ mod m. Mutate x so its hash becomes h₂ with
h₂ mod m ≠ h₁ mod m. Then `x in s` scans bucket h₂ mod m, finds nothing,
returns False — while x is physically in the set and `s` still contains an
object equal to x. The invariant "x ∈ s ⇔ lookup finds x" is broken, and
no amount of care by the caller can repair it. ∎

Python therefore sets `__hash__ = None` on `list`, `dict`, and `set`:

```python
>>> hash([1, 2])
TypeError: unhashable type: 'list'
>>> {[1]: 'x'}
TypeError: unhashable type: 'list'
```

A tuple is hashable **iff all its items are** — `hash((1, [2]))` raises.
This is the rule that makes `(row, col)` a legal key for grid problems and
`tuple(sorted(word))` a legal anagram key.

Escape hatches: `frozenset` for an immutable set, `tuple` for an immutable
list, `@dataclass(frozen=True)` for your own types (lesson 7). Objects
without a value-based `__eq__` hash by identity, which never changes, so
they stay hashable while mutable — sound, but two equal-looking instances
are different keys.

### How the table works (open addressing)

CPython uses **open addressing**: one flat array of slots, no per-bucket
chains. To insert key k with h = hash(k) into a table of size m = 2^b:

    j = h & (m - 1)                    # first probe: low bits of the hash
    while slot j is occupied by a different key:
        j = (5*j + 1 + perturb) & (m - 1)
        perturb >>= 5                  # mixes in the HIGH bits of h
    place k at slot j

The perturbation feeds the high bits of the hash into later probes, so
keys agreeing in their low bits do not follow identical probe sequences.
The **load factor** α = used/m is kept below ⅔; on exceeding it the table
is grown to a larger power of two and every entry is reinserted (its slot
depends on m). Deletion writes a tombstone, since simply emptying a slot
would cut a probe chain in half.

Since 3.6 the storage is *compact*: entries live in a dense
insertion-ordered array, and the hash table holds indices into it. That is
why dicts are memory-lean and why iteration order is insertion order.

### Why "O(1)" is amortized expected, not worst case

Three separate qualifiers, each earned by a different argument.

**Expected.** Assume hashes distribute keys uniformly over slots. The
probability that a given probe hits an occupied slot is at most α, and
probes are (modelled as) independent, so the expected number of probes for
an unsuccessful search is at most

    Σ_{i≥0} α^i = 1/(1 − α)

With α ≤ ⅔ that is ≤ 3 — a constant independent of n. ∎

**Amortized.** Growth reinserts all n entries, costing Θ(n) for one
insertion. But the table only grows when α crosses ⅔, i.e. after Θ(m) new
insertions since the last growth, and it grows by a constant factor. The
geometric-sum argument from lesson 4 applies verbatim: n insertions cost
O(n) total, so O(1) each on average. ∎

**Not worst case.** If every key hashes to the same slot, every operation
degenerates to a linear scan: lookup Θ(n), building the dict Θ(n²). There
is no hash function for which this is impossible — for any fixed h, the
set of keys with h(k) = c is infinite.

**Adversarial input.** An attacker who knows the hash function can supply
n colliding keys and turn an O(n) request handler into O(n²) — the
hash-flooding denial of service. Python's answer (PEP 456) is a per-process
random seed for `str` and `bytes` hashing, so an attacker cannot precompute
collisions:

```python
$ python3 -c "print(hash('a'))"     # differs run to run
$ PYTHONHASHSEED=0 python3 -c "print(hash('a'))"   # pinned, reproducible
```

**Ints are not randomized**: `hash(n) == n` for small ints. So keys
`{0, m, 2m, 3m, …}` for the table size m all take slot 0. This is not
theoretical — it is the reason a competitive-programming judge can make
your dict-based solution time out while the same code runs instantly on
your machine. If int keys may be adversarial, mix them (`hash(k * BIG ^ K)`)
or use sorting/bucketing instead.

Costs to state from memory:

| operation                | expected | worst case |
|--------------------------|----------|------------|
| `k in d`, `d[k]`, `d[k]=v` | O(1)   | O(n)       |
| `del d[k]`, `s.add(x)`   | O(1)     | O(n)       |
| iterate                  | O(n)     | O(n)       |
| `len`                    | O(1)     | O(1)       |
| `a & b` (sets)           | O(min(\|a\|, \|b\|)) | — |

`k in list` is O(n) with a comparison per element; `k in dict/set` is O(1)
expected. Converting a list to a set costs O(n) once and pays for itself
after two lookups. That single substitution is what turns most naive
LeetCode solutions from O(n²) into O(n).

### Ordering guarantees

- **dict preserves insertion order** — an implementation detail in 3.6, a
  language guarantee since 3.7. Re-assigning an existing key keeps its
  original position; deleting and re-inserting moves it to the end.
- **set does not.** Set iteration order depends on hash values and table
  history, and for strings it varies between runs. Never rely on it; call
  `sorted(s)` when order matters.
- Equality ignores order: `{'a': 1, 'b': 2} == {'b': 2, 'a': 1}` is True.

### Set algebra

Sets obey the usual laws — commutativity, associativity, distributivity of
∩ over ∪, De Morgan — and inclusion–exclusion:

    |A ∪ B| = |A| + |B| − |A ∩ B|

The operators require both operands to be sets; the method forms
(`s.union(t)`) accept any iterable. `a & b` iterates the smaller operand
and probes the larger, hence O(min(|a|, |b|)).

## Worked examples

```python
>>> from collections import Counter, defaultdict
>>> nums = [1, 2, 2, 3, 3, 3]
>>> Counter(nums).most_common(1)
[(3, 3)]
>>> {k for k, v in Counter(nums).items() if v == 1}
{1}
```

Two-sum in one pass. Invariant: before examining index i, `seen` maps each
value in nums[0..i) to an index where it occurs.

```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:          # O(1) expected
            return (seen[target - x], i)
        seen[x] = i                     # restores the invariant
    return None
```

Correctness: if a pair (p, q) with p < q sums to target, then at i = q the
invariant puts nums[p] in `seen`, so the test fires no later than q. The
loop is O(n) expected. ∎

Grouping by a canonical key — the shape of a dozen problems:

```python
>>> g = defaultdict(list)
>>> for w in ["eat", "tea", "tan", "ate"]:
...     g["".join(sorted(w))].append(w)     # key: hashable canonical form
>>> dict(g)
{'aet': ['eat', 'tea', 'ate'], 'ant': ['tan']}
```

Tuple keys for grids and memo tables:

```python
>>> seen = set()
>>> seen.add((0, 0))
>>> (0, 0) in seen
True
>>> visited = {(r, c) for r in range(2) for c in range(2)}
```

Views are live:

```python
>>> d = {"a": 1}
>>> ks = d.keys()
>>> d["b"] = 2
>>> list(ks)
['a', 'b']
>>> for k in d: d[k + "!"] = 0      # RuntimeError: dict changed size
```

Never insert into or delete from a container you are iterating. Iterate
`list(d)` (a snapshot) or build a new dict.

## Exercises

Open `exercises/06_dicts_sets.py`; run `python3 -m pytest exercises/06_dicts_sets.py`.

- `is_hashable(x)` — decide by the protocol, not by a type list.
- `two_sum(nums, target)` — the one-pass invariant above.
- `char_count(s)` — dict of counts without `Counter`.
- `first_unique_char(s)` — index of the first non-repeating character.
- `group_anagrams(words)` — canonical hashable key.
- `top_k_frequent(nums, k)` — counts plus an ordering rule.
- `has_close_duplicate(nums, k)` — sliding window of a set.
- `jaccard(a, b)` — |A ∩ B| / |A ∪ B|, with the empty-set convention.

## LeetCode

- 1 Two Sum — the canonical hash-map pass.
- 217 Contains Duplicate — set size vs list length.
- 219 Contains Duplicate II — sliding window set.
- 242 Valid Anagram — Counter equality, or the lesson-5 count vector.
- 387 First Unique Character in a String — count then scan.
- 349 / 350 Intersection of Two Arrays I & II — set algebra vs multiset.
- 49 Group Anagrams — sorted-tuple key.
- 347 Top K Frequent Elements — Counter plus bucket sort in O(n).
- 128 Longest Consecutive Sequence — set membership; only start runs at
  values whose predecessor is absent, giving O(n).
- 205 Isomorphic Strings — two dicts, one per direction.
- 290 Word Pattern — the same bijection argument.
- 454 4Sum II — pair-sum counts in a dict, O(n²).

## Next

Lesson 07: classes and dataclasses — how to make your own types satisfy
the `__eq__` / `__hash__` contract this lesson depends on.
