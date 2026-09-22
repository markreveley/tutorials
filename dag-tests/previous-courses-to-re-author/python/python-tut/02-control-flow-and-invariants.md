# 02. Control Flow and Invariants

## Concept

Blocks are delimited by a colon and indentation (4 spaces, never tabs).
There are no parentheses around conditions and no braces.

```python
if x < 0:
    sign = -1
elif x == 0:
    sign = 0
else:
    sign = 1

sign = -1 if x < 0 else (0 if x == 0 else 1)   # conditional *expression*
```

`elif` is a single keyword, not a nested `else: if:`; the chain tests in
order and takes the first true branch. `pass` is the empty statement.

Two loops:

```python
i = 0
while i < n:            # test, body, repeat
    i += 1

for x in items:         # bind x to each element in turn
    ...
```

`range(stop)`, `range(start, stop)`, `range(start, stop, step)` produce
integers over the **half-open** interval `[start, stop)`:

```python
range(n)            # 0, 1, ..., n-1          — n values
range(1, n)         # 1, ..., n-1
range(n - 1, -1, -1)   # n-1, n-2, ..., 0     — countdown
range(0, n, 2)      # even indices
len(range(a, b))    # max(0, b - a)
```

Half-open is not arbitrary: `len(range(a, b)) == b - a`, adjacent ranges
`[a, m)` and `[m, b)` tile `[a, b)` with no overlap and no gap, and an empty
range is written `[a, a)` rather than needing a special case. Python slices
use the same convention, so index reasoning transfers.

Iterate over elements, not indices, unless you need the index:

```python
for i, x in enumerate(items):        # (0, items[0]), (1, items[1]), ...
for a, b in zip(xs, ys):             # stops at the shorter one
```

`break` leaves the loop immediately. `continue` skips to the next
iteration. A loop may carry an `else` clause, which runs **iff the loop
finished without executing `break`**:

```python
for p in range(2, n):
    if n % p == 0:
        break
else:
    print(n, "is prime")     # no divisor found
```

Read `else` here as `no_break`. It removes the "did I find it?" flag
variable, which is a variable you would otherwise have to reason about.

`and` and `or` short-circuit and evaluate to one of their **operands**, not
to a bool: `x or default` yields `x` when `x` is truthy, else `default`.
That is why `if lst and lst[0] == 1:` is safe on an empty list — `lst[0]`
is never evaluated.

## Why

### Hoare triples

Write `{P} S {Q}` for: if predicate P holds and statement S terminates,
then Q holds afterwards. P is the precondition, Q the postcondition. This
is *partial* correctness; total correctness is partial correctness plus a
proof of termination, which we always give separately.

The rule for assignment runs backwards:

    {Q[x := e]}  x = e  {Q}

To get Q afterwards, require Q with every free `x` replaced by `e`
beforehand. Example: to conclude `{y > 5}` after `y = y + 1`, we need
`{y + 1 > 5}`, i.e. `{y > 4}`, before. Working backwards from the goal is
the whole method: you never guess a precondition, you compute it.

Sequencing and branching compose:

    {P} S1 {R} ,  {R} S2 {Q}          {P ∧ B} S1 {Q} ,  {P ∧ ¬B} S2 {Q}
    ----------------------            ------------------------------------
      {P} S1; S2 {Q}                    {P} if B: S1 else: S2 {Q}

The `if` rule says exactly what a case analysis says: prove the goal on
each branch, using the branch condition as an extra assumption.

### The while rule

Loops are the only construct that needs an idea rather than a mechanical
step, because a loop stands for an unbounded number of statements. The
idea is the **invariant** I:

    {I ∧ B} S {I}
    ---------------------------------
    {I}  while B: S  {I ∧ ¬B}

So proving `{P} while B: S {Q}` decomposes into four obligations:

1. **Establishment.** P ⇒ I. The invariant holds before the first test.
2. **Preservation.** {I ∧ B} S {I}. One iteration re-establishes it.
3. **Sufficiency.** (I ∧ ¬B) ⇒ Q. Invariant plus exit condition gives the goal.
4. **Termination.** B eventually fails.

For (4), exhibit a **variant**: an integer expression V such that
I ∧ B ⇒ V ≥ 0, and every iteration strictly decreases V. There is no
infinite strictly decreasing sequence in ℕ (well-ordering), so the loop
cannot run forever. ∎

Note what I is *not*: it is not "what is true at the end". It is what is
true at the top of every iteration, including the first and the last —
which means it is usually a statement about a *partial* result over a
*prefix* of the data. **Choose I first, then write the loop that maintains
it.** The body is then almost forced.

### Proof 1 — sum and maximum of a prefix

    def scan(nums):                       # n = len(nums)
        total = 0
        best = None
        i = 0
        while i < len(nums):
            total = total + nums[i]
            if best is None or nums[i] > best:
                best = nums[i]
            i = i + 1
        return total, best

Goal Q: `total = Σ nums[0..n)` and `best = max nums[0..n)` (None if n = 0).

Invariant I:

    0 ≤ i ≤ n  ∧  total = Σ nums[0..i)
               ∧  (i = 0 ⇒ best is None)
               ∧  (i > 0 ⇒ best = max nums[0..i))

*Establishment.* i = 0, total = 0 = Σ over the empty range, best is None,
and 0 ≤ 0 ≤ n. So I holds. ✓

*Preservation.* Assume I ∧ i < n. The body computes
total′ = total + nums[i] = Σ nums[0..i) + nums[i] = Σ nums[0..i+1).
For best: if i = 0 then best is None, the guard fires, and
best′ = nums[0] = max nums[0..1). If i > 0 then best = max nums[0..i) and
best′ = max(best, nums[i]) = max nums[0..i+1), since the maximum of a set
is the larger of the maximum of a part and the remaining element. Finally
i′ = i + 1, and i < n gives i′ ≤ n. So I holds again. ✓

*Sufficiency.* On exit ¬(i < n) with i ≤ n from I, so i = n. Substituting
into I gives total = Σ nums[0..n) and best = max nums[0..n) when n > 0,
None when n = 0. That is Q. ✓

*Termination.* Take V = n − i. I ∧ B gives i < n so V ≥ 1 > 0, and each
iteration decreases V by exactly 1. ∎

The proof also tells you the cost: V starts at n and drops by 1, so the
loop runs exactly n times — Θ(n).

### Proof 2 — exponentiation by squaring

    def power(b, e):                      # precondition: e ≥ 0
        result = 1
        base = b
        n = e
        while n > 0:
            if n % 2 == 1:
                result = result * base
            base = base * base
            n = n // 2
        return result

Goal Q: `result = b^e`.

Invariant I:  `n ≥ 0  ∧  result · base^n = b^e`.

This is the whole trick: the answer is not `result`, it is `result` times
the work still outstanding, and *that product* is what stays fixed.

*Establishment.* result = 1, base = b, n = e ≥ 0, and 1 · b^e = b^e. ✓

*Preservation.* Assume I ∧ n > 0. Let k = ⌊n/2⌋, so n = 2k or n = 2k+1,
and k ≥ 0.

- n even (n = 2k): result′ = result, base′ = base², n′ = k, and
  result′ · base′^n′ = result · (base²)^k = result · base^{2k}
  = result · base^n = b^e.
- n odd (n = 2k+1): result′ = result · base, base′ = base², n′ = k, and
  result′ · base′^n′ = result · base · base^{2k} = result · base^{2k+1}
  = result · base^n = b^e.

Either way I is restored. ✓

*Sufficiency.* On exit n = 0 (n ≥ 0 from I and ¬(n > 0)), so
result = result · base^0 = b^e = Q. ✓

*Termination.* V = n. I ∧ B gives n ≥ 1, and n′ = ⌊n/2⌋ ≤ n/2 < n with
n′ ≥ 0. Strictly decreasing in ℕ, so the loop halts. Moreover n at least
halves each pass, so it runs ⌊log₂ e⌋ + 1 times — Θ(log e) multiplications
instead of Θ(e). ∎

### Proof 3 — Euclid's algorithm, and why the variant is the point

    def gcd(a, b):                        # precondition: a ≥ 0, b ≥ 0, not both 0
        while b != 0:
            a, b = b, a % b
        return a

Invariant I: `gcd(a, b) = gcd(a₀, b₀) ∧ a ≥ 0 ∧ b ≥ 0`.

*Preservation* rests on a lemma: for b > 0, gcd(a, b) = gcd(b, a mod b).
Proof: write a = qb + r with r = a mod b. If d divides b and r, it divides
qb + r = a, so d is a common divisor of a and b. Conversely if d divides a
and b, it divides a − qb = r. The two pairs therefore have the *same* set
of common divisors, hence the same greatest one. ∎ The simultaneous
assignment `a, b = b, a % b` evaluates the whole right side first, so it
performs exactly this substitution.

*Sufficiency.* On exit b = 0, and gcd(a, 0) = a for a > 0. So the returned
a is gcd(a₀, b₀). ✓

*Termination.* V = b. When b > 0, `a % b` lies in [0, b) by the floor law
of lesson 01, so b′ < b and b′ ≥ 0. ∎ Notice that termination here is not
obvious from the code — it is a consequence of a property of `%`. That is
the normal situation: **the variant is where the real argument lives.**

### `for` is a `while` in disguise

    for x in it: BODY

means: get an iterator from `it`, then repeatedly ask it for the next
element until it signals exhaustion. Two consequences worth having now.
First, the loop variable is an ordinary local name that survives the loop
and is *not* restored afterwards. Second, mutating a list while iterating
over it changes what the iterator sees:

```python
xs = [1, 2, 3, 4]
for x in xs:
    if x % 2 == 0:
        xs.remove(x)      # BUG: skips elements; the index keeps advancing
```

Iterate over a copy (`for x in xs[:]`) or build a new list. Lesson 08
gives the iterator protocol properly.

### Why `else` on a loop is the search postcondition

A search loop has two exits, and they have different postconditions:

- exited by `break`: ∃ i < n. found(a[i]) — and `i` is a witness.
- exited normally: ∀ i < n. ¬found(a[i]).

The `else` clause is the second postcondition, given a syntax. The
alternative — a `found = False` flag — forces you to carry the flag in the
invariant instead, which is strictly more to prove.

## Worked examples

```python
>>> n = 100
>>> total = 0
>>> for i in range(1, n + 1):     # invariant: total = Σ 1..i-1
...     total += i
>>> total, n * (n + 1) // 2
(5050, 5050)
```

Linear search with `for/else`:

```python
def index_of(xs, target):
    for i in range(len(xs)):        # invariant: target ∉ xs[0..i)
        if xs[i] == target:
            return i                # witness
    return -1                       # ∀ i < n. xs[i] != target
```

Digit loop (the variant is `n`, which shrinks by a factor of 10):

```python
>>> n, out = 9051, 0
>>> while n > 0:                  # invariant: out·10^k + n = 9051 reversed-so-far
...     out = out * 10 + n % 10
...     n //= 10
>>> out
1509
```

Collatz — a loop whose termination nobody can prove:

```python
def collatz_steps(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps
```

There is no known variant. The invariant (`steps` counts the applications
so far) is easy; the termination obligation is an open problem in number
theory. This is a useful reminder that obligation 4 is a real obligation
and not a formality.

## Exercises

Open `exercises/02_control_flow.py`; run `python3 -m pytest exercises/02_control_flow.py`.

- `sum_and_max(nums)` — one pass, the prefix invariant of Proof 1.
- `power(base, exp)` — exponentiation by squaring, the invariant of Proof 2.
- `gcd(a, b)` — Euclid; state the variant.
- `first_index_of(xs, target)` — linear search with `for/else`.
- `is_prime(n)` — trial division to ⌊√n⌋, `break` and loop-`else`.
- `fizzbuzz(n)` — the `elif` chain, order matters.
- `collatz_steps(n)` — a `while` with an unproven variant.

## LeetCode

- 9 Palindrome Number — reverse half the digits; invariant on the two halves.
- 69 Sqrt(x) — integer square root by loop; invariant `r² ≤ x`.
- 50 Pow(x, n) — exactly Proof 2, plus the negative-exponent case.
- 412 Fizz Buzz — branch ordering.
- 202 Happy Number — loop with a termination argument you must supply.
- 268 Missing Number — sum invariant, Σ 0..n minus the observed sum.
- 1342 Number of Steps to Reduce a Number to Zero — variant is the number itself.
- 1512 Number of Good Pairs — nested loops; count over a prefix.

## Next

Lesson 3 replaces the loop with the recursive call, and the invariant with
the induction hypothesis. They are the same discipline.
