# 01. Values, Types, and Expressions

## Concept

Rust's scalar types are fixed-width and named for their width.

```rust
let a: i32 = -42;        // signed, 32 bits, range −2^31 .. 2^31−1
let b: i64 = 9_000_000;  // signed, 64 bits; _ is a digit separator
let c: u32 = 42;         // unsigned, 32 bits, 0 .. 2^32−1
let d: usize = 7;        // unsigned, pointer-width (64 on this machine)
let e: f64 = 3.14;       // IEEE-754 double
let f: bool = true;      // exactly true or false, 1 byte
let g: char = 'é';       // ONE Unicode scalar value, 4 bytes
```

`usize` is the index type: `Vec::len` returns it, and `v[i]` requires it.
Use `usize` for lengths and indices, `i64`/`u64` for arithmetic that must not
overflow, `i32` when a problem statement says the values fit in 32 bits.

The default when inference has no other constraint is `i32` for integers and
`f64` for floats.

```rust
let n = 5;          // i32
let x = 5.0;        // f64
let m = 5u64;       // suffix pins the type
let k: u8 = 5;      // annotation pins it
```

There are no implicit numeric conversions. Ever. `as` converts explicitly and
truncates without complaint:

```rust
let big: u64 = 300;
let small = big as u8;      // 44 — 300 mod 256; `as` never panics, never warns
let w: u32 = 4;
let area = w as u64 * 100;  // widen BEFORE multiplying, not after
```

### Expressions vs statements

Rust is an expression language. Almost everything produces a value; the
things that do not are *statements*, and there are only two kinds: `let`
declarations and expressions followed by `;`. The semicolon is an operator
that throws a value away and yields `()`, the empty tuple.

```rust
let y = { let t = 3; t * t };   // a BLOCK is an expression: y == 9
let z = if y > 5 { "big" } else { "small" };   // if is an expression
```

A function's return value is its final expression, with no semicolon:

```rust
fn max_expr(a: i32, b: i32) -> i32 {
    if a > b { a } else { b }       // no semicolon, no `return`
}
```

Add a semicolon there and the block's value becomes `()`, and you get
`error[E0308]: mismatched types — expected i32, found ()`. That error means
"you threw the answer away", and it is the single most common beginner
mistake.

### let, mutability, shadowing

`let` binds. Bindings are immutable unless declared `mut`.

```rust
let x = 5;
x = 6;                  // error[E0384]: cannot assign twice to immutable `x`

let mut y = 5;
y = 6;                  // fine

let s = "5";
let s: i32 = s.parse().unwrap();   // SHADOWING: a new binding, new type
```

Shadowing is not mutation. `let s = …` a second time creates a *different*
variable that happens to reuse the name; the old one still exists (something
may still be borrowing it) and may have a different type. Mutation with `mut`
cannot change the type. Prefer shadowing when a value is being transformed
once; prefer `mut` when a value is genuinely being updated in a loop.

### Tuples and arrays

```rust
let p: (i32, f64, char) = (1, 2.0, 'c');
let (a, b, _) = p;              // destructuring
let first = p.0;                // field access by index

let arr: [i32; 4] = [1, 2, 3, 4];   // length is part of the TYPE
let zeros = [0u8; 16];              // 16 zero bytes
let n = arr.len();                  // 4, known at compile time
let s: &[i32] = &arr[1..3];         // a slice: [2, 3]
```

`[i32; 4]` and `[i32; 5]` are different types. That is what lets an array
live on the stack with no length word: the length is in the type, not in the
value. A *slice* `&[i32]` is a pointer plus a run-time length, and is how you
pass "some run of elements" to a function.

The unit type `()` has exactly one value, also written `()`. A function with
no `-> T` returns `()`.

## Why

### Static types as a proof obligation discharged early

A type is a proposition about a value: `x : u32` asserts "x is a natural
number below 2^32". A type *checker* is a proof checker: it verifies, once,
that every operation in the program is applied to arguments satisfying its
precondition. What is checked statically never needs checking again at run
time — which is exactly why `a + b` on two `u32`s compiles to one machine
instruction with no tag test, no dispatch, no `isinstance`.

Compare the dynamic discipline. In Python `a + b` must, at every execution,
ask what `a` and `b` are. That is a run-time cost paid on every iteration
forever, in exchange for deferring the obligation. Rust's trade is the
opposite: pay the proof once, at compile time, and run with no residue.

The obligation is real, and it is *yours*: when the checker rejects your
program it is telling you the proposition you asserted does not follow. The
error `expected u64, found u32` on

```rust
fn area(w: u32, h: u32) -> u64 { w * h }        // WRONG
```

is not pedantry. `w * h` at type `u32` can overflow; widening the *result*
of a `u32` multiplication does not recover the lost bits. The fix widens the
operands, so the multiplication itself happens at `u64`:

```rust
fn area(w: u32, h: u32) -> u64 { w as u64 * h as u64 }
```

The type system forced you to notice a real bug. That is the whole point.

### Why integer overflow is defined in Rust and undefined in C

In C, signed overflow is **undefined behavior**: the standard imposes no
requirement at all, so a compiler may assume it never happens. That
assumption is not idle — it licenses transformations like rewriting
`x + 1 > x` to `true` and deleting the loop-bound check that depended on it.
Real CVEs come from exactly this.

Why did C choose UB? Because in 1989 target machines disagreed: some
trapped on overflow, some wrapped two's-complement, some wrapped
ones'-complement. Defining one behavior would have forced a check or a
fixup on the machines that did the other thing. UB was the price of "no
cost on any target".

Rust rejects that trade because the cost is now negligible and the safety
value is large. Rust's rule:

- Arithmetic overflow is **not** undefined. It is always one of two defined
  behaviors, chosen by the `overflow-checks` flag.
- Debug builds (`cargo test`, `cargo build`): overflow **panics**.
- Release builds (`cargo build --release`): overflow **wraps** two's
  complement, i.e. the result is the true value reduced mod 2^n.

Both are defined. Neither licenses the compiler to assume anything. The
split exists because a panic is the right development-time signal and an
unconditional check is not always affordable in a hot release loop.

This means **`a + b` is not the operation you want when overflow is
possible and meaningful.** Say what you mean with an explicit method, and
then the behavior no longer depends on the build profile:

```rust
a.wrapping_add(b)      // (a + b) mod 2^n            — never panics
a.checked_add(b)       // Option<T>: None on overflow — you handle it
a.saturating_add(b)    // clamps at T::MAX / T::MIN
a.overflowing_add(b)   // (wrapped result, bool did_overflow)
```

with `_sub`, `_mul`, `_neg`, `_pow` variants. `u8::saturating_sub` is how you
write `max(a − b, 0)` for unsigned types without ever going negative — the
naive `if a > b { a - b } else { 0 }` is correct but says less.

Corollary worth internalizing: a test that passes under `cargo test` can
still be wrong under `--release`, if it relies on the panic to catch a bug.
Wrapping silently is exactly the C-like failure Rust is otherwise avoiding.
The defence is `checked_*` in code that must be right.

### Why floats are a separate type with no implicit promotion

`f64` is a finite subset of the rationals, ~15.9 significant decimal digits,
and `f64` addition is not associative: `(0.1 + 0.2) + 0.3 ≠ 0.1 + (0.2 + 0.3)`.
Integers are exact. Mixing them silently would make the *type* of a result
depend on a value somewhere far away, so Rust makes every crossing explicit
(`x as f64`, `y as i64`). Consequences:

- Never test floats with `==`. Test `(a - b).abs() < 1e-9`.
- `f64` does not implement `Ord`, only `PartialOrd`, because `NaN` breaks
  totality: `NaN < x`, `NaN > x`, and `NaN == x` are all false. So
  `vec_of_f64.sort()` does not compile; `sort_by(|a, b| a.partial_cmp(b).unwrap())`
  does, and tells you where the assumption lives.

### Why `char` is 4 bytes and strings are not arrays of it

`char` is a Unicode *scalar value* (U+0000..U+D7FF and U+E000..U+10FFFF), so
it needs 21 bits, rounded to 4. A `String` is UTF-8 bytes, where a scalar
value occupies 1 to 4 bytes, so `s[3]` is not defined — index 3 might land
mid-character. `s.chars()` decodes; `s.len()` counts *bytes*. Lesson 09
returns to this; for now: `"héllo".len() == 6`, `"héllo".chars().count() == 5`.

## Worked examples

```rust
// Expression-ness
let grade = { let score = 87; if score >= 90 { 'A' } else { 'B' } };
assert_eq!(grade, 'B');

// Shadowing changes the type; `mut` cannot
let spaces = "   ";
let spaces = spaces.len();          // now usize == 3
assert_eq!(spaces, 3);

// Widen before multiplying
let w: u32 = u32::MAX;
assert_eq!(w as u64 * w as u64, 18446744065119617025);

// Overflow, three ways
assert_eq!(u32::MAX.wrapping_add(1), 0);
assert_eq!(i32::MAX.checked_add(1), None);
assert_eq!(3u8.saturating_sub(10), 0);
assert_eq!(255u8.overflowing_add(1), (0, true));
// u32::MAX + 1  → panics in debug, is 0 in release

// Integer division truncates toward zero; % takes the sign of the dividend
assert_eq!(-7 / 2, -3);
assert_eq!(-7 % 2, -1);
assert_eq!((-7i32).rem_euclid(2), 1);   // use this for ring indexing

// Digit extraction, the loop behind digit_sum
let mut n = 1234u64;
let mut s = 0u32;
while n > 0 { s += (n % 10) as u32; n /= 10; }
assert_eq!(s, 10);

// Tuples and arrays
let (q, r) = (17 / 5, 17 % 5);
assert_eq!((q, r), (3, 2));
let arr = [1, 2, 3, 4];
assert_eq!(arr.iter().sum::<i32>(), 10);
assert_eq!(&arr[1..3], &[2, 3]);

// Limits are associated constants
assert_eq!(u8::MAX, 255);
assert_eq!(i32::MIN, -2147483648);
```

Note `-7 / 2 == -3` in Rust, but `-7 // 2 == -4` in Python: Rust truncates
toward zero (C's rule), Python floors. When you need Python's behavior — for
wrapping an index into a length-n buffer — use `rem_euclid`, which is the one
that returns a value in `0..n` for every input.

## Exercises

Open `exercises/src/l01_basics.rs`; run

    cd rust && cargo test -p exercises l01

- `area(w, h)` — widen before multiplying; the test uses `u32::MAX`.
- `c_to_f(c)` — float arithmetic; the test compares with a tolerance.
- `is_even(n)` — one expression, no `return`.
- `wrapping_sum(a, b)` — must not panic on `u32::MAX + 1`.
- `checked_sum(a, b)` — `Option<i32>`; note `i32::MIN.checked_add(-1)`.
- `sat_sub(a, b)` — unsigned, so `3 − 10` is `0`, not a panic.
- `digit_sum(n)` — `while` loop, shadowing `n` is fine.
- `max_expr(a, b)` — `if` as an expression.

## LeetCode

Modest and honest — you have arithmetic and `while` loops, nothing else.

- 7 Reverse Integer — the whole problem *is* checked arithmetic; use
  `checked_mul`/`checked_add` and return 0 on `None`.
- 9 Palindrome Number — `% 10` and `/ 10`, no string conversion.
- 231 Power of Two — one expression once you know `n & (n - 1)`.
- 258 Add Digits — the digit-sum loop, then the `(n − 1) % 9 + 1` shortcut.
- 263 Ugly Number — repeated `%` and `/`; watch the `n == 0` case.
- 1523 Count Odd Numbers in an Interval Range — pure integer division.

## Next

Lesson 2 adds loops and the discipline for proving them correct.
