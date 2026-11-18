# 09. Complexity: O, Θ, Ω, and Amortized Cost

## Concept

### The definitions

Let f, g : ℕ → ℝ≥0. All three are statements about *eventual* behaviour up
to a constant factor.

    f ∈ O(g)   ⇔  ∃c > 0, ∃n₀ ∈ ℕ, ∀n ≥ n₀ :  f(n) ≤ c·g(n)
    f ∈ Ω(g)   ⇔  ∃c > 0, ∃n₀ ∈ ℕ, ∀n ≥ n₀ :  f(n) ≥ c·g(n)
    f ∈ Θ(g)   ⇔  f ∈ O(g) and f ∈ Ω(g)
               ⇔  ∃c₁,c₂ > 0, ∃n₀, ∀n ≥ n₀ :  c₁·g(n) ≤ f(n) ≤ c₂·g(n)

O is an upper bound, Ω a lower bound, Θ a tight bound. To *prove* a bound
you exhibit the witnesses (c, n₀); to *refute* one you assume witnesses
exist and derive a contradiction.

`O(g)` is a set of functions. `f = O(g)` is the traditional abuse of
notation for `f ∈ O(g)`; it is not symmetric, so never write `O(g) = f`.

**Example (proof).** 3n² + 7n + 2 ∈ O(n²). Take c = 12, n₀ = 1. For n ≥ 1,
n ≤ n² and 1 ≤ n², so 3n² + 7n + 2 ≤ 3n² + 7n² + 2n² = 12n². ∎
Also Ω(n²) with c = 3, n₀ = 0, since 3n² + 7n + 2 ≥ 3n². Hence Θ(n²).

**Example (refutation).** n² ∉ O(n). Suppose c, n₀ existed with n² ≤ c·n
for all n ≥ n₀. Divide by n > 0: n ≤ c for all n ≥ n₀. Take
n = max(n₀, ⌈c⌉ + 1) — a contradiction. ∎

The general rule this generalizes: for a polynomial p of degree d with
positive leading coefficient, p ∈ Θ(n^d), witnessed by c = Σ|aᵢ| and
n₀ = 1. Constants and lower-order terms vanish; the *shape* survives.

Worst / average / best case is a separate axis from O / Θ / Ω. "Quicksort
is O(n²)" names its worst case; "quicksort is Θ(n log n) on average" names
the expected cost under random pivots. Say which you mean.

### Reading a loop nest

Cost = the number of times the innermost statement runs. Sum, do not guess.

```python
for i in range(n):            # Σ_{i=0}^{n-1} 1        = n            Θ(n)
    work()

for i in range(n):            # Σ_{i=0}^{n-1} Σ_{j=i+1}^{n-1} 1
    for j in range(i + 1, n): #  = n(n-1)/2                            Θ(n²)
        work()

i = 1
while i < n:                  # i takes 1,2,4,...; stops after
    i *= 2                    #  ⌊log₂ n⌋ + 1 steps                    Θ(log n)

for i in range(1, n + 1):     # Σ_{i=1}^{n} n/i = n·Hₙ
    for j in range(0, n, i):  #  and Hₙ = Θ(log n)                     Θ(n log n)
        work()
```

Two traps that hide a loop inside a line of straight-line code:

```python
for i in range(n):
    if x in lst:              # `in` on a list is Θ(len(lst))  ⇒ Θ(n·m)
        ...
    s = s + t                 # str concat copies             ⇒ Θ(n²)
    out.insert(0, i)          # list insert at 0 shifts       ⇒ Θ(n²)
```

### Amortized analysis: the accounting method

Some operations are occasionally expensive but cheap on average *over any
sequence* — not on a probabilistic average, but as a worst-case guarantee
for the sequence as a whole.

Assign each operation an **amortized cost** â. The method is sound if for
every sequence of m operations,

    Σ_{i=1}^{m} âᵢ  ≥  Σ_{i=1}^{m} cᵢ        (actual costs cᵢ)

Equivalently: the credit balance (Σâ − Σc) never goes negative. Cheap
operations pay a surcharge that is banked as credit; an expensive operation
spends credit it did not have to charge at the time.

**Theorem.** With a growth factor of 2 (double when full), `list.append`
has amortized cost O(1); n appends to an empty list cost O(n) total.

*Proof.* Cost model: writing one element costs 1; a resize that copies k
elements costs k. Charge each append â = 3.

Invariant to maintain: immediately after any append, the list holds at
least 2·(size − capacity/2) credits — i.e. every element past the halfway
mark of the current block carries 2 credits.

- No resize: the append pays 1 to write and banks 2 credits on the new
  element. Every element past the halfway mark still carries 2. ✓
- Resize: the list is full at size = capacity = m, so by the invariant the
  elements in positions m/2 .. m−1 carry 2 credits each: 2·(m/2) = m
  credits, exactly enough to pay the copy of m elements. The copy spends
  all of it. Capacity becomes 2m and size becomes m+1; the halfway mark is
  now m, so only the newly appended element is past it, and the append's
  own 2 banked credits cover it. ✓

The balance is never negative, so Σc ≤ Σâ = 3n = O(n), and the amortized
cost per append is 3 = O(1). ∎

Nothing depends on the factor being 2. For growth factor g > 1, a resize to
capacity m follows m/g appends since the previous one, each of which must
fund m/(m − m/g) = g/(g−1) units of copying, so â = 1 + g/(g−1) = O(1).
CPython actually grows by roughly 1.125× plus a constant, giving a larger
constant and the same O(1). What *fails* is additive growth: growing by a
fixed k gives Σ resizes ≈ n²/(2k) = Θ(n²) total, amortized Θ(n).

Amortized is not average. `list.append` is amortized O(1) worst case: any n
appends cost O(n), with no probabilistic assumption. But a *single* append
is Θ(n) when it resizes — which is why real-time systems preallocate.

### The master theorem

For T(n) = a·T(n/b) + f(n) with a ≥ 1, b > 1, and f eventually positive,
let e = log_b a (the exponent of the leaf count: the recursion tree has
a^(log_b n) = n^e leaves).

    Case 1  f(n) = O(n^(e−ε)) for some ε > 0        ⇒ T(n) = Θ(n^e)
    Case 2  f(n) = Θ(n^e)                          ⇒ T(n) = Θ(n^e · log n)
    Case 3  f(n) = Ω(n^(e+ε)) for some ε > 0,
            and a·f(n/b) ≤ c·f(n) for some c < 1   ⇒ T(n) = Θ(f(n))

Read it as a competition between the leaves (n^e) and the root (f(n)): the
bigger one wins; a tie costs an extra log n, one per level.

When f(n) = Θ(n^k) the test is just k vs log_b a, and you can avoid
logarithms entirely: log_b a > k ⇔ a > b^k.

    merge sort       T = 2T(n/2) + Θ(n)     e = 1,      k = 1  ⇒ Θ(n log n)
    binary search    T = 1T(n/2) + Θ(1)     e = 0,      k = 0  ⇒ Θ(log n)
    binary tree walk T = 2T(n/2) + Θ(1)     e = 1,      k = 0  ⇒ Θ(n)
    Karatsuba        T = 3T(n/2) + Θ(n)     e = log₂3,  k = 1  ⇒ Θ(n^1.585)
    Strassen         T = 7T(n/2) + Θ(n²)    e = log₂7,  k = 2  ⇒ Θ(n^2.807)
    naive matmul     T = 8T(n/2) + Θ(n²)    e = 3,      k = 2  ⇒ Θ(n³)

The theorem does not cover every recurrence: T(n) = T(n−1) + Θ(n) (the
quicksort worst case, Θ(n²)) and T(n) = 2T(n/2) + Θ(n / log n) fall outside
it. Unroll those by hand or use the recursion tree directly.

### Space, including the stack

Total space = input + output + auxiliary. Report **auxiliary** space unless
the output is the interesting part, and say which you are reporting.

Every pending call frame costs space. A recursion of depth d holding O(1)
locals per frame uses Θ(d) space even if it allocates nothing:

```python
def depth_sum(node):                 # tree of height h: Θ(h) stack
    if node is None: return 0
    return node.val + depth_sum(node.left) + depth_sum(node.right)
```

That is O(log n) for a balanced tree and O(n) for a degenerate one — which
is exactly when CPython raises `RecursionError` (default limit ≈ 1000).
Quicksort recursing on the smaller half first bounds the stack at O(log n)
regardless of pivot luck. A generator pipeline (lesson 08) is O(1) because
no stage buffers. A memo table is Θ(number of distinct subproblems).

### CPython cost table

n is the container's length; k the slice or argument length.

| Operation                       | Time            | Note                      |
|---------------------------------|-----------------|---------------------------|
| `lst[i]`, `lst[i] = v`          | Θ(1)            | contiguous array of ptrs  |
| `lst.append(x)`, `lst.pop()`    | Θ(1) amortized  | proved above              |
| `lst.insert(0, x)`, `lst.pop(0)`| Θ(n)            | shifts every element      |
| `x in lst`, `lst.index(x)`      | Θ(n)            | linear scan               |
| `lst[i:j]`, `lst + lst2`        | Θ(k)            | copies                    |
| `len(anything)`                 | Θ(1)            | stored, never counted     |
| `lst.sort()`, `sorted(it)`      | Θ(n log n)      | Timsort; Θ(n) if runs sorted |
| `min`/`max`/`sum`               | Θ(n)            |                           |
| `d[k]`, `k in d`, `d[k] = v`    | Θ(1) expected   | Θ(n) worst per adversarial keys |
| `k in set`, `set.add`           | Θ(1) expected   | the reason to build a set |
| `set(a) & set(b)`               | Θ(min of sizes) |                           |
| `deque.appendleft/popleft`      | Θ(1)            | use for queues, not lists |
| `heapq.heappush/heappop`        | Θ(log n)        | `heapify` is Θ(n)         |
| `s + t` for str                 | Θ(len s + len t)| build a list, then `join` |
| `"".join(parts)`                | Θ(total length) |                           |
| `str[i:j]`, `bytes[i:j]`        | Θ(k)            | strings are immutable     |

The single highest-value line: `x in lst` is Θ(n) and `x in set` is Θ(1)
expected. Turning a membership test inside a loop from list to set is the
difference between Θ(n²) and Θ(n) and is the most common accepted-vs-TLE
edit on LeetCode.

## Why it is part of the answer

A submitted solution is a claim with two parts: *it returns the right
answer* and *it does so within the stated bounds*. Leaving the second part
implicit is leaving the problem half-finished — the interviewer's next
question is always "what's the complexity?", and the honest answer is a
short derivation, not a memorized label.

The discipline: after writing a function, write one line naming the time
and space bound and the reason.

```python
# two_sum_sorted: Θ(n) time — each iteration advances lo or hi, and
# hi - lo strictly decreases from n-1 to 0; Θ(1) auxiliary space.
```

If you cannot write that line, you do not yet know what your code does.

## Worked examples

```python
>>> import timeit
>>> timeit.timeit("999999 in lst", "lst = list(range(10**6))", number=100)
0.5...                                    # Θ(n) per test
>>> timeit.timeit("999999 in s", "s = set(range(10**6))", number=100)
0.00001...                                # Θ(1) per test
```

Counting operations instead of trusting intuition:

```python
>>> def ops(n):
...     c = 0
...     for i in range(n):
...         j = 1
...         while j < n:
...             c += 1
...             j *= 2
...     return c
...
>>> [ops(n) for n in (8, 16, 32)]         # n·(log₂n + 1)
[32, 80, 192]
>>> [n * (n.bit_length()) for n in (8, 16, 32)]
[32, 80, 192]
```

Amortized append, measured:

```python
>>> import sys
>>> lst, caps = [], []
>>> for i in range(20):
...     lst.append(i)
...     caps.append(sys.getsizeof(lst))
>>> sorted(set(caps))            # a handful of distinct block sizes,
[120, 152, 184, 248, 312]        # not 20 — resizes are geometric
```

## Exercises

Open `exercises/09_complexity.py`; run `python3 -m pytest exercises/09_complexity.py`.

- `is_big_o(f_values, g_values, c, n0)` — the definition, made executable.
- `witness_for_polynomial(coeffs)` — return (c, n₀) proving p ∈ O(n^deg).
- `nested_loop_count(n)` — closed form for the triangular nest, in O(1).
- `master_theorem(a, b, k)` — classify T(n) = a·T(n/b) + Θ(n^k) without floats.
- `amortized_append_cost(n)` — simulate doubling; total must stay ≤ 3n.
- `binary_search_counted(xs, target)` — index plus a comparison count ≤ ⌊log₂n⌋+1.
- `cost_class(operation)` — recite the table above.

## LeetCode

- 1 Two Sum — Θ(n²) nested loops vs Θ(n) with a dict; state both.
- 217 Contains Duplicate — the list-vs-set membership lesson, exactly.
- 704 Binary Search — Θ(log n); prove the loop halves the range.
- 912 Sort an Array — merge sort, then apply the master theorem to it.
- 53 Maximum Subarray — Θ(n²) prefix sums vs Θ(n) Kadane (lesson 10).
- 240 Search a 2D Matrix II — Θ(m+n) staircase; argue why it is not Θ(mn).
- 373 Find K Pairs with Smallest Sums — heap; the bound is Θ(k log k), not Θ(mn).
- 4 Median of Two Sorted Arrays — Θ(log(min(m,n))); the bound *is* the problem.

## Next

Lesson 10 applies all of this: array patterns, each with an invariant, a
correctness argument, and a cost argument you can write in one line.
