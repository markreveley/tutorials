# 00. Overview

**Redesign in progress:** the [tests-first DAG specification](../../dag-tests/README.md)
targets reading and explaining beatcode. Start with its
[source-reading assessments](dag/assessments/reading.md) to review the new direction.
The lessons below are the original course; the DAG rewrite is not yet authored.

A ground-up Rust course for a programmer whose goal is to solve LeetCode
problems and *know why* the solutions are correct — and, in Rust's case, why
they are *safe*. Every lesson pairs a language feature with the formal idea
that justifies it.

## How to run things

    cd rust
    cargo test                          # everything: exercises + solutions
    cargo test -p exercises             # every exercise module
    cargo test -p exercises l01         # one lesson (substring match on test path)
    cargo test -p exercises l01::tests::digits    # one test
    cargo test -p solutions             # reference solutions (all pass)

The workspace is `rust/Cargo.toml` with two members, `exercises` and
`solutions`. Edition 2024, no external dependencies — everything here is
`std` or less. A stable toolchain new enough for edition 2024 is the only
prerequisite (`rustup update stable`).

Exercise stubs are `todo!()`, which compiles and then panics at run time, so
a fresh `cargo test -p exercises` shows every test failing. Replace the
bodies until the module is green. Tests live in the same file as the stubs,
in an inline `#[cfg(test)] mod tests` — read them; they are the
specification.

Two flags worth knowing:

    cargo test -- --nocapture     # let println! through
    cargo test --release          # overflow checks OFF — see lesson 01

To poke at something interactively there is no REPL; write a scratch
`fn main()` or use `cargo test -- --nocapture` on a throwaway `#[test]`.

## Files

    00-overview.md
    01-basics.md          exercises/src/l01_basics.rs
    02-control-flow.md    exercises/src/l02_control_flow.rs
    03-functions.md       exercises/src/l03_functions.rs
    04-ownership.md       exercises/src/l04_ownership.rs
    05-borrowing.md       exercises/src/l05_borrowing.rs
    06-lifetimes.md       exercises/src/l06_lifetimes.rs
    07-adts.md            exercises/src/l07_adts.rs
    08-traits.md          exercises/src/l08_traits.rs
    09-collections.md     exercises/src/l09_collections.rs
    10-iterators.md       exercises/src/l10_iterators.rs
    11-patterns1.md       exercises/src/l11_patterns1.rs
    12-patterns2.md       exercises/src/l12_patterns2.rs
    solutions/src/lNN_*.rs   solved versions, same tests

## How each lesson is organized

1. **Concept** — the language feature, minimal syntax.
2. **Why** — the semantic requirement that forces the rule, stated and
   argued. Short proofs where a proof exists.
3. **Worked examples** — code you can paste into a test and run.
4. **Exercises** — pointer to `exercises/src/lNN_*.rs` and the command.
5. **LeetCode** — problems solvable with only what you know so far.

Lessons 1–3 are the ordinary imperative language: values, control flow,
functions. Lessons 4–6 are the part of Rust no other mainstream language
has — ownership, borrowing, lifetimes — and they are where the formal
content is densest. Lessons 7–8 are data modelling (enums, structs, traits).
Lessons 9–10 are the standard library you actually use. Lessons 11–12 are
the problem-solving patterns, each with a correctness argument and a cost
argument.

## The theoretical spine

Four ideas recur in every lesson. Learn to reach for them by name.

**1. Ownership is an affine type discipline.** In a *linear* type system
every value must be used exactly once; in an *affine* system every value is
used *at most* once. Rust is affine: a move consumes the binding, and
whatever is never moved out is destroyed exactly once by the compiler at
scope exit. The whole memory-safety story is a corollary. Write the rule as

    Γ₁ ⊢ e : T     (the binding is spent)
    ─────────────
    Γ₁ ∖ {x} ⊢ …   (it is gone from the environment afterwards)

and double-free and use-after-free become *unprovable* rather than merely
discouraged (lesson 4 proves this).

**2. Shared XOR mutable.** At any program point, for any value, either there
exist any number of shared references `&T` and no way to mutate, or exactly
one `&mut T` and no other access path at all. Never both. This single
invariant is what buys data-race freedom, iterator-invalidation freedom, and
the compiler's licence to assume `&mut T` does not alias (lessons 5, 6, 9).

**3. Invariants and induction.** A loop is correct when some statement P is
true before it, is preserved by every iteration, and, together with the exit
condition, implies the postcondition; it terminates when some quantity into
a well-founded order strictly decreases. A recursive function is correct
when it is correct on base cases and, assuming correctness on smaller
inputs, correct on the current one. Loops and recursion are the same idea
seen from two directions (lessons 2, 3, 11, 12).

**4. Cost as an obligation.** A solution is not finished until you can state
its time and space bounds and say why. In Rust the obligation is sharper
than in Python, because the language makes every allocation and every copy
visible: `clone()` is a cost you wrote down, `&` is a cost you did not.
Every pattern from lesson 11 on carries a cost argument.

## Notation

Plain-text math throughout. `∀ i < n` is universal quantification, `⇒` is
implication, `∧` and `∨` are and/or, `Σ` is summation, `⌊x⌋` is floor,
`a[i..j)` means indices i through j−1 (half-open, matching Rust's `&a[i..j]`
and `i..j` ranges). `{P} S {Q}` is a Hoare triple: if P holds before S runs
and S terminates, then Q holds after. `∎` ends a proof.

For types: `x : T` reads "x has type T", `Γ ⊢ e : T` reads "in environment
Γ, expression e has type T", and a horizontal rule separates premises above
from conclusion below.

## Prerequisites

You can program in some language. Nothing about Rust is assumed. If you have
written C you will find lesson 4 familiar in its concerns and alien in its
guarantees; if you have written only garbage-collected languages, lesson 4
is where the course actually starts.
