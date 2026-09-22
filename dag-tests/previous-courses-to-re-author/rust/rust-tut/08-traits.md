# 08. Traits, Generics, and Dispatch

## Concept

A **trait** names a set of operations a type can support.

```rust
pub trait Area {
    fn area(&self) -> f64;                 // required
    fn is_degenerate(&self) -> bool {      // provided (default) method
        self.area() == 0.0
    }
}

pub struct Square(pub f64);
impl Area for Square {
    fn area(&self) -> f64 { self.0 * self.0 }
}
```

A **generic** function abstracts over a type, and a **bound** says which traits
that type must implement.

```rust
pub fn largest<T: PartialOrd + Copy>(xs: &[T]) -> Option<T> {
    let mut it = xs.iter().copied();
    let mut best = it.next()?;
    for x in it { if x > best { best = x; } }
    Some(best)
}
```

Bounds may also be written in a `where` clause, which is the same thing with
more room:

```rust
fn show_all<T>(xs: &[T]) -> String
where T: std::fmt::Debug
{ format!("{xs:?}") }
```

`impl Trait` is shorthand. In argument position it is an anonymous generic
parameter; in return position it is an opaque concrete type.

```rust
pub fn min_by_key_fn<T, K: Ord>(xs: &[T], key: impl Fn(&T) -> K) -> Option<&T> {
    xs.iter().min_by_key(|x| key(x))
}
fn evens(xs: &[i32]) -> impl Iterator<Item = &i32> { xs.iter().filter(|x| *x % 2 == 0) }
```

`#[derive(...)]` writes the obvious implementation for you:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Default)]
pub struct Version { pub major: u32, pub minor: u32, pub patch: u32 }
```

Derived `PartialOrd`/`Ord` on a struct compare fields **in declaration order**,
lexicographically — which is exactly semantic-version ordering here, and a
reason to order fields deliberately.

## Why

### A trait is a predicate on types

Read `Area` as a set: the collection of types for which an `impl Area` exists.
Then `T: Area` is the proposition *T ∈ Area*, and an `impl Area for Square` is
a **witness** for that proposition. `T: A + B` is conjunction, T ∈ A ∧ T ∈ B.

A generic function is then a term with a **bounded universal** type:

    largest : ∀T. (T ∈ PartialOrd ∧ T ∈ Copy) ⇒ &[T] → Option<T>

Two consequences, and they are the whole ergonomics of Rust generics.

**Inside the body, only the bounds are available.** `T` is opaque; you may use
exactly the operations the bounds provide. Forget `Copy` and `.copied()` stops
compiling — inside the function, not at some caller. Contrast C++ templates,
which typecheck after substitution and produce errors in terms of code the
caller never wrote.

**At the call site, the compiler must find the witness.** `largest(&[3, 9, 2])`
requires `i32: PartialOrd` and `i32: Copy`; both impls exist, so the
proposition is discharged and the call is accepted. If not, the error names the
missing impl.

Operationally, the witness is a **dictionary**: a record of the trait's
function pointers. `impl Area for Square` is that record. Everything below is
about *when* the dictionary is chosen.

### Coherence: witnesses must be unique

Rust enforces two rules:

- **Overlap:** for a given trait and type, at most one impl may apply.
- **Orphan:** you may write `impl Trait for Type` only if you define the trait
  or the type (roughly — the local-type rule has refinements).

Why uniqueness matters: `HashMap` inserts using `Hash` and looks up using
`Hash`. If two crates could each supply a different `Hash for String`, a value
inserted through one and queried through the other would go missing, with no
`unsafe` anywhere. Global uniqueness of the witness makes the choice of impl
independent of context. The price is the orphan rule, and the standard
workaround is a newtype: `struct MyString(String)` is your type, so you may
implement foreign traits on it.

### Two dispatch strategies

Given a call `x.area()`, the compiler must find the right function body. It has
two ways.

**Static dispatch via monomorphization.** For a generic like
`total_area_static<T: Area>(xs: &[T])`, the compiler emits one specialized copy
per concrete `T` used in the program, with the dictionary resolved at compile
time and erased. `total_area_static::<Square>` contains a *direct* call to
`Square::area` — usually inlined away entirely.

```rust
pub fn total_area_static<T: Area>(xs: &[T]) -> f64 {
    xs.iter().map(|x| x.area()).sum()
}
```

- Cost at runtime: zero. Same code you would have written by hand.
- Cost at compile time: one copy per instantiation — binary size and
  compile time grow with the number of distinct `T`s.
- Limitation: `&[T]` is homogeneous. A slice cannot hold a `Square` and a
  `Circle`; `T` is one type per instantiation.

**Dynamic dispatch via trait objects.** `dyn Area` is an unsized type; you
handle it behind a pointer (`&dyn Area`, `Box<dyn Area>`, `Rc<dyn Area>`).
That pointer is **fat**: two words, a data pointer and a **vtable** pointer.
The vtable is a static table holding the size, alignment, and drop glue of the
concrete type, plus one function pointer per trait method.

```rust
pub fn total_area_dyn(xs: &[Box<dyn Area>]) -> f64 {
    xs.iter().map(|x| x.area()).sum()
}

let mixed: Vec<Box<dyn Area>> = vec![Box::new(Square(1.0)), Box::new(Circle(1.0))];
```

- Cost at runtime: one load from the vtable plus an indirect call, and — usually
  the bigger cost — the call cannot be inlined, which blocks constant folding
  and vectorization across it. Pointers are two words instead of one.
- Cost at compile time: one copy of `total_area_dyn`, whatever the mix.
- Gain: **heterogeneity**. The vector above is the thing generics cannot
  express.

The tradeoff, concretely: *generics trade binary size for speed; trait objects
trade speed for flexibility and code size.* Default to generics. Reach for
`dyn` when you need a heterogeneous collection, when the concrete type is only
known at runtime (plugins, parsed configuration), when a public API should not
leak type parameters, or when monomorphization is measurably bloating the
build. Boxed errors (`Box<dyn Error>`) are the most common real use.

### Object safety

Not every trait can become a `dyn Trait`. A trait is **dyn-compatible**
(historically "object safe") when every method can be given a vtable slot. The
main disqualifiers:

- **Generic methods.** `fn f<U>(&self, u: U)` would need one vtable slot per
  `U`, and the set of `U`s is not known when the vtable is built.
- **`Self` by value or in the return type** — `fn clone(&self) -> Self`,
  `fn eq(&self, other: &Self)`. The caller of a `dyn` method does not know
  `Self`'s size, so it cannot pass or receive one by value.
- **Associated constants**, and `Self: Sized` bounds on the trait itself.

Hence `Clone` and `PartialEq` are not dyn-compatible, and `Iterator` is (its
`next` returns `Option<Self::Item>`, and `Item` is fixed once the concrete type
is). A method that would break the rule can be excluded from the vtable with
`where Self: Sized`, which keeps the rest of the trait usable as an object.

### Associated types vs type parameters

```rust
trait Iterator { type Item; fn next(&mut self) -> Option<Self::Item>; }
trait From<T>  { fn from(t: T) -> Self; }
```

An **associated type** is an output: the implementing type determines it, and
there is at most one impl. A **type parameter** is an input: a type may
implement the trait many times, once per parameter. `Vec<i32>` iterates over
exactly one `Item`, so `Item` is associated. `String` can be built `From<&str>`
and `From<char>`, so `From`'s parameter is a parameter. Choosing wrong shows up
as either impossible impls or turbofish everywhere at call sites.

### The traits worth memorizing

| Trait | Meaning | Notes |
| --- | --- | --- |
| `Debug` | `{:?}` formatting | derive it on everything; `{:#?}` pretty-prints |
| `Display` | `{}` formatting | never derived — you write the user-facing form |
| `Clone` | explicit duplication | `.clone()`; may be deep and expensive |
| `Copy` | implicit bitwise duplication | requires `Clone`; only for small, `Drop`-free types |
| `PartialEq` | `==` | partial: `NaN != NaN` |
| `Eq` | marker: `==` is reflexive | `f64` is `PartialEq` but **not** `Eq` |
| `PartialOrd` | `<`, `>`, `partial_cmp` | may return `None` (incomparable) |
| `Ord` | total order, `cmp` | required by `sort`, `BinaryHeap`, `BTreeMap` |
| `Hash` | hashing | keys of `HashMap`/`HashSet`; must agree with `Eq` |
| `Default` | `T::default()` | pairs with struct update: `Foo { x: 1, ..Default::default() }` |
| `From`/`Into` | infallible conversion | implement `From`; `Into` comes free by blanket impl |
| `TryFrom`/`TryInto` | fallible conversion | returns `Result` |
| `FromStr` | `"1.2.3".parse::<T>()` | associated `Err` type |
| `Iterator` | `next()` | one required method, ~70 provided (lesson 10) |

Three rules that follow from the table and cause most beginner confusion:

- **`Eq` is a promise, not a method.** It asserts `a == a` for all `a`. `f64`
  cannot promise it, so floats are barred from `HashMap` keys and from
  `sort()`. Sort floats with
  `xs.sort_by(|a, b| a.partial_cmp(b).unwrap())`, having ruled out NaN.
- **Implement `From`, never `Into`.** The standard library has
  `impl<T, U: From<T>> Into<U> for T`; writing `From` gives you both, and `?`
  converts error types through `From` automatically (lesson 7).
- **`Hash` and `Eq` must agree**: `a == b ⇒ hash(a) == hash(b)`. Derive both
  together, or neither.

Traits can have **supertraits** (`trait Ord: Eq + PartialOrd`), which is
implication: T ∈ Ord ⇒ T ∈ Eq. And **blanket impls** apply to every type
satisfying a bound — `impl<T: Display> ToString for T` is why every `Display`
type has `.to_string()`.

## Worked examples

```rust
// Implementing a std trait so std machinery works on your type.
use std::str::FromStr;

impl FromStr for Version {
    type Err = String;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.split('.').collect();
        if parts.len() != 3 { return Err(format!("bad version {s:?}")); }
        let p = |i: usize| parts[i].parse::<u32>().map_err(|e| e.to_string());
        Ok(Version { major: p(0)?, minor: p(1)?, patch: p(2)? })
    }
}

let a: Version = "1.2.3".parse().unwrap();      // .parse() came from FromStr
let b: Version = "1.10.0".parse().unwrap();
assert!(a < b);                                  // derived Ord: 2 < 10 numerically
let mut vs = vec![b, a];
vs.sort();                                       // sort() requires Ord
assert_eq!(vs[0], a);

// Display is written by hand, and gives ToString for free.
impl std::fmt::Display for Point {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}
assert_eq!(format!("{}", Point { x: 1, y: -2 }), "(1, -2)");
assert_eq!(Point { x: 0, y: 0 }.to_string(), "(0, 0)");

// An operator is a trait: bound on Add to write generic arithmetic.
pub fn pair_sum<T: std::ops::Add<Output = T> + Copy>(p: (T, T)) -> T { p.0 + p.1 }
assert_eq!(pair_sum((1, 2)), 3);
assert_eq!(pair_sum((1.5, 2.5)), 4.0);

// Static and dynamic dispatch, side by side.
let squares = [Square(1.0), Square(2.0)];
let s = total_area_static(&squares);                       // one direct call per element
let mixed: Vec<Box<dyn Area>> = vec![Box::new(Square(1.0)), Box::new(Circle(1.0))];
let d = total_area_dyn(&mixed);                            // one vtable call per element
assert!(Square(0.0).is_degenerate());                      // default method, no impl needed

// Fat pointers are two words wide.
use std::mem::size_of;
assert_eq!(size_of::<&Square>(), size_of::<usize>());
assert_eq!(size_of::<&dyn Area>(), 2 * size_of::<usize>());

// Closures are traits: Fn / FnMut / FnOnce, by how they capture.
fn apply<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 { f(x) }
let k = 10;
assert_eq!(apply(|x| x + k, 5), 15);
```

## Exercises

Open `exercises/src/l08_traits.rs`; run:

    cargo test -p exercises l08

- `largest(xs)` — `T: PartialOrd + Copy`; note where the bounds are forced.
- `Area` with a default method, plus `impl Area for Square`/`Circle`.
- `total_area_static` vs `total_area_dyn` — the same fold, both dispatch modes.
- `Display for Point` — `write!` into the formatter, return `fmt::Result`.
- `min_by_key_fn(xs, key)` — `impl Fn(&T) -> K` with `K: Ord`.
- `Version` — derive `Ord` and rely on field order; implement `FromStr` so
  `"1.2.3".parse()` works.
- `pair_sum(p)` — bound on `std::ops::Add<Output = T>`.

## LeetCode

Problems where the ordering or hashing trait is the actual content.

- 215 Kth Largest Element in an Array — `BinaryHeap` needs `Ord`.
- 347 Top K Frequent Elements — `HashMap` needs `Eq + Hash`; heap needs `Ord`.
- 23 Merge k Sorted Lists — a custom `Ord` impl, `Reverse` for a min-heap.
- 49 Group Anagrams — a derived-`Hash` key type.
- 56 Merge Intervals — `sort_by_key` on a struct field.
- 179 Largest Number — a custom comparator: `b+a` vs `a+b`.
- 1 Two Sum — `HashMap<i32, usize>`, the `Eq`/`Hash` pair in the simplest case.
- 146 LRU Cache — a design problem where trait bounds shape the API.

## Next

Lesson 9 puts these traits to work: the standard collections, what each one
requires of its element type, and what each operation costs.
