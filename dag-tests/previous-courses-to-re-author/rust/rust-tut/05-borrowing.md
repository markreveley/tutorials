# 05. Borrowing

## Concept

Lesson 4 gave each value exactly one owner. That alone would make Rust
unusable: every function call would move its arguments away. **Borrowing** is
the escape hatch — temporary access to a value without taking ownership.

Two kinds of reference:

```rust
let s = String::from("hi");
let r: &String = &s;            // shared borrow  — read-only, copyable
let mut t = String::from("hi");
let m: &mut String = &mut t;    // mutable borrow — read/write, unique
```

Use them with `*` to dereference; `.` auto-dereferences.

```rust
fn len(s: &String) -> usize { s.len() }        // borrows, caller keeps s
fn push(s: &mut String) { s.push('!'); }       // borrows mutably

let mut s = String::from("a");
len(&s);                // s still owned here
push(&mut s);           // s == "a!"
```

`&[T]` and `&str` are *slices*: a borrowed view of a contiguous run of
elements (pointer + length). `&Vec<T>` coerces to `&[T]`, `&String` to `&str`.
Prefer slices in signatures — they accept more callers.

```rust
fn sum(xs: &[i32]) -> i32 { xs.iter().sum() }
sum(&vec![1, 2, 3]);
sum(&[1, 2, 3]);
sum(&vec![1, 2, 3][1..]);
```

The rules, informally: **you may have any number of `&T`, or exactly one
`&mut T`, but never both at once.**

## Why

### The rules as an inference system

Fix a *place* p (a variable, a field, an index — anything you can assign to).
A **loan** of p is a reference created from p; each loan is shared or mutable
and is *live* over the region of program points from its creation to its last
use. Write S(p) for the set of live shared loans of p and M(p) for the set of
live mutable loans, at a given program point.

    ───────────────────────────  (SHARED)
    M(p) = ∅
    ⊢ &p : &T,  add to S(p)

    ───────────────────────────  (MUT)
    p is declared `mut`,  S(p) = ∅,  M(p) = ∅
    ⊢ &mut p : &mut T,  add to M(p)

    ───────────────────────────  (READ)     reading p requires  M(p) = ∅
    ───────────────────────────  (WRITE)    writing or moving p requires  S(p) = ∅ ∧ M(p) = ∅

Loans of p also count as loans of everything p reaches: borrowing `v[0]`
borrows all of `v`, and borrowing `s.f` borrows `s` (though disjoint *fields*
of one struct are tracked separately).

By induction on the derivation, these four rules maintain one invariant at
every program point and for every place p:

> **Aliasing XOR Mutability.** Either |S(p)| ≥ 0 and |M(p)| = 0, or
> |S(p)| = 0 and |M(p)| = 1. Never both.

Proof: (SHARED) fires only when M(p) = ∅, so it can only grow the left
disjunct. (MUT) fires only when S(p) = M(p) = ∅, so it moves from the
"0 shared, 0 mutable" state to "0 shared, 1 mutable" and can never fire twice
without the first loan dying. Loans only leave the sets. ∎

Equivalently: **a reference through which you can write is a reference nobody
else holds.** This is why `&mut` is badly named. It is not "the mutable one";
it is *the exclusive one*. `&T` is the shared one. Mutability is a consequence
of exclusivity, not the point of it.

### What the invariant buys: iterator invalidation

In C++, `for (auto x : v) v.push_back(x);` is undefined behaviour: `push_back`
may reallocate, and the loop's iterator then points into freed memory. In
Python the analogous mutation silently skips elements.

Claim: this class of bug cannot typecheck in Rust.

Proof. Iterating `for x in &v` creates a shared loan of `v` that is live for
the whole loop body (the iterator holds it, and the iterator is used on every
iteration). Any operation that can reallocate — `push`, `insert`, `clear`,
`remove` — takes `&mut self`, so calling it applies rule (MUT) to `v`, which
requires S(v) = ∅. But the loop's loan is in S(v) and live. The premise fails;
the program is rejected. ∎

```rust
let mut v = vec![1, 2, 3];
for x in &v {
    v.push(*x);        // error[E0502]: cannot borrow `v` as mutable
}                      // because it is also borrowed as immutable
```

The same argument covers the general case: any reference that could dangle
because of a reallocation had to be derived from a shared loan, and the
reallocating call needs an exclusive one.

### What the invariant buys: data races

A **data race** is: two or more threads access the same memory location
concurrently, at least one access is a write, and the accesses are not
ordered by synchronization.

Claim: within safe Rust, no program with a data race typechecks.

Proof sketch. Consider a write to location p from thread A. By (WRITE) — or by
(MUT), if the write goes through a reference — thread A holds a `&mut` to p, or
owns p outright. By Aliasing XOR Mutability, |S(p)| = 0 and |M(p)| = 1 at that
point, so no other live reference to p exists *anywhere in the program*, and in
particular thread B holds none. Thread B therefore cannot access p at all,
let alone concurrently. If instead the write is preceded by the value being
shared, the sharing had to end (the loan died) before (MUT) could fire, and
the mechanisms that hand a reference to another thread require the reference to
outlive the thread — checked by lifetimes (lesson 6) and the `Send`/`Sync`
marker traits. ∎

The striking part is that the *same rule* that stops iterator invalidation in
single-threaded code stops data races in concurrent code. Rust did not add a
concurrency checker. Aliasing XOR mutability was already enough. This is what
"fearless concurrency" actually means.

### NLL: borrows end at last use

A loan is live from its creation to its **last use**, not to the end of the
enclosing scope. This is *non-lexical lifetimes* (NLL), stabilized in 2018.

```rust
let mut s = String::from("hi");
let r = &s;
println!("{r}");        // last use of r — the shared loan dies here
s.push('!');            // fine: S(s) = ∅ again
```

Without NLL the loan would live until the closing brace and this would be
rejected. With NLL, most borrow errors you actually hit are real ones.

### Reborrowing

Passing a `&mut T` to a function that wants a `&mut T` does not move it. The
compiler inserts a **reborrow**, `&mut *r`: a fresh, shorter loan derived from
`r`, during which `r` itself is frozen.

```rust
fn bump(x: &mut i32) { *x += 1; }

let mut n = 0;
let r = &mut n;
bump(r);        // reborrow: &mut *r, dies at end of call
bump(r);        // r is usable again — it was never moved
```

`&mut T` is not `Copy` (that would break exclusivity), so without reborrowing
the first call would consume `r`. Reborrowing is why `&mut` feels ergonomic
despite being a linear resource.

## Soundness vs completeness

A static checker for a nontrivial property must give up one of two things.
The borrow checker is **sound**: every program it accepts satisfies aliasing
XOR mutability. It is **not complete**: it rejects some programs that would
have satisfied it. It errs on the side of "no", because the alternative — err
on the side of "yes" — is undefined behaviour.

The canonical rejected-but-safe program:

```rust
let mut v = vec![1, 2, 3, 4];
let a = &mut v[0];
let b = &mut v[3];      // error[E0499]: cannot borrow `v` as mutable more
*a += 1;                // than once at a time
*b += 1;
```

Indices 0 and 3 are disjoint memory, so nothing here can go wrong. But
`v[i]` desugars to `*IndexMut::index_mut(&mut v, i)`, which takes `&mut v` —
the *whole vector*. The checker sees two mutable loans of the same place, and
it cannot know that `0 ≠ 3` implies disjointness, because index computations
are arbitrary runtime values.

Three standard workarounds:

1. **`split_at_mut`** — a library function that hands out two disjoint `&mut`
   slices. Internally it uses `unsafe` and raw pointers; the safety argument is
   made once, by hand, and exported as a safe signature. This is the intended
   pattern: push the unprovable step into a small audited primitive.

   ```rust
   let (l, r) = v.split_at_mut(2);
   l[0] += 1;
   r[1] += 1;
   ```

2. **Work with indices, not references.** An index is a plain `usize`; it
   borrows nothing. Copy the value out, compute, write it back.

   ```rust
   let first = v[0];      // i32 is Copy — no loan survives this line
   v.push(first);         // fine
   ```

   This is the fix for the classic `v.push(v[0])` error, and it is why
   LeetCode-style array code in Rust tends to be index-based.

3. **Scope the borrows.** Put the first loan in a block, or just use it and
   let NLL kill it, before creating the second.

Also useful: `iter_mut()` (the library proves disjointness of successive
elements), `get_mut()` (returns `Option<&mut T>`, no panic), `std::mem::swap`
and `std::mem::take` (move values out without leaving a hole), and interior
mutability types `Cell`/`RefCell` (lesson 9) which move the check to runtime.

Rule of thumb: when the borrow checker rejects something you are *sure* is
safe, the fix is almost never `unsafe`. It is a smaller borrow, an index, or
a library primitive that already did the proof.

## Worked examples

```rust
// Shared borrows are Copy; you can have as many as you like.
let v = vec![1, 2, 3];
let (a, b, c) = (&v, &v, &v);
println!("{} {} {}", a.len(), b[0], c.iter().sum::<i32>());

// Exclusive borrow: one at a time, and it freezes the owner.
let mut v = vec![1, 2, 3];
let m = &mut v;
m.push(4);
// println!("{v:?}");   // error: v is borrowed by m
println!("{m:?}");      // [1, 2, 3, 4]  — last use of m
println!("{v:?}");      // now fine

// A returned reference keeps the loan alive.
fn first(xs: &[i32]) -> Option<&i32> { xs.first() }
let mut v = vec![1, 2, 3];
let f = first(&v);
// v.push(4);           // error: f still borrows v
println!("{f:?}");

// Disjoint fields of a struct are tracked separately.
struct P { x: i32, y: i32 }
let mut p = P { x: 0, y: 0 };
let rx = &mut p.x;
let ry = &mut p.y;      // fine — different places
*rx += 1; *ry += 2;

// Method calls borrow for the duration of the call only.
let mut s = String::from("ab");
let n = s.len();        // &s, dies immediately
s.push('c');            // &mut s
assert_eq!((n, s.len()), (2, 3));
```

## Exercises

Open `exercises/src/l05_borrowing.rs`; run:

    cargo test -p exercises l05

- `longest_len(words)` — read through `&[String]`, return an owned `usize`.
- `add_all(xs, delta)` — mutate every element through `&mut [i32]`.
- `max_ref(xs)` — return `Option<&i32>`; note the loan outlives the call.
- `bump_at(xs, i)` — `get_mut`, not indexing; no panic on out-of-range.
- `bump_halves(xs)` — two simultaneous `&mut` into one slice via `split_at_mut`.
- `remove_all(xs, v)` — in place, no new allocation.
- `count_occurrences(haystack, needle)` — borrow a `&str`, return a count.
- `push_first(v)` — the `v.push(v[0])` puzzle; copy the value out first.

## LeetCode

All of these are in-place array problems where the exclusivity rule is the
whole difficulty; write them index-based.

- 26 Remove Duplicates from Sorted Array — two indices, one `&mut Vec`.
- 27 Remove Element — same shape; compare with `retain`.
- 283 Move Zeroes — slow/fast pointers, `swap` to avoid double `&mut`.
- 344 Reverse String — `&mut [char]`, or `split_at_mut`.
- 88 Merge Sorted Array — merge backwards to avoid overwriting.
- 121 Best Time to Buy and Sell Stock — one shared borrow, running min.
- 125 Valid Palindrome — two indices into a `&str`'s bytes.
- 189 Rotate Array — `reverse` on three `&mut` sub-slices.

## Next

Lesson 6 asks the question this lesson dodged: *how long* is a loan live, and
how does the compiler prove a reference still points at something?
