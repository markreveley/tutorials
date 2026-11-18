# 02. Control Flow and Loop Invariants

## Concept

### `if` is an expression

```rust
let parity = if n % 2 == 0 { "even" } else { "odd" };
```

Both arms must have the same type. There is no truthiness: the condition
must be `bool`. `if x` where `x: i32` is `error[E0308]`. No parentheses are
needed around the condition; braces are never optional.

An `if` with no `else` has type `()`, so it can only be used as a statement.

### Three loops

```rust
loop { ... }              // forever, until break
while cond { ... }        // test first
for x in iterable { ... }  // over anything IntoIterator
```

Rust has no C-style `for (i = 0; i < n; i++)`. Ranges take its place:

```rust
for i in 0..n     { }     // half-open: 0, 1, …, n−1
for i in 0..=n    { }     // inclusive: 0, 1, …, n
for i in (0..n).rev() { } // n−1 down to 0
for i in (0..n).step_by(2) { }
for (i, &x) in xs.iter().enumerate() { }   // index and element
```

`0..n` is a *value* of type `Range<usize>` that happens to be an iterator;
it is not syntax. That is why `.rev()`, `.step_by()`, `.zip()` compose on it.

### `break` with a value

`loop` is an expression, and `break e` supplies its value. `while` and `for`
cannot do this (they may exit without ever reaching a `break`, so there
would be no value), and always have type `()`.

```rust
let k = loop {
    if p >= n { break k; }
    p *= 2;
    k += 1;
};
```

### Labels

Labels are `'name:` on a loop, and `break 'name` / `continue 'name` target
it. Without a label, `break` and `continue` bind to the innermost loop.

```rust
'outer: for p in 2..n {
    let mut d = 2;
    while d * d <= p {
        if p % d == 0 { continue 'outer; }   // p is composite: next p
        d += 1;
    }
    count += 1;                              // reached only if p is prime
}
```

This is the structured replacement for `goto`, and the reason the "found a
divisor" flag variable that C code needs does not appear here.

### `match` basics

`match` compares a scrutinee against patterns, top to bottom, and is an
expression. It must be **exhaustive** — the compiler proves that some arm
matches every possible value, or rejects the program.

```rust
match (n % 3, n % 5) {
    (0, 0) => "FizzBuzz".to_string(),
    (0, _) => "Fizz".to_string(),
    (_, 0) => "Buzz".to_string(),
    _      => n.to_string(),
}
```

`_` is the wildcard. Patterns can also be ranges and can carry guards:

```rust
match ch {
    'a'..='z' => "lower",
    '0'..='9' => "digit",
    c if c.is_whitespace() => "space",
    _ => "other",
}
```

Order matters: the first matching arm wins, so `(0, 0)` must precede
`(0, _)`. Exhaustiveness is checked, but *unreachability* is only a warning.

## Why

### The proof discipline: Hoare triples

Write `{P} S {Q}` for: if P holds before statement S runs, and S terminates,
then Q holds after. This is *partial* correctness; termination is a separate
obligation.

The rule for `while` is the only one that needs an idea:

        {I ∧ c} body {I}
    ─────────────────────────
    {I} while c { body } {I ∧ ¬c}

Read it as: if the loop body preserves I whenever it runs, then the loop
preserves I, and on exit you additionally know the guard is false. I is the
**loop invariant**. To use the rule you must supply three things:

1. **Initialization** — I holds when control first reaches the loop.
2. **Preservation** — `{I ∧ c} body {I}`.
3. **Exit** — `I ∧ ¬c ⇒ Q`, the postcondition you actually wanted.

For termination, supply a fourth: a **variant**, an expression V mapping the
state into a well-founded order (usually ℕ) such that every iteration
strictly decreases V. A strictly decreasing sequence in ℕ is finite, so the
loop stops.

Writing loops in this order — pick I first, then write the body that
preserves it — is the difference between debugging off-by-ones and not
having them.

### Proof 1: `sum_to`

```rust
pub fn sum_to(n: u64) -> u64 {
    let mut acc = 0;
    for i in 1..=n { acc += i; }
    acc
}
```

Desugar the `for` into the loop the compiler builds, with `i` the value most
recently taken from the range and `i = 0` standing for "none taken yet".

Invariant **I: acc = i(i+1)/2**, where i is the last value consumed
(i = 0 before the first iteration).

*Initialization.* Before the loop, acc = 0 and i = 0; 0·1/2 = 0. I holds.

*Preservation.* Assume I and that the range yields a next value, which is
i+1 (the range is consecutive and starts at 1). The body sets
acc' = acc + (i+1) = i(i+1)/2 + (i+1) = (i+1)(i+2)/2, and i' = i+1, so
acc' = i'(i'+1)/2. I holds. ∎

*Exit.* The range is exhausted exactly when i = n (or immediately, when
n = 0, in which case i = 0 = n still). So on exit I ∧ (i = n) gives
acc = n(n+1)/2, which is the postcondition Q: the return value is Σ_{j=1..n} j.

*Termination.* Variant V = n − i. Each iteration increases i by 1, so V
strictly decreases, and I together with i ≤ n keeps V ≥ 0. Hence at most n
iterations. ∎

Cost: O(n) time, O(1) space. (The closed form `n*(n+1)/2` is O(1) — and note
that `n*(n+1)` can overflow `u64` for n near 2^32 while the loop's `acc`
would too. Neither is safe for arbitrary n; both are fine for the tests.)

### Proof 2: `ceil_log2`

```rust
pub fn ceil_log2(n: u64) -> u32 {
    let mut k = 0;
    let mut p: u64 = 1;
    loop {
        if p >= n { break k; }
        p *= 2;
        k += 1;
    }
}
```

Postcondition Q: the returned k is the least k ≥ 0 with 2^k ≥ n.

Invariant **I: p = 2^k ∧ (k = 0 ∨ 2^(k−1) < n)**.

The second conjunct is the interesting half: it records that we have not
overshot — every exponent we already passed was too small.

*Initialization.* k = 0, p = 1 = 2^0, and the disjunct k = 0 holds. I holds.

*Preservation.* Assume I and the guard's negation, i.e. p < n. The body sets
p' = 2p = 2·2^k = 2^(k+1) and k' = k+1, so p' = 2^k'. For the second
conjunct with k' ≥ 1 we must show 2^(k'−1) < n, i.e. 2^k < n; that is
exactly p < n, the loop condition we assumed. I holds. ∎

*Exit.* The loop leaves only via `break k`, taken when p ≥ n. With I this
gives 2^k ≥ n ∧ (k = 0 ∨ 2^(k−1) < n).

- If k = 0 then 2^0 = 1 ≥ n and no smaller exponent exists, so k is least.
- If k > 0 then 2^(k−1) < n, and 2^j is increasing in j, so for every j < k
  we have 2^j ≤ 2^(k−1) < n. No smaller exponent works. k is least.

Either way Q holds. ∎

*Termination.* Variant V = max(0, n − p). While the guard holds, p < n and
the body doubles p with p ≥ 1, so p strictly increases and V strictly
decreases; V ≥ 0 by construction. Since p at least doubles, the loop runs at
most ⌊log₂ n⌋ + 1 times. Cost: O(log n). ∎

*Edge case, checked against the proof rather than by running it:* n = 0.
Then p = 1 ≥ 0 on the first test, so the loop breaks immediately with k = 0,
and indeed 2^0 = 1 ≥ 0 and 0 is the least such k. The proof covers it
because nothing above assumed n > 0.

### Proof 3 (sketch, same discipline): `isqrt`

```rust
pub fn isqrt(n: u64) -> u64 {
    let mut r = 0u64;
    while (r + 1).checked_mul(r + 1).map_or(false, |sq| sq <= n) { r += 1; }
    r
}
```

Invariant **I: r² ≤ n**. Initialization: 0 ≤ n. ✓ Preservation: the guard
says (r+1)² ≤ n, so after `r += 1` the invariant is literally the guard. ✓
Exit: the guard is false, so (r+1)² > n (or (r+1)² overflows `u64`, which
also implies (r+1)² > n since n : u64). With I: r² ≤ n < (r+1)², which is
the definition of ⌊√n⌋. ✓ Termination: variant n − r; each iteration
increments r, and I gives r ≤ r² ≤ n for r ≥ 1, so n − r ≥ 0. ∎

Cost O(√n) — worth noting, because binary search on the same invariant gets
O(log n) and lesson 11 will ask you to do exactly that.

### When you cannot supply a variant: `collatz_steps`

```rust
while n != 1 { n = if n % 2 == 0 { n / 2 } else { 3 * n + 1 }; steps += 1; }
```

There is a perfectly good invariant (`steps` = number of steps taken so far
from the original n, and n is the current term), so partial correctness is
easy. There is **no known variant**: whether this loop terminates for every
starting n is the Collatz conjecture, open since 1937. This is the honest
shape of the situation — partial correctness and termination really are two
obligations, and here only one is dischargeable.

Practical note: `3 * n + 1` on a `u64` can overflow for large n, which would
panic in debug. The tests stay small.

### Why exhaustiveness matters

`match` being exhaustive is the same proof-obligation idea as lesson 01's
types. The compiler checks that the arms cover the scrutinee's type, so a
`match` can never "fall through to nothing" and there is no need for a
run-time default that silently does the wrong thing. When lesson 07
introduces `enum`, this becomes the tool that makes adding a variant a
compile error at every place that must be updated — the single most useful
refactoring property Rust has.

## Worked examples

```rust
// if as an expression, both arms same type
let n = 7;
assert_eq!(if n % 2 == 0 { "even" } else { "odd" }, "odd");

// loop with break value
let mut p = 1u64; let mut k = 0;
let k = loop { if p >= 1000 { break k; } p *= 2; k += 1; };
assert_eq!(k, 10);           // 2^10 = 1024 ≥ 1000

// ranges
assert_eq!((0..5).sum::<i32>(), 10);
assert_eq!((0..=5).sum::<i32>(), 15);
assert_eq!((0..5).rev().collect::<Vec<_>>(), vec![4, 3, 2, 1, 0]);

// enumerate: the loop behind linear_search
let xs = [4, 2, 9];
let mut found = None;
for (i, &x) in xs.iter().enumerate() {
    if x == 9 { found = Some(i); break; }
}
assert_eq!(found, Some(2));

// labeled continue
let mut count = 0;
'outer: for p in 2..20u32 {
    let mut d = 2;
    while d * d <= p { if p % d == 0 { continue 'outer; } d += 1; }
    count += 1;
}
assert_eq!(count, 8);        // 2 3 5 7 11 13 17 19

// match on a tuple; order matters
let f = |n: u32| match (n % 3, n % 5) {
    (0, 0) => "FizzBuzz".to_string(),
    (0, _) => "Fizz".to_string(),
    (_, 0) => "Buzz".to_string(),
    _      => n.to_string(),
};
assert_eq!((f(15), f(9), f(10), f(7)), ("FizzBuzz".into(), "Fizz".into(), "Buzz".into(), "7".into()));

// match with ranges and a guard
let classify = |c: char| match c {
    'a'..='z' => "lower",
    '0'..='9' => "digit",
    c if c.is_whitespace() => "space",
    _ => "other",
};
assert_eq!((classify('q'), classify('4'), classify(' '), classify('!')),
           ("lower", "digit", "space", "other"));
```

## Exercises

Open `exercises/src/l02_control_flow.rs`; run

    cd rust && cargo test -p exercises l02

For each loop, write the invariant in a comment *before* the body.

- `sum_to(n)` — `for` over `1..=n`; invariant proved above.
- `collatz_steps(n)` — `while`; partial correctness only.
- `ceil_log2(n)` — `loop` with `break k`; check n = 0 and n = 1.
- `fizzbuzz(n)` — `match` on `(n % 3, n % 5)`; mind the arm order.
- `linear_search(xs, t)` — invariant: no element in `xs[0..i)` equals t.
- `isqrt(n)` — invariant r² ≤ n; use `checked_mul` so the guard cannot panic.
- `count_primes(n)` — nested loops and a labeled `continue`; the inner bound
  is `d * d <= p`, which is the whole reason this is O(n√n) and not O(n²).

## LeetCode

- 1 Two Sum — the O(n²) double loop is fine now; state the invariant.
- 66 Plus One — carry loop over a digit array, backwards.
- 121 Best Time to Buy and Sell Stock — one pass; invariant: `min_so_far`
  is the minimum of the prefix, `best` the best profit ending in the prefix.
- 169 Majority Element — Boyer–Moore; the invariant is the interesting part.
- 204 Count Primes — exactly `count_primes`, then improve it to a sieve.
- 283 Move Zeroes — two indices, invariant on `a[0..w)` and `a[w..r)`.
- 344 Reverse String — two indices moving inward; invariant: the outside is
  already swapped.
- 704 Binary Search — do it now with the invariant
  `target ∈ a ⇒ target ∈ a[lo..hi)`, and prove the variant `hi − lo`
  decreases every iteration. Lesson 11 revisits it.

## Next

Lesson 3 turns loops inside out: recursion, and the induction proofs that
justify it.
