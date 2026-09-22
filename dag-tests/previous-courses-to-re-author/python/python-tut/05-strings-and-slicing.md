# 05. Strings and Slicing

## Concept

A `str` is an **immutable sequence of Unicode code points**. Everything
from lesson 4 about indexing sequences applies; nothing about mutation
does. There is no `s[0] = 'x'`.

```python
s = "hello"
len(s)         # 5
s[0]           # 'h'        indexing yields a length-1 str, not a char type
s[-1]          # 'o'        s[-k] is s[len(s) - k]
s[1:4]         # 'ell'      slice: indices 1, 2, 3 — j is excluded
s[:3]          # 'hel'      omitted i means 0
s[3:]          # 'lo'       omitted j means len(s)
s[:]           # 'hello'    whole string (for str, s itself: immutable)
s[::2]         # 'hlo'      step
s[::-1]        # 'olleh'    negative step reverses
'l' in s       # True       substring test, not element test
```

The slice notation is `a[i:j:k]` — start, stop, step. It works on any
sequence: `str`, `list`, `tuple`, `range`, `bytes`.

Core methods (all return new strings; none mutate):

```python
" a,b ".strip()            # 'a,b'   strips whitespace from BOTH ends
"xxaxx".strip("x")         # 'a'     strips a SET of chars, not a prefix
"a,b,,c".split(",")        # ['a', 'b', '', 'c']   explicit sep keeps empties
" a  b \n".split()         # ['a', 'b']            no arg: runs of whitespace
",".join(["a", "b"])       # 'a,b'
"abc".replace("b", "ZZ")   # 'aZZc'
"abc".find("z")            # -1      index() raises instead
"abc".startswith("ab")     # True
"Ab".lower(), "Ab".upper() # ('ab', 'AB')
"a1".isalpha(), "12".isdigit(), "a1".isalnum()   # (False, True, True)
"abc".count("b")           # 1
"prefix_x".removeprefix("prefix_")   # 'x'   (3.9+)
```

f-strings interpolate expressions and carry format specs:

```python
n, x = 7, 3.14159
f"{n} items"          # '7 items'
f"{x:.2f}"            # '3.14'      fixed decimals
f"{n:04d}"            # '0007'      zero pad
f"{n:>5}|{n:<5}|"     # '    7|7    |'   align
f"{x!r}"              # '3.14159'   repr, not str
f"{n=}"               # 'n=7'       debug form
```

Code points and bytes:

```python
ord('a'), chr(97)     # (97, 'a')
ord('A')              # 65
"é".encode()          # b'\xc3\xa9'   str → bytes, UTF-8 by default
b'\xc3\xa9'.decode()  # 'é'           bytes → str
len("é"), len("é".encode())          # (1, 2)
b"abc"[0]             # 97 — indexing bytes yields an int, not bytes
```

## Why

### Why half-open intervals, and why they compose

Python slices are half-open: `a[i:j]` covers `a[i..j)` — index i included,
index j excluded. Three properties follow, and together they are the whole
reason the convention was chosen.

**(T1) Length is a subtraction.** For 0 ≤ i ≤ j ≤ n = len(a):

    len(a[i:j]) == j - i

Proof: the index set is {i, i+1, …, j-1}, which is in bijection with
{0, 1, …, j-i-1} via x ↦ x - i, so it has j - i members. ∎

With a closed interval the answer would be j - i + 1, and every length
computation would carry a ±1 you can get wrong. `range(n)` has the same
convention for the same reason: `len(range(i, j)) == j - i`.

**(T2) Every split is exact.** For every integer k (any k — no range
restriction):

    a[:k] + a[k:] == a

Proof for 0 ≤ k ≤ n: the left piece is a[0..k), the right is a[k..n).
These sets are disjoint (nothing is both < k and ≥ k) and their union is
{0..n), so concatenating in index order reproduces a. For k outside
[0, n], Python normalizes first: a negative k becomes k + n, then both
endpoints are clamped to [0, n]. Clamping maps k to some k' ∈ [0, n] and
*uses the same k' in both slices*, reducing to the previous case. ∎

Check the corners: `"abc"[:0] + "abc"[0:]`, `"abc"[:99] + "abc"[99:]`, and
`"abc"[:-99] + "abc"[-99:]` all give `"abc"`.

**(T3) Adjacent slices concatenate.** For 0 ≤ i ≤ j ≤ k ≤ n:

    a[i:j] + a[j:k] == a[i:k]

Proof: [i..j) and [j..k) partition [i..k), same argument as T2. ∎

T3 is what makes divide-and-conquer on sequences trivially correct: split
at any j, solve halves, glue. It is also why an empty slice is the
degenerate case rather than an error — `a[5:5]` is `''`, and if i ≥ j the
result is empty rather than reversed or exceptional.

**Normalization rule** (step > 0). Given `a[i:j]` on length n:

    i' = clamp(i + n if i < 0 else i, 0, n)
    j' = clamp(j + n if j < 0 else j, 0, n)
    result = a[i'..j') , of length max(0, j' - i')

So slicing **never** raises IndexError, while plain indexing does. `a[99]`
is an error; `a[99:]` is `''`. This asymmetry is deliberate: an index names
one element that must exist; a slice names a set that may be empty.

**Extended slices.** For step k > 0 the result is a[i'], a[i'+k], …, so

    len(a[i:j:k]) == max(0, ⌈(j' - i') / k⌉) == max(0, (j' - i' + k - 1) // k)

For k < 0 the defaults flip: start defaults to n-1, stop to "before the
beginning". Hence `a[::-1]` is the full reverse, and `a[i::-1]` walks from
i down to 0. Do not write `a[i:-1:-1]` expecting "down to the start" — the
-1 stop normalizes to n-1 and the result is empty.

### Why immutability

`str` is immutable, so:

- **Sharing is safe.** `t = s` aliases, but no aliasing bug is possible
  because no operation mutates. `s = s + "x"` rebinds `s` to a new object;
  `t` is untouched (lesson 1).
- **Strings are hashable.** A hash may be computed once and cached, and it
  can never go stale. Lesson 6 shows why mutability and hashing conflict.
- **`s[:]` is `s`.** CPython returns the same object for a full slice of a
  str or tuple; for a list it must copy, because a list can be mutated.

The cost: any "edit" allocates. Build strings by collecting pieces in a
list and joining once.

### Why `s += c` in a loop is O(n²), and `join` is O(n)

Claim: building a length-n string with repeated concatenation does
Θ(n²) character copies.

Proof. Strings are immutable, so `s = s + c` must allocate a new object and
copy the contents of both operands. Before the i-th iteration `s` has
length i-1, so that iteration copies i characters. Total:

    Σ_{i=1}^{n} i = n(n+1)/2 = Θ(n²)   ∎

Claim: `''.join(parts)` is Θ(N + m) where N = Σ len(parts[i]) and m is the
number of parts.

Proof. `join` makes two passes: one to sum the m lengths (Θ(m)) so it can
allocate the exact result buffer once, one to copy each part into place
(Θ(N) total, since each character is copied exactly once). No intermediate
object is ever built. ∎

The same argument applies to `list.append` + `join` — appends are amortized
O(1) (lesson 4), so the whole build is O(N).

    # O(n²)                       # O(n)
    s = ""                        parts = []
    for c in xs:                  for c in xs:
        s = s + c                     parts.append(c)
                                  s = "".join(parts)

Caveat, and it is a trap: CPython special-cases `s += t` when `s` is a
local name holding the *only* reference to its string, resizing in place
and giving accidentally linear behaviour. It silently degrades to
quadratic the moment a second reference exists (another name, a list
slot, a debugger). It is an implementation detail of one interpreter.
Write `join`.

### str vs bytes

They are different types and do not mix: `"a" + b"a"` is a TypeError.

- `str` is a sequence of **code points** — integers in [0, 0x110000)
  identifying Unicode characters. `s[i]` is a code point, not a byte, not
  a glyph.
- `bytes` is an immutable sequence of **integers in [0, 256)**. `b[i]` is
  an `int`.
- `encode` (str → bytes) and `decode` (bytes → str) need an encoding;
  UTF-8 is the default and the only one you should use.

UTF-8 is variable width: 1 byte for ASCII, 2–4 for the rest. So byte
offsets are not code point offsets, and `len` differs for non-ASCII text.
CPython dodges this internally (PEP 393): a str stores 1, 2, or 4 bytes
per code point uniformly, picked from the largest code point present. That
uniform width is why `s[i]` is O(1) — you cannot index UTF-8 in O(1).

Note also that a code point is not a user-perceived character: `"é"` may be
one code point (U+00E9) or two (e + combining accent). LeetCode never
tests this; real text does.

### ASCII arithmetic

`ord` and `chr` are inverse bijections between characters and code points.
For the contiguous ASCII ranges this gives arithmetic:

    ord('0') == 48   digits '0'..'9' are 48..57
    ord('A') == 65   uppercase  65..90
    ord('a') == 97   lowercase  97..122

Since the 26 lowercase letters are contiguous, `c ↦ ord(c) - ord('a')` is a
bijection from {'a'..'z'} onto {0..25}: a **perfect hash** into a fixed
26-slot array. That turns character counting into O(1) array indexing with
no dict overhead, and it is why so many string problems are O(n) time,
O(1) space (the 26 is a constant).

```python
def counts(s):                      # s is lowercase a-z
    c = [0] * 26
    for ch in s:
        c[ord(ch) - ord('a')] += 1
    return c
```

Two strings are anagrams iff their count vectors are equal — a Θ(n)
decision, versus Θ(n log n) if you sort.

## Worked examples

```python
>>> a = "abcdef"
>>> len(a[1:4]) == 4 - 1
True
>>> all(a[:k] + a[k:] == a for k in range(-10, 10))
True
>>> a[1:3] + a[3:5] == a[1:5]
True
>>> a[10:], a[-99:2]
('', 'ab')
>>> a[::-1], a[::2], a[4::-1]
('fedcba', 'ace', 'edcba')
```

Split/join round trips:

```python
>>> ",".join("a,b,,c".split(","))
'a,b,,c'                       # exact: explicit sep is lossless
>>> " ".join("  a   b ".split())
'a b'                          # lossy: whitespace collapsed, ends trimmed
>>> "banana".strip("ba")
'nan'                          # a SET of chars, eaten from both ends
>>> "banana".removeprefix("ba")
'nana'                         # what you probably meant
```

Reversal and palindromes:

```python
>>> def is_pal(s): return s == s[::-1]          # O(n) time, O(n) space
>>> def is_pal2(s):                             # O(n) time, O(1) space
...     i, j = 0, len(s) - 1
...     while i < j:
...         if s[i] != s[j]: return False
...         i, j = i + 1, j - 1
...     return True
```

Invariant for `is_pal2`: before each iteration, s[0..i) is the reverse of
s(j..n). It holds initially (both empty) and each iteration extends both
after checking the new pair. At exit i ≥ j, so the unexamined middle is at
most one character, which is its own reverse. ∎

Building output:

```python
>>> rows = [("amy", 30), ("bob", 5)]
>>> "\n".join(f"{name:<6}{age:>3}" for name, age in rows)
'amy    30\nbob     5'
```

Character arithmetic:

```python
>>> [chr(ord('a') + i) for i in range(5)]
['a', 'b', 'c', 'd', 'e']
>>> sum((ord(c) - ord('0')) for c in "1234")     # digits without int()
10
>>> chr(ord('a') ^ 32)                           # ASCII case flip
'A'
```

## Exercises

Open `exercises/05_strings.py`; run `python3 -m pytest exercises/05_strings.py`.

- `split_at(s, k)` — the T2 split; must hold for every integer k.
- `every_kth(s, k)` — reproduce `s[::k]` without extended slicing.
- `letter_counts(s)` — 26-slot count vector via `ord` arithmetic.
- `is_anagram(a, b)` — decide in Θ(n) using the count vector.
- `is_palindrome_alnum(s)` — two pointers, ignoring case and punctuation.
- `caesar_shift(s, k)` — shift letters mod 26, preserving case and others.
- `normalize_spaces(s)` — collapse whitespace runs, trim ends.
- `longest_common_prefix(strs)` — slicing; state the cost.

## LeetCode

- 344 Reverse String — in place on a list of chars; two pointers.
- 125 Valid Palindrome — the `is_pal2` invariant plus filtering.
- 242 Valid Anagram — count vector, Θ(n).
- 383 Ransom Note — count vector, subtraction.
- 387 First Unique Character in a String — two passes over 26 counts.
- 14 Longest Common Prefix — vertical scan or prefix shrinking by slicing.
- 28 Find the Index of the First Occurrence — the naive O(nm) scan first.
- 58 Length of Last Word — `split()` vs a reverse scan; do both.
- 151 Reverse Words in a String — `split()` + `join`, then the O(1)-space version.
- 8 String to Integer (atoi) — `ord` arithmetic and careful bounds.
- 415 Add Strings — digit-wise carry; no `int()`.

## Next

Lesson 06: dicts and sets — the hash table, its invariant, and why "O(1)"
is a statement about expectations, not guarantees.
