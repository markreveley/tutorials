# 00. Overview

A ground-up Python course for a programmer whose goal is to solve LeetCode
problems and *know why* the solutions are correct. Every lesson pairs a
language feature with the formal idea that justifies it.

## How to run things

    cd python
    python3 -m pytest exercises/                 # run every exercise file
    python3 -m pytest exercises/01_objects.py    # run one lesson
    python3 -m pytest exercises/01_objects.py -k test_bind   # one test
    python3 -m pytest solutions/                 # reference solutions (all pass)

If `pytest` is missing:

    python3 -m pip install --user pytest
    # on Homebrew/PEP 668 systems:
    python3 -m pip install --user --break-system-packages pytest

Exercise stubs `raise NotImplementedError`, so a fresh run shows every test
failing. Replace the bodies until the file is green. Tests live in the same
file as the stubs; read them — they are the specification.

To poke at something interactively: `python3 -q`, then `>>> import this`.

## Files

    00-overview.md
    01-objects-and-expressions.md     exercises/01_objects.py
    02-control-flow-and-invariants.md exercises/02_control_flow.py
    03-functions-scope-recursion.md   exercises/03_functions.py
    04-lists-tuples-mutability.md     exercises/04_lists.py
    05-strings-and-slicing.md         exercises/05_strings.py
    06-dicts-sets-hashing.md          exercises/06_dicts_sets.py
    07-classes-and-dataclasses.md     exercises/07_classes.py
    08-iterators-generators.md        exercises/08_iterators.py
    09-complexity.md                  exercises/09_complexity.py
    10-patterns-arrays.md             exercises/10_patterns_arrays.py
    11-patterns-recursion-trees.md    exercises/11_patterns_trees.py
    12-patterns-dp-heaps-graphs.md    exercises/12_patterns_dp.py
    solutions/NN_*.py                 solved versions, same tests

## How each lesson is organized

1. **Concept** — the language feature, minimal syntax.
2. **Why** — the semantic requirement that forces the rule, stated and
   argued. Short proofs where a proof exists.
3. **Worked examples** — code you can paste into `python3 -q`.
4. **Exercises** — pointer to `exercises/NN_*.py`.
5. **LeetCode** — problems solvable with only what you know so far.

Lessons 1–8 are the language. Lesson 9 is the analysis toolkit. Lessons
10–12 are the problem-solving patterns, each with a correctness argument.

## The theoretical spine

Four ideas recur in every lesson. Learn to reach for them by name.

**1. Names bind to objects.** A Python variable is a label, not a box.
`a = b` makes two labels for one object. Every surprise about mutation,
default arguments, and `is` vs `==` reduces to this (lessons 1, 4).

**2. Invariants.** A loop is correct when some statement P is true before
the loop, is preserved by every iteration, and, together with the exit
condition, implies the postcondition. We write loops by choosing P first
(lessons 2, 10, 12 — binary search is the canonical case).

**3. Induction.** A recursive function is correct when it is correct on
base cases and, assuming correctness on smaller inputs, correct on the
current one. Induction and recursion are the same idea viewed from two
directions; the structure of the data (list, tree) dictates the shape of
the proof (lessons 3, 11, 12).

**4. Cost as an obligation.** A solution is not finished until you can
state its time and space bounds and say why. Big-O is defined precisely
in lesson 9 and every pattern after that carries a cost argument.

## Notation

Plain-text math throughout: `∀ i < n`, `a[i..j)` means indices i through
j-1 (half-open, matching Python slices), `⇒` for implication, `Σ` for sums,
`⌊x⌋` for floor. `{P} S {Q}` is a Hoare triple: if P holds before S runs
and S terminates, Q holds after.

## Prerequisites

You can program in some language. Nothing about Python is assumed.
