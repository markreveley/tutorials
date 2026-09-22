# 01. Objects, Names, and Expressions

## Concept

Python has a handful of built-in scalar types:

```python
42          # int    — arbitrary precision, exact
3.14        # float  — IEEE-754 double, 64 bits, approximate
"hi"        # str    — immutable sequence of Unicode code points
True        # bool   — a subclass of int; True == 1, False == 0
None        # NoneType — the single "no value" object
```

Expressions combine values with operators. Precedence is the usual
mathematical one (`**` binds tightest and is right-associative, then unary
`-`, then `* / // %`, then `+ -`, then comparisons, then `not`, `and`, `or`).

```python
7 / 2       # 2.5   true division, always float
7 // 2      # 3     floor division
-7 // 2     # -4    floor, not truncation
7 % 2       # 1
-7 % 2      # 1     sign follows the divisor
2 ** 10     # 1024
2 ** -1     # 0.5   negative exponent promotes to float
1 < 2 < 3   # True  comparisons chain: (1 < 2) and (2 < 3)
```

Every value is an **object**. An object has an identity (`id(x)`), a type
(`type(x)`), and a value. A **variable is a name bound to an object** — a
label, not a box holding bytes.

```python
a = 1000
b = a          # bind b to the same object a is bound to
a is b         # True  — same identity
a == b         # True  — same value
a = a + 1      # rebind a to a NEW object; b unchanged
a is b         # False
```

`is` compares identity; `==` compares value. `==` is what you almost always
want. `is` is for singletons: `x is None`, `x is True`.

Type checks:

```python
type(3) is int              # exact type
isinstance(True, int)       # True — bool subclasses int
isinstance(3, (int, float)) # tuple of alternatives
```

Truthiness: in a boolean context, `0`, `0.0`, `""`, `None`, and empty
containers are false; everything else is true. `bool(x)` makes it explicit.

Conversions are explicit: `int("42")`, `float(3)`, `str(3.0)`, `int(3.9)`
truncates toward zero (→ `3`), `round(2.5)` is `2` (banker's rounding).

## Why

### Why int and float are separate types

Suppose there were one numeric type. It must satisfy two requirements that
conflict:

1. **Closure under exact arithmetic.** For counting, indexing, hashing, and
   modular arithmetic we need `(a + b) - b == a` and `a * b // b == a`
   to hold *always*. Integers give this; `10**20 + 1 - 10**20 == 1` in Python.
2. **Bounded representation of the reals.** We need `1/3`, `√2`, `π` in
   constant space. No finite encoding represents all reals, so any such
   type rounds, and rounding breaks (1): `0.1 + 0.2 == 0.3` is `False`.

A single type must choose. Python chooses both by keeping them distinct,
and makes the lossy direction explicit: `/` always yields float (so the
result type does not depend on the *values* of the operands, only on the
operator), and `//` stays in int when both operands are int.

Consequence you must internalize: **floats are not reals**. They are a
finite subset of the rationals with ~15.9 significant decimal digits.
Never test floats for equality; test `abs(a - b) < eps`. Never use a float
as a loop counter or a dict key derived from arithmetic.

### Why `//` and `%` use floor, not truncation

Python guarantees, for any ints `a` and `b ≠ 0`:

    a == (a // b) * b + (a % b)           (1)
    0 ≤ a % b < b   when b > 0            (2)

Claim: (1) and (2) together determine a unique pair (q, r). Proof: given
b > 0, the intervals [kb, (k+1)b) for k ∈ ℤ partition ℤ, so exactly one k
has kb ≤ a < (k+1)b. Set q = k, r = a − kb; then 0 ≤ r < b. Uniqueness
follows because a second pair (q', r') with the same bounds gives
|r − r'| = |q' − q|·b < b, forcing q = q'. ∎

Truncation toward zero (C's rule) gives `-7 % 2 == -1`, violating (2). The
floor rule is what makes `i % n` a valid index into a length-n sequence for
*every* integer `i`, including negatives — which is why circular buffers,
ring indexing, and hash-bucket selection work without special cases.

### Why names bind rather than copy

The semantic requirement: assignment must be O(1) regardless of object
size, and two names must be able to refer to one shared structure (a tree
node reachable from two parents). Both force "assignment copies a
reference". The cost is that mutation through one name is visible through
the other — lesson 4 makes this precise. For the immutable types in this
lesson (int, float, str, bool, None) there is no mutation, so sharing is
invisible and harmless.

### Interning: why `is` on ints and strings lies

CPython caches small ints (−5..256) and some strings, so `1000 is 1000` may
be `True` in one context and `False` in another. This is an implementation
detail, not the language. The language only promises `is` semantics for
identity; it never promises *when* two equal immutable values share an
object. Hence the rule: `is` only for `None`, `True`, `False`, and objects
you created yourself.

## Worked examples

```python
>>> x = 7; y = 7.0
>>> x == y, x is y, type(x), type(y)
(True, False, <class 'int'>, <class 'float'>)

>>> 0.1 + 0.2
0.30000000000000004
>>> abs((0.1 + 0.2) - 0.3) < 1e-9
True

>>> divmod(-7, 2)          # (q, r) satisfying a == q*b + r
(-4, 1)
>>> -7 == -4 * 2 + 1
True

>>> s = "abc"; t = s; s = s + "d"
>>> s, t                   # t still bound to original; strings are immutable
('abcd', 'abc')

>>> bool(""), bool("0"), bool(0), bool(0.0), bool(None), bool([])
(False, True, False, False, False, False)

>>> isinstance(True, int), True + True
(True, 2)

>>> 10 ** 30               # ints never overflow
1000000000000000000000000000000
>>> 10.0 ** 400
OverflowError: (34, 'Result too large')
```

Modular arithmetic with negatives, which LeetCode rotation problems need:

```python
>>> n = 5
>>> [i % n for i in range(-3, 8)]
[2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2]
```

## Exercises

Open `exercises/01_objects.py`; run `python3 -m pytest exercises/01_objects.py`.

- `same_object(a, b)` — identity, not equality.
- `is_integer_valued(x)` — ints, integral floats, bools, rejecting everything else.
- `floor_div_and_mod(a, b)` — return (q, r) satisfying the two laws above, without using `//` or `%`.
- `classify(x)` — name the type of a scalar.
- `truthy_count(items)` — count elements that are true in a boolean context.
- `safe_divide(a, b)` — true division, or `None` for a zero divisor.

## LeetCode

- 7 Reverse Integer — `%` and `//` on negatives; the floor rule matters.
- 9 Palindrome Number — digit extraction via `% 10` and `// 10`.
- 50 Pow(x, n) — int vs float, negative exponents (return to this in lesson 3).
- 66 Plus One — carry arithmetic; note Python ints would trivialize it, so do it digit-wise.
- 171 Excel Sheet Column Number — base conversion with `ord`.
- 258 Add Digits — digital root; `(n - 1) % 9 + 1`.
- 263 Ugly Number — repeated `%` and `//`.

## Next

Lesson 2 adds control flow and the discipline for proving loops correct.
