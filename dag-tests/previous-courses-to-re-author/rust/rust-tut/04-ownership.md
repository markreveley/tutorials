# 04. Ownership and Move Semantics

## Concept

Every value in Rust has exactly one **owner**: a binding, or a field of an
owned value, or a slot in an owned collection. Three rules:

1. Each value has one owner.
2. Assigning or passing a non-`Copy` value **moves** it: the old owner is
   invalidated, the new one takes over. There is still one owner.
3. When an owner goes out of scope while it still owns the value, the value
   is **dropped** — its destructor runs and its heap memory is released.

```rust
let s = String::from("hello");
let t = s;              // MOVE: t owns the buffer, s is dead
println!("{}", s);      // error[E0382]: borrow of moved value: `s`
```

Nothing was copied. A `String` is three words on the stack — pointer,
length, capacity — plus a heap buffer. The move copies the three words and
*forgets* the source binding. Cost O(1), and often zero after optimization.

Passing to a function is the same event:

```rust
pub fn consume_len(s: String) -> usize { s.len() }

let s = String::from("hello");
let n = consume_len(s);      // s moved into the callee
// s is unusable here; the callee dropped the buffer when it returned
```

Returning moves the other way:

```rust
pub fn shout(mut s: String) -> String { s.push('!'); s }   // moved in, moved out
let s = shout(String::from("hi"));                          // caller owns it again
```

### `Copy` types do not move

```rust
let a = 5;
let b = a;
println!("{a} {b}");        // fine: i32 is Copy
```

`Copy` means "duplicating the bytes is a valid duplication of the value".
All scalars are `Copy`; so are tuples and arrays whose elements all are, and
shared references `&T`. Not `Copy`: `String`, `Vec<T>`, `Box<T>`, `&mut T`,
and anything containing them.

```rust
pub fn sum4(arr: [i32; 4]) -> i32 { arr.iter().sum() }
let arr = [1, 2, 3, 4];
assert_eq!(sum4(arr), 10);
assert_eq!(arr[0], 1);      // caller kept its own copy
```

### `Drop`

```rust
struct Noisy(&'static str);
impl Drop for Noisy {
    fn drop(&mut self) { println!("dropping {}", self.0); }
}
{
    let _a = Noisy("a");
    let _b = Noisy("b");
}   // prints "dropping b" then "dropping a"
```

Locals drop in **reverse** declaration order; struct fields drop in
declaration order; a `Vec<T>` drops its elements then frees its buffer. You
never call `drop(&mut self)` yourself. `std::mem::drop(x)` just takes `x` by
value and lets it fall out of scope — a three-line function, not magic.

### `clone` is the explicit escape hatch

```rust
pub fn duplicate(s: String) -> Vec<String> {
    let c = s.clone();      // one allocation + one memcpy, right here
    vec![s, c]
}
```

`clone()` produces a second independently-owned value. It is a method call
you wrote, so its cost is visible in the source. `Copy` is the subset of
cloning that is a bitwise duplicate with no destructor — which is why it can
be implicit.

### Moving out from behind a reference

You cannot move out of something you do not own:

```rust
fn bad(v: &mut Vec<i32>) -> Vec<i32> { *v }   // error[E0507]: cannot move out
```

If that were allowed, `*v` would be a hole — memory that is nobody's and
would still be dropped when the owner's scope ends. The fix is to leave
something valid behind:

```rust
pub fn swap_in_place(a: &mut String, b: &mut String) { std::mem::swap(a, b); }
pub fn take_out(slot: &mut Vec<i32>) -> Vec<i32> { std::mem::take(slot) }
// also: std::mem::replace(slot, new_value) -> old_value
```

`swap` exchanges two owned values through references, `take` swaps in
`Default::default()`, `replace` swaps in whatever you supply. All three are
O(1) and clone nothing. Lesson 5 makes references themselves the subject.

## Why

### Ownership is an affine type discipline

In a **linear** type system every value must be consumed exactly once. In an
**affine** system every value is consumed *at most* once — using it twice is
a type error, using it zero times is allowed. Rust is affine, with an extra
rule that whatever went unused is destroyed automatically at scope exit.

Formalize it. Let a context Γ map each binding to its type and a *status*,
live or moved. Write the typing judgment in flow form,

    Γ ⊢ e : T ⊣ Γ'

read "in context Γ, expression e has type T, leaving context Γ' behind".
The output context is what makes this affine: evaluating an expression can
spend bindings.

**(Var-move)** — using a non-`Copy` binding spends it:

    T is not Copy
    ─────────────────────────────────────────
    Γ, x : T^live  ⊢  x : T  ⊣  Γ, x : T^moved

**(Var-copy)** — `Copy` bindings survive use:

    T : Copy
    ────────────────────────────────────────
    Γ, x : T^live  ⊢  x : T  ⊣  Γ, x : T^live

**(Var-moved)** — there is *no* rule with `x : T^moved` in the input
position concluding `x : T`. The absence of a rule is the whole mechanism:
`error[E0382]: use of moved value` is the type checker reporting that no
derivation exists.

**(App)** — a call spends its argument by the same rule as any use:

    Γ ⊢ e : T ⊣ Γ₁      f : T → U
    ───────────────────────────────
    Γ ⊢ f(e) : U ⊣ Γ₁

**(Let/scope)** — the rule that schedules destruction:

    Γ ⊢ e : T ⊣ Γ₁        Γ₁, x : T^live ⊢ body : U ⊣ Γ₂, x : T^s
    ─────────────────────────────────────────────────────────────
    Γ ⊢ { let x = e; body } : U ⊣ Γ₂        emit drop(x) iff s = live

The compiler inserts a call to the destructor at scope exit **exactly when
the status at that point is live** — that is what "drop flags" are in the
generated code, and why a conditionally-moved value costs a hidden boolean.

Two contrasts worth naming:

- **Affine, not linear**: you may drop a value without using it. A linear
  Rust would force you to consume every `File` explicitly. Rust instead
  consumes it for you, which is what RAII *is*.
- **Not leak-free**: `std::mem::forget(x)` and `Rc` cycles suppress the drop.
  Leaking is memory-*safe* — it never produces a dangling pointer — so it is
  outside the guarantee. Safety here means "no undefined behavior", not "no
  waste".

### Theorem 1: no double free

*Setup.* A heap block is freed only by drop glue, and drop glue for a
binding x is emitted only by the (Let/scope) rule, at most once per scope
exit, and only when x's status is live there.

*Lemma (unique live owner).* At every program point, the map from live
bindings of non-`Copy` type to the heap blocks they own is injective: no
block has two live owners.

*Proof of lemma*, by induction on the typing derivation.

- *Allocation* (`String::from`, `Vec::new`, `Box::new`) produces a fresh
  block reachable from exactly one new binding. Injectivity preserved.
- *(Var-move) followed by a binding of the result.* Before: x live, owning
  block β; nothing else owns β by the hypothesis. After: x is `moved`, and
  the new owner is live and owns β. The number of live owners of β is 1
  before and 1 after. Injectivity preserved.
- *(Var-copy).* Applies only when T : `Copy`. The compiler enforces that no
  type may implement both `Copy` and `Drop` (`error[E0184]`), and a `Copy`
  type transitively contains no field that implements `Drop` — otherwise the
  derive is rejected. Hence a `Copy` value owns no heap block, and
  duplicating it duplicates no ownership. Injectivity preserved vacuously.
- *(Let/scope) exit.* Bindings are removed from the context; removing
  entries cannot break injectivity. ∎

*Proof of theorem.* Suppose block β were freed twice. Each free is a drop
of some live binding at its scope exit. Two cases.

1. Two different bindings x ≠ y, both live and both owning β at their
   respective scope exits. Take the earlier exit, at point p. At p, y is
   still live and owns β (it exits later), and x is live and owns β. Two
   live owners of β at p, contradicting the lemma.
2. The same binding x dropped twice. Impossible: (Let/scope) emits at most
   one drop per binding per scope, and a scope's exit is reached once per
   entry — and each entry rebinds x to whatever `e` evaluated to on *that*
   entry, a separate value. ∎

The interesting case is the one C cannot rule out:

```c
char *p = malloc(n);
char *q = p;            /* two owners, silently */
free(p);
free(q);                /* double free */
```

Line 2 in Rust is `let q = p;`, which is (Var-move): after it, p is moved,
and there is no rule that lets you use p. The C bug is not merely detected;
it is not expressible.

### Theorem 2: no use-after-free

*Claim.* Under these rules (and with no `unsafe`), no expression evaluates
by reading a freed block.

*Proof.* Suppose an expression reads block β at point p, and β was freed at
some earlier point q. By Theorem 1's setup, the free at q was a drop of a
binding x that was live at q and owned β, at x's scope exit.

To read β at p, the program must reach it through some access path. There
are three kinds.

1. **Through x itself.** After q, x is out of scope: x is not in the context
   Γ at p, so no rule concludes anything about x. No derivation exists.
2. **Through another owning binding y.** Then y is live at q (it must be
   live to be usable at p, and (Var-move) only kills, never revives, a
   binding). So x and y are two live owners of β at q — excluded by the
   lemma.
3. **Through a reference `&β` or `&mut β`.** This is the case ownership
   alone does not settle, and it is exactly what lessons 5 and 6 are for:
   the borrow checker requires the referent to outlive the reference, so a
   reference cannot survive to p. Granting that obligation, no path remains.

Since no access path exists, no such derivation exists. ∎

*The honest boundary.* Both theorems are about the safe subset. `unsafe`
code — including the implementation of `Vec` itself — steps outside the
rules and takes on the obligation of restoring them at its boundary. The
guarantee Rust makes is a *conditional* one: safe code cannot cause UB
provided the `unsafe` code it builds on upholds its contracts. That is a far
stronger position than "the programmer is careful", and a weaker one than
"the language is proved sound end to end". (The formal soundness work —
RustBelt — proves the standard library's `unsafe` cores do uphold them.)

### Why this and not a garbage collector

A GC also prevents both bugs. What it costs: an extra word or more per
object, unpredictable pause times, a runtime, and — the part that matters
for correctness rather than speed — **no** guarantee about *when* a resource
is released. A GC's reachability analysis is about memory only; a file
handle, a mutex guard, or a database connection is released whenever the
collector gets around to it, or never. Rust's scope-exit drop is
deterministic, which is why `MutexGuard`, `File`, and `Vec` all use the same
mechanism, and why "resource acquisition is initialization" is not a
convention here but a theorem about the (Let/scope) rule.

The cost of Rust's choice is that the discipline is *visible*: you have to
decide, for each value, whether it moves, is borrowed, or is cloned. That
decision is real in every language; Rust just refuses to let you leave it
implicit.

### Cost, made explicit

| operation | cost |
|---|---|
| move a `String` / `Vec` | copy 3 words, no allocation |
| `clone()` a `String` of n bytes | 1 allocation + n-byte memcpy |
| `Copy` an `[i32; 4]` | 16-byte memcpy, no allocation |
| drop a `Vec<T>` of n elements | n destructor calls + 1 free |
| `mem::swap` / `take` / `replace` | O(1), no allocation |

The rule of thumb for exercises and for LeetCode: reach for a reference
first (lesson 5), a move second, and `clone()` only when you can say the
sentence "I need two independently-owned copies because …". A `.clone()`
inserted to silence a borrow error is a bug report about your design, not a
fix.

## Worked examples

```rust
// Move out of a function: the Vec is built here and handed over
pub fn squares(n: usize) -> Vec<u64> {
    let mut v = Vec::with_capacity(n);       // one allocation, exactly n slots
    for i in 0..n as u64 { v.push(i * i); }
    v                                        // moved to the caller, not copied
}
assert_eq!(squares(5), vec![0, 1, 4, 9, 16]);

// into_iter() moves elements out; iter() would only lend them
pub fn partition_parity(v: Vec<i32>) -> (Vec<i32>, Vec<i32>) {
    let (mut evens, mut odds) = (Vec::new(), Vec::new());
    for x in v.into_iter() {                 // v is consumed
        if x % 2 == 0 { evens.push(x) } else { odds.push(x) }
    }
    (evens, odds)
}

// Move through a reference without cloning
let mut a = String::from("a");
let mut b = String::from("b");
std::mem::swap(&mut a, &mut b);
assert_eq!((a.as_str(), b.as_str()), ("b", "a"));

let mut slot = vec![1, 2, 3];
let old = std::mem::take(&mut slot);         // slot becomes vec![]
assert_eq!(old, vec![1, 2, 3]);
assert!(slot.is_empty());

// Partial moves: a struct can be moved out of field by field
struct Pair { a: String, b: String }
let p = Pair { a: "x".into(), b: "y".into() };
let a = p.a;            // p is now PARTIALLY moved
// let q = p;           // error[E0382]: use of partially moved value
assert_eq!(p.b, "y");   // the still-live field is fine

// Shadowing vs mutation, revisited with ownership
let s = String::from("hi");
let s = shout(s);       // old s moved in; the name is rebound to the result
assert_eq!(s, "hi!");

// Closures capture by move
let data = vec![1, 2, 3];
let f = move || data.len();   // `data` moved into the closure
assert_eq!(f(), 3);
// data is unusable here
```

Reading the error message is a skill:

    error[E0382]: borrow of moved value: `s`
      = note: move occurs because `s` has type `String`,
              which does not implement the `Copy` trait
      help: consider cloning the value if the performance cost is acceptable

The `note` names the rule that fired ((Var-move), because not `Copy`), and
the `help` names the escape hatch and its price. Both are literally the
content of this lesson.

## Exercises

Open `exercises/src/l04_ownership.rs`; run

    cd rust && cargo test -p exercises l04

Write no `clone()` except where the doc comment says one is needed.

- `consume_len(s)` — take by value; note the commented-out line in the test.
- `shout(s)` — `mut` parameter, mutate in place, move back out. No new
  `String`.
- `squares(n)` — build and move out; use `with_capacity`.
- `partition_parity(v)` — `into_iter()`, not `iter()`.
- `swap_in_place(a, b)` — `std::mem::swap`, zero clones.
- `take_out(slot)` — `std::mem::take`; why can't you write `*slot`?
- `duplicate(s)` — exactly one `clone()`: `s` is moved in, and you need two.
- `sum4(arr)` — arrays of `Copy` are `Copy`; the caller keeps its array.

## LeetCode

Ownership rarely changes an algorithm, but it changes the signature — and
picking the wrong one is what makes a Rust submission fight you.

- 1470 Shuffle the String — takes `Vec<i32>` by value; build and return a
  new `Vec`, moving it out. Compare with taking `&[i32]`.
- 1929 Concatenation of Array — the whole exercise is "own the input or
  borrow it"; `nums.repeat(2)` allocates once.
- 88 Merge Sorted Array — mutates `nums1` through `&mut Vec<i32>`; merge
  backwards so you never overwrite an unread element (state that invariant).
- 27 Remove Element / 26 Remove Duplicates from Sorted Array — in-place
  through `&mut Vec<i32>`, returning the new length.
- 448 Find All Numbers Disappeared in an Array — consume the input to build
  the answer, or borrow it; do it both ways and compare.
- 344 Reverse String — `&mut Vec<char>`; `swap` on two indices, and note
  that `v.swap(i, j)` exists precisely because you cannot hold two `&mut`
  into one `Vec` (lesson 5).

## Next

Lesson 5 introduces borrowing — how to *use* a value without taking it —
and the shared-XOR-mutable invariant that discharges case 3 of Theorem 2.
