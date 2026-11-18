# Elixir from the ground up — for functional leetcode

A 12-lesson course. Reader: a programmer who has never written Elixir, who
wants to solve leetcode-style problems in a genuinely functional style and
understand *why* the style works, not just imitate it.

## Running things

Prerequisites: `/opt/homebrew/bin/elixir` and `iex` (Elixir 1.18 / OTP 27).

```sh
cd ~/dev/repos/coding/elixir

# run one exercise file (its inline ExUnit tests execute):
elixir exercises/01_basics.exs

# run a solved version:
elixir solutions/01_basics.exs

# run everything:
for f in solutions/*.exs; do elixir "$f"; done

# explore interactively:
iex
iex> [1, 2, 3] |> Enum.map(&(&1 * 2))
[2, 4, 6]

# load an exercise module into iex and poke at it:
iex> c "exercises/04_lists.exs"     # compiles, runs tests, leaves module loaded
iex> Lists.reverse([1, 2, 3])
```

Useful iex keys: `h Enum.map` (docs), `i value` (inspect type), `recompile`,
Ctrl-C twice to quit. `IO.inspect(x, label: "here")` returns `x`, so you can
drop it into any pipeline.

## Layout

```
00-overview.md          this file
01-values-and-match.md  ... 12-patterns-ii.md   lessons
exercises/NN_topic.exs  stubbed module + tests (tests fail until you fill in)
solutions/NN_topic.exs  same tests, solved
```

Each exercise file is self-contained:

```elixir
ExUnit.start()                   # boot the test runner

defmodule Topic do               # you edit this
  def f(_x), do: raise "not implemented"
end

defmodule TopicTest do           # you leave this alone
  use ExUnit.Case
  test "f" do assert Topic.f(1) == 2 end
end
```

Workflow: read the lesson, open `exercises/NN_*.exs`, replace each
`raise "not implemented"` with a real body, re-run until green. Compare to
`solutions/` only after you have something passing (or are truly stuck).

## How each lesson is organised

1. **Concept** — the language feature, minimal syntax.
2. **Grounding** — the formal idea underneath it (unification, structural
   induction, folds, sum types, actors...) and a short rigorous proof where
   one is cheap. Proofs use plain text: `xs ++ ys`, `∀`, `⇒`, `≡`.
3. **Worked examples** — code you can paste into iex.
4. **Exercises** — pointer to the file, with hints.
5. **Leetcode** — problems that this stage's tools are sufficient for.

## The theoretical spine

The course has one argument running through it:

- A program is a set of **rewrite rules** over immutable **terms**
  (lesson 1). `=` is not assignment; it asks "can these two terms be made
  equal?" (unification).
- Functions with multiple clauses are **case analysis** on the shape of
  their input (lesson 2). Pattern matching is sound because a pattern is
  just a term with holes, and matching is structural.
- Because nothing mutates, **equational reasoning** is valid: you may
  replace any expression with its value anywhere (lesson 3). This is what
  makes proofs about programs possible.
- Lists are an **inductively defined** type (`[]` or `[h | t]`), so
  **structural induction** is the proof technique that matches the data
  (lesson 4). Every recursive list function is a proof by induction in
  disguise.
- Accumulator-passing (tail recursion) is a **program transformation**
  with a correctness proof (lesson 5). Loops are unnecessary once you have
  it.
- `map`, `filter`, `reduce` are **folds**; folds are universal — every
  structurally recursive list function is a fold (lesson 6). Laws like
  `map f ∘ map g = map (f ∘ g)` are provable and let you refactor safely.
- Maps and sets are **persistent** structures; O(log n) update is the
  price of keeping old versions alive (lesson 7).
- Errors are **sum types** `{:ok, v} | {:error, e}`; `with` is a
  monadic bind over them (lesson 8).
- Binaries are bytes, strings are UTF-8 binaries, charlists are lists of
  codepoints; complexity is a **proof obligation** you discharge by
  structural reasoning (lesson 9).
- Processes are **actors**: isolated state plus a mailbox; the model is
  formal and composable (lesson 10).
- Lessons 11–12 apply all of it to the standard leetcode pattern
  catalogue: two pointers, sliding window, prefix sums, hashing, binary
  search with an explicit invariant, trees, graphs, BFS/DFS with
  `:queue`, DP as memoised recursion, heaps.

## Lesson list

| # | File | Topic |
|---|------|-------|
| 01 | `01-values-and-match.md` | Values, atoms, tuples, `=` as unification |
| 02 | `02-pattern-matching.md` | Patterns, guards, multi-clause functions |
| 03 | `03-immutability.md` | Immutability, referential transparency, rebinding |
| 04 | `04-lists-and-recursion.md` | Cons cells, recursion, structural induction |
| 05 | `05-tail-recursion.md` | Accumulators, tail calls, no loops |
| 06 | `06-enum-and-folds.md` | Enum/Stream, higher-order functions, fold laws |
| 07 | `07-maps-and-structs.md` | Maps, keyword lists, MapSet, structs, persistence |
| 08 | `08-pipes-and-errors.md` | Pipes, `with`, errors as sum types |
| 09 | `09-binaries-and-strings.md` | Binaries, strings, charlists, complexity |
| 10 | `10-processes.md` | Processes, messages, actors, GenServer |
| 11 | `11-patterns-i.md` | Two pointers, sliding window, prefix sums, hashing, binary search |
| 12 | `12-patterns-ii.md` | Trees, graphs, BFS/DFS, DP/memoisation, heaps |

## Conventions

- `xs`, `ys` for lists; `h`/`t` for head/tail; `acc` for accumulators.
- `f ∘ g` means `fn x -> f.(g.(x)) end`.
- `≡` is "equal as terms after evaluation".
- Complexity claims are stated as `O(n)` with `n` defined in context.
- Leetcode problem references give the number and name; solve them in an
  `.exs` file with your own ExUnit tests, following the exercise-file
  shape.
