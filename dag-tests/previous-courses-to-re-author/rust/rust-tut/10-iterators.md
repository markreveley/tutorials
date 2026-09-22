# 10. Iterators and Closures

## Concept

An iterator is anything implementing one method:

```rust
pub trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
    // ~75 provided methods, all built on next()
}
```

`None` means exhausted. Implement `next`, get everything else free:

```rust
pub struct Fib { a: u64, b: u64 }

impl Iterator for Fib {
    type Item = u64;
    fn next(&mut self) -> Option<u64> {
        let out = self.a;
        let next = self.a + self.b;
        self.a = self.b;
        self.b = next;
        Some(out)                     // never None: this iterator is infinite
    }
}
```

Three ways to iterate a collection, differing only in what they hand you:

```rust
for x in &v      { }   // v.iter()      -> Item = &T      (borrow)
for x in &mut v  { }   // v.iter_mut()  -> Item = &mut T  (mutable borrow)
for x in v       { }   // v.into_iter() -> Item = T       (moves v)
```

**Adapters** are lazy: they build a new iterator and do no work.

```rust
xs.iter()
  .map(|x| x * 2)              // transform
  .filter(|x| *x > 3)          // keep
  .enumerate()                 // -> (usize, Item)
  .zip(other)                  // stop at the shorter
  .take(5).skip(2)             // prefix / drop prefix
  .take_while(|x| ...)         // stop at first failure
  .skip_while(|x| ...)
  .rev()                       // needs DoubleEndedIterator
  .chain(more)                 // concatenate
  .flat_map(|x| ...)           // map then flatten
  .scan(init, |st, x| ...)     // fold that yields every intermediate
  .peekable()                  // adds .peek()
  .step_by(2)
  .cloned() / .copied()        // &T -> T
```

**Consumers** drive the machine and produce a value:

```rust
.collect::<Vec<_>>()   .sum::<i64>()   .product()   .count()
.fold(init, |acc, x| ...)   .for_each(|x| ...)
.any(pred)   .all(pred)   .find(pred)   .position(pred)
.min()  .max()  .min_by_key(f)  .max_by_key(f)  .min_by(cmp)
.last()  .nth(i)  .partition(pred)  .unzip()
```

Slices add three non-iterator windows that behave like adapters:
`v.windows(k)` (overlapping), `v.chunks(k)` (disjoint), `v.split(pred)`.

A **closure** is an anonymous function plus captured environment. Rust infers
the capture mode from the body, then classifies the closure by the trait it can
implement:

| Trait | Captures | Callable | `self` in `call` |
| --- | --- | --- | --- |
| `Fn` | by `&` | any number of times | `&self` |
| `FnMut` | by `&mut` | many times, needs a `mut` binding | `&mut self` |
| `FnOnce` | by value (consumes) | exactly once | `self` |

```rust
let n = 10;
let read  = |x: i32| x + n;          // Fn:     borrows n
let mut v = vec![];
let mut push  = |x: i32| v.push(x);  // FnMut:  mutably borrows v
let owned = String::from("s");
let eat   = move || owned;           // FnOnce: moves owned out
```

`move` forces every capture to be taken **by value**. It is required whenever
the closure outlives the scope that owns the captures — returning it, spawning
a thread, or storing it in a struct.

## Why

### Why `Fn` / `FnMut` / `FnOnce` are three traits and not one

They are exactly the three ways a callable can treat its captured state, and
they follow from ownership, not from any special-casing of closures:

- If the body only reads a capture, calling requires `&self`, so the closure
  can be called through a shared reference, concurrently, any number of times.
- If the body mutates a capture, calling requires `&mut self`. Aliasing rules
  then forbid two simultaneous calls — hence `let mut c = counter();`.
- If the body *moves* a capture out, calling consumes the closure. A second
  call would read a moved-out value, so the type system must forbid it.

The inclusion `Fn ⊆ FnMut ⊆ FnOnce` holds as trait bounds (`Fn` implies
`FnMut` implies `FnOnce`), so a generic function should demand the *weakest*
bound it can: take `FnOnce` if you call once, `FnMut` if you call in a loop
with mutation, `Fn` only if you truly need the strongest guarantee.

Every closure has its own anonymous type, which is why returning one needs
either `impl Fn(..) -> ..` (static, monomorphised, zero indirection) or
`Box<dyn Fn(..) -> ..>` (a heap allocation and one indirect call, but a type you
can name and store in a `Vec`).

### Why laziness is not an optimisation but a requirement

```rust
fib().take_while(|&x| x < 100).filter(|x| x % 2 == 0).sum::<u64>()  // 44
```

`fib()` never returns `None`. If `take_while` eagerly materialised its input
this would not terminate. Laziness makes infinite sources legal, makes
short-circuiting (`any`, `find`, `position`) actually short-circuit, and means
a chain of k adapters allocates zero intermediate vectors regardless of k. The
cost is one real rule to remember: **an adapter chain with no consumer does
nothing**, and the compiler warns you (`#[must_use]`).

### Why the adapter chain compiles to the same loop

Claim: `xs.iter().filter(p).map(f).sum()` emits the same machine code as the
hand-written loop. Four facts compose to give it.

**1. Adapters are structs, not allocations.** `map` returns
`Map<I, F> { iter: I, f: F }`. So the chain above has the static type
`Map<Filter<slice::Iter<i32>, P>, F>` — a struct containing a slice pointer, a
length, and the two closures. Nothing is on the heap.

**2. Closures with no captures are zero-sized.** `|x| x * 2` captures nothing,
so its type is a ZST: `size_of` is 0, and it occupies no space in the `Map`
struct. The whole chain object is the same size as the original slice iterator.

**3. Everything is statically dispatched and monomorphised.** `F` is a concrete
closure type, so `self.f(x)` is a direct call to a known function — never a
function pointer, never a vtable. LLVM inlines it.

**4. `for` desugars to exactly the same shape as the loop.**

```rust
for x in it { body }
// becomes
let mut it = IntoIterator::into_iter(it);
loop { match it.next() { Some(x) => { body } None => break } }
```

Composing them: `Map::next` calls `Filter::next` calls `Iter::next`. Each is a
tiny `#[inline]` function. After inlining, the three `next` bodies fuse into one
loop body whose control flow is `if p(x) { acc += f(x) }` — the hand-written
loop, with the `Option` matching optimised away because the `None` case is the
loop exit. `sum` starts from `Iterator::fold`, which many iterators override
with an internal loop precisely so this fusion has less work to do.

Two places where the abstraction is *better* than the naive loop, not merely
equal: slice iterators carry a start/end pointer pair, so the compiler needs no
bounds check per element (whereas `for i in 0..n { v[i] }` needs the optimiser
to prove `i < n`); and `collect` reads `size_hint`, so `Vec` is allocated once
at the right capacity instead of grown by doubling.

Where it stops being free: `dyn` closures (`Box<dyn Fn>`) prevent inlining;
`collect()` in the middle of a chain forces a real allocation; and
`.map(...).collect::<Vec<_>>().iter().filter(...)` pays for a vector that the
fused version would not have needed.

### `iter()` vs `into_iter()` and the borrow you keep forgetting

`v.iter()` yields `&T`, so closures receive references and `filter` receives a
reference *to* that: `|x: &&i32|`. That is why `.filter(|x| **x > 3)` and
`.filter(|&&x| x > 3)` and `.copied().filter(|x| *x > 3)` all appear. Pick one
style; `.copied()` early is usually clearest for `Copy` element types.

## Worked examples

```rust
// scan: a fold that emits every partial result
let totals: Vec<i32> = [1, 2, 3].iter()
    .scan(0, |acc, x| { *acc += x; Some(*acc) })
    .collect();
assert_eq!(totals, vec![1, 3, 6]);

// fold with an explicit accumulator and a widening type
let p = [2, 3, 4].iter().fold(1i64, |acc, &x| acc * x as i64);
assert_eq!(p, 24);

// vacuous truth: all() over nothing is true, any() over nothing is false
assert!([].iter().all(|_: &i32| false));
assert!(![].iter().any(|_: &i32| true));

// short-circuiting: position stops at the first hit
assert_eq!([1, 3, 4, 5].iter().position(|&x| x % 2 == 0), Some(2));

// windows for adjacency questions
assert!([1, 2, 2, 3].windows(2).any(|w| w[0] == w[1]));

// collect can target more than Vec
use std::collections::{HashMap, HashSet};
let set: HashSet<i32> = [1, 2, 2].into_iter().collect();
let map: HashMap<&str, usize> = ["a", "bb"].into_iter().map(|s| (s, s.len())).collect();

// collect::<Result<Vec<_>, _>> turns a sequence of fallible steps into one Result
let ok: Result<Vec<i32>, _> = ["1", "2"].iter().map(|s| s.parse::<i32>()).collect();
let bad: Result<Vec<i32>, _> = ["1", "x"].iter().map(|s| s.parse::<i32>()).collect();
assert!(ok.is_ok() && bad.is_err());

// FnMut closure with private state
let mut c = { let mut n = 0; move || { n += 1; n } };
assert_eq!((c(), c()), (1, 2));
```

## Exercises

Open `exercises/src/l10_iterators.rs`; run `cargo test -p exercises l10`.

- `squares_of_evens`, `sum_of_lengths`, `zip_sum`, `flatten_nested`,
  `rev_chain`, `chunk_sums` — adapter fluency, one chain each, no `for` loops.
- `running_totals`, `take_while_increasing` — `scan` and `enumerate` +
  `take_while`.
- `index_of_first`, `all_positive`, `any_adjacent_equal`, `longest_word`,
  `partition_parity`, `product_fold` — consumers, including the empty-input
  edge cases.
- `apply_twice`, `make_adder`, `counter`, `consume_once` — one function per
  capture mode; note which need `move` and which need `mut`.
- `Fib` / `fib` / `first_n_fib` / `odd_squares_sum` — implement `next` and let
  laziness handle the infinity.

## LeetCode

- 136 Single Number — `fold` with XOR, O(1) space.
- 268 Missing Number — `sum` and the Σ formula, or XOR.
- 709 To Lower Case — `chars().map(..).collect::<String>()`.
- 1470 Shuffle the Array — `zip` and `flat_map`.
- 1512 Number of Good Pairs — `enumerate` plus counting.
- 561 Array Partition — `sort_unstable` then `step_by(2)`.
- 448 Find All Numbers Disappeared in an Array — `enumerate` + `filter_map`.
- 118 Pascal's Triangle — `windows(2)` on the previous row.
- 412 Fizz Buzz — `map` over a range into `Vec<String>`.
- 1051 Height Checker — `zip` a sorted copy with the original.
