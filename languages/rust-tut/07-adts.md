# 07. Structs, Enums, and Algebraic Data Types

## Concept

Two ways to build a type from other types.

**Struct** — a value of this *and* that:

```rust
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Point { pub x: i64, pub y: i64 }

let p = Point { x: 1, y: 2 };
let Point { x, y } = p;                       // destructuring
struct Meters(f64);                           // tuple struct
struct Marker;                                // unit struct
```

**Enum** — a value of this *or* that, and the variants may carry data:

```rust
#[derive(Debug, Clone, PartialEq)]
pub enum Shape {
    Circle { r: f64 },
    Rect { w: f64, h: f64 },
    Tri { a: f64, b: f64, c: f64 },
}
```

Methods go in `impl` blocks; `self`, `&self`, `&mut self` pick the ownership
mode (lessons 4–5).

```rust
impl Point {
    pub fn manhattan(self, other: Point) -> i64 {
        (self.x - other.x).abs() + (self.y - other.y).abs()
    }
}
```

`match` takes a value apart, and must cover every case:

```rust
impl Shape {
    pub fn area(&self) -> f64 {
        match self {
            Shape::Circle { r } => std::f64::consts::PI * r * r,
            Shape::Rect { w, h } => w * h,
            Shape::Tri { a, b, c } => {
                let s = (a + b + c) / 2.0;
                (s * (s - a) * (s - b) * (s - c)).sqrt()
            }
        }
    }
}
```

Two enums from the standard library carry most of the weight in real code:

```rust
enum Option<T> { None, Some(T) }
enum Result<T, E> { Ok(T), Err(E) }
```

Rust has no `null`. `Option<T>` is how absence is expressed, and it is an
ordinary enum — nothing built in.

## Why

### Types have cardinalities, and the constructors are arithmetic

Write |T| for the number of distinct values of type T.

    |!|            = 0        the never type — no values at all
    |()|           = 1        the unit type — exactly one value
    |bool|         = 2
    |u8|           = 256
    |char|         = 1_112_064

A struct is a **product**: to build one you must supply *every* field, so the
count multiplies.

    struct P { a: A, b: B }        ⇒  |P| = |A| × |B|
    |(bool, bool)| = 2 × 2 = 4
    |Point| (two i64)              = 2^64 × 2^64 = 2^128

An enum is a **sum**: to build one you supply *exactly one* variant's payload,
so the counts add.

    enum E { L(A), R(B) }          ⇒  |E| = |A| + |B|
    |Option<T>|      = 1 + |T|
    |Result<T, E>|   = |T| + |E|
    |Option<bool>|   = 1 + 2 = 3          None, Some(false), Some(true)

The identities you would expect from arithmetic hold up to isomorphism:
`(T, ())` ≅ `T` (multiplying by 1), `Result<T, !>` ≅ `T` (adding 0), and
`Option<Option<bool>>` has 1 + (1 + 2) = 4 values, matching `(bool, bool)`'s 4
— the same *count*, different types. Function types complete the picture:
|A → B| = |B|^|A|, so `bool -> bool` has 2² = 4 inhabitants.

This is not decoration. Cardinality is a fast check on a data model: **if your
type has more values than your domain has states, some of those values are
bugs you will have to rule out by hand.** A "user with an optional email that
must be present when verified" modelled as `struct { email: Option<String>,
verified: bool }` has 2 × (1 + n) states, two of which are nonsense. Modelled
as an enum with `Unverified` and `Verified { email: String }`, it has exactly
the states that exist.

### Recursive enums need a box

```rust
pub enum Expr {
    Num(i64),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
    Div(Box<Expr>, Box<Expr>),
}
```

|Expr| is infinite, but every *value* must occupy a finite, statically known
number of bytes. `size_of::<Expr>()` would have to satisfy
s = max(8, 2s + tag) — no finite solution. `Box<Expr>` is a pointer of fixed
size, so the recursion goes through the heap and s becomes finite. This is why
Rust rejects a directly recursive enum with "recursive type has infinite size"
and suggests `Box`.

### Exhaustiveness is totality

A `match` is a definition by cases. Defining f : E → R by cases means giving,
for each constructor of E, a rule producing an R. The definition is a
**total function** exactly when the cases cover E.

Because an enum is a disjoint union of its variants, coverage is decidable: the
compiler enumerates constructors and patterns and checks that the union of the
patterns is the whole type. Miss one and it is a compile error, not a runtime
surprise:

```rust
match light {
    Light::Red => Light::Green,
    Light::Green => Light::Yellow,
}   // error[E0004]: non-exhaustive patterns: `Light::Yellow` not covered
```

The practical payoff is *change safety*: add a variant, and the compiler lists
every match that must be revisited. A wildcard `_ => ...` arm turns that
guarantee off — it makes the match total by fiat and silences the next
addition. Use `_` for genuinely open cases (integers, strings), avoid it on
enums you own.

Patterns compose: literals, ranges `1..=9`, bindings `n @ 1..=9`, or-patterns
`A | B`, struct and tuple destructuring, nested patterns, and guards
`Some(x) if x > 0 =>`. Guards are *not* considered by the exhaustiveness
checker — `Some(x) if x > 0` does not cover `Some`.

### Why `null` is absent, precisely

In a language with null, every reference type T is secretly the sum T + 1, but
the `+ 1` is invisible to the type system. Two things follow:

1. **Every dereference carries an unproven precondition.** `x.f` is only
   defined when x ≠ null, and nothing checks it. The failure appears at
   runtime, arbitrarily far from the code that produced the null.
2. **The totality check becomes impossible.** You cannot ask the compiler
   "did I cover every case?" when one case is present in every type and absent
   from the syntax.

`Option<T>` makes the `+ 1` a first-class constructor. Now:

- The type `T` genuinely means "a T"; if it can be absent, the signature says
  so. Absence is documented by the compiler, not by a comment.
- Getting at the value *requires* handling `None` — via `match`, `if let`,
  `?`, or an explicit `unwrap` that you must write and can be grepped for.
- Absence **nests**: `Option<Option<T>>` has three states, and
  `map.get(k)` returning `Option<&Option<V>>` distinguishes "no key" from "key
  present, value absent". Null cannot express this; null of null is null.

And it is free. Rust applies a **niche optimization**: `&T`, `Box<T>`, `NonZero*`
and similar types have forbidden bit patterns, so `None` is encoded as one of
them and `size_of::<Option<&T>>() == size_of::<&T>()`. You get the checked
version of a nullable pointer at exactly the nullable pointer's cost.

`Result<T, E>` applies the same move to failure: the error case is in the type,
so ignoring it is a compile-time warning rather than a silently dropped return
code.

### Getting values out

Full `match` is always available. Three shorthands cover most uses:

```rust
if let Some(x) = opt { use_it(x); } else { fallback(); }   // one case + else

let Some(x) = opt else { return None; };                   // let-else: bind or diverge
                                                           // x is in scope afterwards
while let Some(top) = stack.pop() { visit(top); }          // loop until None
```

`let ... else` is the tool for early returns; the `else` block must diverge
(`return`, `break`, `continue`, `panic!`).

The `?` operator propagates:

```rust
fn parse_point(s: &str) -> Result<Point, String> {
    let (xs, ys) = s.split_once(',').ok_or_else(|| format!("no comma in {s:?}"))?;
    let x = xs.trim().parse::<i64>().map_err(|e| e.to_string())?;
    let y = ys.trim().parse::<i64>().map_err(|e| e.to_string())?;
    Ok(Point { x, y })
}
```

`e?` desugars to roughly

```rust
match e {
    Ok(v) => v,
    Err(err) => return Err(From::from(err)),
}
```

— the `From::from` is why `?` can convert between error types automatically.
It works on `Option` too, returning `None` early. `?` is only legal in a
function whose return type is the matching enum.

### Combinators

`match` when the logic is interesting; combinators when it is a pipeline.

```rust
opt.map(f)                 // Option<T> -> Option<U>          apply inside
opt.and_then(f)            // f: T -> Option<U>               flatten (monadic bind)
opt.filter(pred)           // keep Some only if pred holds
opt.unwrap_or(d)           // T, with default
opt.unwrap_or_else(|| d()) // lazily computed default
opt.unwrap_or_default()    // T: Default
opt.ok_or(e)               // Option<T> -> Result<T, E>
opt.as_ref()               // &Option<T> -> Option<&T>        borrow inside
opt.take()                 // &mut Option<T> -> Option<T>, leaving None

res.map(f) / res.map_err(g)
res.and_then(f)            // f: T -> Result<U, E>
res.ok()                   // Result<T, E> -> Option<T>, discarding the error
res.unwrap_or(d)
```

`map` vs `and_then` is the distinction to internalize: `map` when `f` cannot
fail, `and_then` when it can (otherwise you get `Option<Option<U>>`).

`collect` has a useful trick: an iterator of `Option<T>` collects into
`Option<Vec<T>>`, and one of `Result<T, E>` into `Result<Vec<T>, E>` —
short-circuiting on the first `None`/`Err`. The same works for `sum` and
`product`, which is the one-liner for `sum_all` in the exercises.

Avoid `unwrap` and `expect` outside tests and cases where you can state the
invariant that makes them unreachable. If you write `expect`, write the reason:
`expect("index checked above")`.

## Worked examples

```rust
// Sum type as a state machine; exhaustive next().
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Light { Red, Green, Yellow }

impl Light {
    fn next(self) -> Light {
        match self {
            Light::Red => Light::Green,
            Light::Green => Light::Yellow,
            Light::Yellow => Light::Red,
        }
    }
}
assert_eq!(Light::Red.next().next().next(), Light::Red);

// Recursion over a sum type mirrors the type's structure.
fn eval(e: &Expr) -> Result<i64, String> {
    Ok(match e {
        Expr::Num(n) => *n,
        Expr::Add(a, b) => eval(a)? + eval(b)?,
        Expr::Mul(a, b) => eval(a)? * eval(b)?,
        Expr::Div(a, b) => {
            let d = eval(b)?;
            if d == 0 { return Err("division by zero".to_string()); }
            eval(a)? / d
        }
    })
}

// Patterns: guards, ranges, or-patterns, bindings.
fn classify(n: i32) -> &'static str {
    match n {
        i32::MIN..=-1 => "negative",
        0 => "zero",
        1 | 2 | 3 => "small",
        x if x % 2 == 0 => "even",
        _ => "odd",
    }
}

// Combinator pipeline vs. the same thing as a match.
let s = "42";
let doubled: Option<i64> = s.parse::<i64>().ok().map(|n| n * 2);
assert_eq!(doubled, Some(84));

// Short-circuiting collect.
let all: Option<Vec<i64>> = ["1", "2", "x"].iter().map(|s| s.parse().ok()).collect();
assert_eq!(all, None);

// Niche optimization: no space cost for the absence case.
assert_eq!(std::mem::size_of::<Option<&u8>>(), std::mem::size_of::<&u8>());
```

## Exercises

Open `exercises/src/l07_adts.rs`; run:

    cargo test -p exercises l07

- `Point` + `manhattan` — a product type and a method taking `self` by value.
- `Shape::area` — exhaustive match, no `_` arm; Heron's formula for the triangle.
- `Expr` + `eval` — recursive sum type behind `Box`, errors propagated with `?`.
- `parse_point(s)` — `split_once`, `ok_or_else`, `parse`, `map_err`, `?`.
- `second_largest(xs)` — `Option` state threaded through a fold or a match.
- `Light::next` — a total function on a three-state enum.
- `sum_all(xs)` — short-circuiting `Option`; one line with `sum()`.

## LeetCode

- 20 Valid Parentheses — `while let Some(c) = stack.pop()`, match on the pair.
- 155 Min Stack — a struct with two `Vec`s; `Option` for the empty case.
- 8 String to Integer (atoi) — a small state machine as an enum.
- 65 Valid Number — the same, and a case where `_` arms hide bugs.
- 224 Basic Calculator — build and evaluate an `Expr`-like tree.
- 150 Evaluate Reverse Polish Notation — `Result` for division by zero.
- 706 Design HashMap — `Vec<Option<...>>` buckets; nested absence matters.
- 341 Flatten Nested List Iterator — a recursive sum type, exactly like `Expr`.

## Next

Lesson 8 asks what `Some(x) == Some(y)` and `xs.sort()` actually require of a
type: traits, bounds, and the two ways Rust dispatches a method call.
