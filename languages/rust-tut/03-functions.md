# 03. Functions, Recursion, and Induction

## Concept

```rust
pub fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 { a } else { gcd(b, a % b) }
}
```

- `fn name(param: Type, …) -> Ret { body }`.
- Parameter types and the return type are **mandatory**. Inference works
  inside a function body, never across its signature. That is deliberate: the
  signature is the contract, and a contract you have to infer is not one.
- The value is the final expression, no semicolon. `return e;` exists for
  early exit; using it as the last line is unidiomatic but not wrong.
- No overloading, no default arguments, no varargs. One name, one signature.
- `pub` makes the item visible outside its module. Without it, a function is
  private to the module and its children.

Parameters are patterns, so destructuring works:

```rust
fn dist((x1, y1): (f64, f64), (x2, y2): (f64, f64)) -> f64 {
    ((x2 - x1).powi(2) + (y2 - y1).powi(2)).sqrt()
}
```

A parameter can be `mut`, which says the *local binding* is mutable. It says
nothing to the caller — the caller already gave the value away:

```rust
pub fn shout(mut s: String) -> String { s.push('!'); s }
```

Functions returning nothing return `()` and may omit `-> ()`. Diverging
functions (`panic!`, infinite `loop`) have type `!`, which coerces to
anything — that is why `let x: i32 = if c { 1 } else { panic!() };` compiles.

### `const fn`

A `const fn` can be evaluated by the compiler when its arguments are
constants, so its result can appear where a constant is required — array
lengths, `const` items, enum discriminants.

```rust
const fn kib(n: usize) -> usize { n * 1024 }
const BUF: usize = kib(4);
static ARR: [u8; kib(1)] = [0; kib(1)];
```

`const fn` is a *superset* capability, not a restriction on callers: the same
function is callable normally at run time. Inside one, you are limited to
what the const evaluator supports (no heap allocation, no trait methods
outside a growing allowed set). Marking a function `const` is a public API
promise; add it when it is genuinely useful, not reflexively.

## Why

### Recursion and induction are one idea

A recursive definition and an inductive proof have the same shape, because
they are the same object read in two directions. A recursive function is
correct when:

1. **Base case.** It is correct on the inputs where it does not recurse.
2. **Inductive step.** Assuming it is correct on every input *smaller* in
   some well-founded order, it is correct on the current input.

"Well-founded" means the order has no infinite descending chain — so the
recursion cannot go forever. That is the termination obligation, and it is
the exact analogue of lesson 2's decreasing variant.

The practical consequence: you may *assume the recursive call works*. Do not
trace it. Tracing a recursion two levels deep is how people convince
themselves correct code is wrong.

### Proof 1: `fact`, ordinary induction

```rust
pub fn fact(n: u64) -> u64 { if n == 0 { 1 } else { n * fact(n - 1) } }
```

Spec: for n ≥ 0, `fact(n)` = n! = Π_{j=1..n} j (empty product = 1).

*Base.* n = 0: returns 1 = 0!. ✓

*Step.* Let n > 0 and assume `fact(n−1)` = (n−1)!. The call returns
n · fact(n−1) = n · (n−1)! = n!. ✓

By induction the spec holds for all n ≥ 0. *Termination:* variant n, a
natural number strictly decreasing at each call, so the chain is finite. ∎

*Cost.* n multiplications, and n stack frames — O(n) time, O(n) space. The
space is the part people forget, and lesson 2's `for` version uses O(1).

*Overflow.* 21! exceeds `u64::MAX`, so `fact(21)` panics in debug and wraps
in release. The proof above is about ℕ; the code is about ℤ/2^64. Whenever
those diverge, the proof is a statement about the intended domain and you owe
a separate argument that the inputs stay inside it. Here: correct for n ≤ 20.

### Proof 2: `pow_mod`, strong induction

```rust
pub fn pow_mod(base: u64, exp: u64, m: u64) -> u64 {
    if exp == 0 { return 1 % m; }
    let half = pow_mod(base, exp / 2, m);
    let sq = half * half % m;
    if exp % 2 == 1 { sq * (base % m) % m } else { sq }
}
```

Spec: `pow_mod(b, e, m)` = b^e mod m, for m ≥ 1.

*Base.* e = 0: returns 1 mod m, which is b^0 mod m (and correctly 0 when
m = 1). ✓

*Step.* Let e > 0 and assume the spec for every exponent < e — strong
induction, because the call is on ⌊e/2⌋, not e−1. Since e > 0, ⌊e/2⌋ < e, so
the hypothesis applies and half = b^⌊e/2⌋ mod m. Then

    sq = (b^⌊e/2⌋ mod m)² mod m = b^(2⌊e/2⌋) mod m

using (x mod m)² ≡ x² (mod m). Now split on parity:

- e even: e = 2⌊e/2⌋, so sq = b^e mod m. ✓
- e odd: e = 2⌊e/2⌋ + 1, and the code returns
  sq · (b mod m) mod m = b^(2⌊e/2⌋) · b mod m = b^e mod m. ✓ ∎

*Termination.* Variant e; each call halves it and ⌊e/2⌋ < e for e > 0, so the
depth is ⌊log₂ e⌋ + 1. Cost O(log e) time and stack. This is the routine
every "answer modulo 1e9+7" problem needs.

*Overflow, again as a separate obligation.* `half * half` is a `u64`
multiplication of two values < m. It is exact iff m² < 2^64, i.e.
m < 2^32 ≈ 4.29e9. For m = 1_000_000_007 that holds. For larger moduli you
need `u128`. The proof is silent on this; you are not.

### Proof 3: `gcd`, well-founded induction on a non-obvious order

```rust
pub fn gcd(a: u64, b: u64) -> u64 { if b == 0 { a } else { gcd(b, a % b) } }
```

Spec: returns gcd(a, b), with the convention gcd(a, 0) = a.

*Key lemma.* For b > 0, gcd(a, b) = gcd(b, a mod b). Proof: write
a = qb + r with r = a mod b. If d divides b and r, then d divides qb + r = a,
so d is a common divisor of a and b. Conversely if d divides a and b then d
divides a − qb = r. The two pairs therefore have the *same set* of common
divisors, hence the same greatest one. ∎

*Base.* b = 0: returns a = gcd(a, 0). ✓

*Step.* b > 0. Assume the spec for every pair whose second component is
smaller than b. Since 0 ≤ a mod b < b, the pair (b, a mod b) qualifies, so
the call returns gcd(b, a mod b), which equals gcd(a, b) by the lemma. ✓ ∎

*Termination.* Variant: the second argument, strictly decreasing in ℕ because
a mod b < b. Cost: O(log min(a,b)) calls — the worst case is consecutive
Fibonacci numbers (Lamé's theorem).

### Proof 4: `sum_rec`, structural induction

```rust
pub fn sum_rec(xs: &[i64]) -> i64 {
    match xs {
        [] => 0,
        [x, rest @ ..] => x + sum_rec(rest),
    }
}
```

Here the order is "shorter slice", and the induction is on the *structure* of
the data rather than on a number. `[x, rest @ ..]` is a slice pattern: bind
the first element to `x`, the remaining subslice to `rest`.

*Base.* Empty slice: returns 0, the empty sum. ✓

*Step.* Slice of length n > 0, say x followed by rest of length n−1. Assume
the spec for all shorter slices; then `sum_rec(rest)` = Σ rest, and the call
returns x + Σ rest = Σ xs. ✓ ∎

*Termination.* Variant `xs.len()`, decreasing by 1 per call.

Every recursive data type comes with its own induction principle — lesson 11
does trees the same way, with two recursive calls and two hypotheses.

### Termination in a lexicographic order: `ackermann`

```rust
pub fn ackermann(m: u64, n: u64) -> u64 {
    match (m, n) {
        (0, n) => n + 1,
        (m, 0) => ackermann(m - 1, 1),
        (m, n) => ackermann(m - 1, ackermann(m, n - 1)),
    }
}
```

No single argument decreases: the third arm calls `ackermann(m, n-1)` with m
unchanged, and `ackermann(m-1, …)` with a *larger* second argument. The
variant is the **pair** (m, n) ordered lexicographically: (m', n') < (m, n)
iff m' < m, or m' = m and n' < n. That order on ℕ² is well-founded (an
infinite descent would need an infinite descent in the first component, or
eventually a fixed first component and an infinite descent in the second).

Check each arm: `(m-1, 1)` has smaller first component ✓; the inner
`(m, n-1)` has equal first and smaller second ✓; the outer `(m-1, _)` has
smaller first ✓. So the recursion terminates. Its *value* grows faster than
any primitive recursive function — `ackermann(4, 2)` has 19729 digits, and
the test stops at (3, 3) = 61 for good reason.

### Why Rust does not guarantee tail-call optimization

`fact_acc(n, acc) = fact_acc(n − 1, acc * n)` is *tail recursive*: the
recursive call is the entire body of its branch, so the caller's frame has no
work left and could in principle be reused. Scheme and OCaml guarantee that
reuse; Rust does **not**, and it is not an oversight:

1. **Destructors.** A frame holding an owned value must run `Drop` at scope
   exit (lesson 4). That drop is work scheduled *after* the tail call, so the
   call is not in tail position after all. LLVM can only elide the frame when
   it can prove no drops remain — which it sometimes can, and sometimes
   cannot, unpredictably.
2. **Unwinding and stack maps.** Panics unwind by walking frames; guaranteed
   TCO would have to interact with that machinery.
3. **A guarantee must be honored on every backend and every opt level.** Rust
   is unwilling to promise something that `-O0` cannot deliver.

So: LLVM *often* turns tail recursion into a loop in release builds, and
essentially never in debug. `cargo test` runs debug. Consequences you must
plan around:

- **Recursion depth is bounded by the actual stack**, typically 8 MiB on the
  main thread and 2 MiB on spawned threads. A frame of a few dozen bytes gets
  you O(10^5) deep; deeper overflows.
- **Stack overflow is not a catchable panic.** It aborts the process with
  `thread '…' has overflowed its stack` (SIGSEGV caught by a guard page).
  There is no `Result` to handle.
- Therefore: recursion depth proportional to input size is only acceptable
  when the input is bounded, or the depth is logarithmic. `sum_rec` on a
  million-element slice will crash; the balanced-tree recursions in lesson 11
  are depth O(log n) and are fine. When depth is O(n) and n is large,
  convert to an explicit loop with your own `Vec` as a stack — the heap is
  much larger than the stack, and `Vec` growth is a `Result`-shaped failure
  rather than an abort.

The accumulator form is still worth writing, not for the compiler but for
you: `fact_acc(n, acc)` has the clean invariant `acc · n! = the answer`,
which is exactly the loop invariant of its iterative twin. Tail-recursive
functions and `while` loops are transcriptions of each other.

## Worked examples

```rust
// Iteration where the recursion would be exponential
pub fn fib(n: u32) -> u64 {
    let (mut a, mut b) = (0u64, 1u64);
    for _ in 0..n { let next = a + b; a = b; b = next; }
    a
}
assert_eq!(fib(10), 55);
assert_eq!(fib(90), 2880067194370816120);   // fib(94) overflows u64
```

The naive two-call `fib` makes T(n) = T(n−1) + T(n−2) + O(1) calls, i.e.
Θ(φ^n) with φ = (1+√5)/2. The loop is O(n) with the invariant
`(a, b) = (fib(i), fib(i+1))` after i iterations — prove it exactly as in
lesson 2.

```rust
// Accumulator form ↔ loop
assert_eq!(fact_acc(5, 1), 120);
assert_eq!(fact_acc(0, 7), 7);      // acc · 0! = acc

// Structural recursion over chars: reverse_rec
pub fn reverse_rec(s: &str) -> String {
    let mut it = s.chars();
    match it.next() {
        None => String::new(),
        Some(c) => { let mut r = reverse_rec(it.as_str()); r.push(c); r }
    }
}
assert_eq!(reverse_rec("héllo"), "olléh");   // chars, not bytes
```

`it.as_str()` is the rest of the string *after* the char just taken — the
right way to peel a UTF-8 string, since `&s[1..]` may split a code point and
panic.

```rust
// Modular exponentiation, the workhorse
assert_eq!(pow_mod(2, 10, 1000), 24);              // 1024 mod 1000
assert_eq!(pow_mod(7, 1_000_000, 1_000_000_007), 880007888);
assert_eq!(pow_mod(5, 3, 1), 0);                   // everything mod 1 is 0

// const fn: evaluated at compile time here, at run time elsewhere
const fn square(x: usize) -> usize { x * x }
const N: usize = square(4);
let arr = [0u8; square(4)];
assert_eq!(arr.len(), N);
```

## Exercises

Open `exercises/src/l03_functions.rs`; run

    cd rust && cargo test -p exercises l03

For each recursive function, write the base case, the inductive hypothesis,
and the variant in a comment above it.

- `fact(n)` — direct recursion; note where it overflows.
- `fib(n)` — iterative, O(n); do not write the exponential version.
- `pow_mod(b, e, m)` — halve the exponent; watch `half * half` overflow.
- `gcd(a, b)` — Euclid; both `gcd(0, 9)` and `gcd(9, 0)` are 9.
- `sum_rec(xs)` — slice patterns `[]` and `[x, rest @ ..]`.
- `reverse_rec(s)` — `chars()`, `next()`, `as_str()`; the test uses `é`.
- `fact_acc(n, acc)` — tail shape; state the invariant it encodes.
- `ackermann(m, n)` — lexicographic variant; do not try (4, 2).

## LeetCode

- 50 Pow(x, n) — same halving as `pow_mod`, over f64, with n possibly
  `i32::MIN` (negating it overflows — use `i64` or `unsigned_abs`).
- 70 Climbing Stairs — Fibonacci in disguise; write the O(n) loop.
- 509 Fibonacci Number — the exponential version is the trap.
- 1137 N-th Tribonacci Number — three-term version of the same loop.
- 231 Power of Two / 342 Power of Four — recursion or one bit trick.
- 1979 Find Greatest Common Divisor of Array — `gcd` folded over a slice.
- 344 Reverse String — do it recursively, then note the O(n) stack depth and
  why the iterative two-pointer version is the one to submit.

## Next

Lesson 4 is where Rust stops resembling other languages: ownership, and the
proof that it makes double-free and use-after-free impossible.
