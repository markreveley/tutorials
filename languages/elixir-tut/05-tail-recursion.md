# 05 — Accumulators, tail calls, and why there are no loops

## Concept

Lesson 4 wrote list functions the obvious inductive way: solve the tail,
then do one more thing on the way out.

```elixir
def sum([]), do: 0
def sum([h | t]), do: h + sum(t)
```

This is **body recursion**: the recursive call sits *inside* a larger
expression (`h + □`). The addition cannot happen until the call returns, so
the caller's frame must survive the call. `sum(xs)` for a list of length n
therefore builds n nested frames before any addition happens.

The alternative is **tail recursion**, where the recursive call is the
*whole* body — the last thing the function does. Nothing is pending, so
there is nothing to come back to:

```elixir
def sum(xs), do: sum_acc(xs, 0)

defp sum_acc([], acc), do: acc
defp sum_acc([h | t], acc), do: sum_acc(t, acc + h)
```

The `acc + h` is computed *before* the call, not after it. The recursive
call is in **tail position**.

### Tail position, precisely

An expression `e` is in tail position of a function body if its value *is*
the function's value — no further work is applied to it. Structurally:

```
body(do: e)              → e is tail
body(e1; e2)             → e2 is tail (e1 is not)
case v do p -> e end     → each e is tail if the case is
cond do g -> e end       → each e is tail if the cond is
if c, do: e1, else: e2   → e1, e2 are tail if the if is
f(...)                   → the call is tail; its *arguments* are not
h + f(x)                 → f(x) is NOT tail (the + is pending)
try/catch                → the body is NOT tail (a handler is pending)
```

A **last call** is a call in tail position. What the BEAM guarantees:

> When a function performs a last call, its own stack frame is discarded
> before the call, and the callee reuses it.

This is *last call optimisation*, and on the BEAM it is a specified
property of the virtual machine, not a compiler heuristic you have to hope
for. It applies to any last call, not just self-calls: mutual recursion
between `even?/1` and `odd?/1` runs in constant stack too. Consequently a
tail-recursive function runs in **O(1) stack** for any input length, and a
process can loop forever (this is exactly how servers are written, lesson
10).

### "No loops" is not a limitation

Elixir has no `while`, no `for(i=0;;)`, no `break`. It does not need them.
A loop is a state machine: some state, a step function, an exit condition.
A tail-recursive function *is* that state machine, with the loop variables
made explicit as parameters:

```
while (cond) { state = step(state) }   ≡   defp loop(s) when cond(s), do: loop(step(s))
                                           defp loop(s), do: s
```

The translation is mechanical and total: any loop becomes a tail call, any
tail call becomes a loop. You lose nothing, and you gain that the loop
variables are named, immutable, and visible in the function head — which is
what makes the invariants below provable.

## Grounding: accumulator introduction is a program transformation

The accumulator is not a trick. It is a transformation with a statement and
a proof. The pattern always has the same three parts:

1. Define an auxiliary `f_acc(xs, acc)`.
2. Prove a **lemma** relating `f_acc` to the original `f`, for *all* `acc`.
3. Instantiate the lemma at the identity element to get `f`.

Step 2 is where the generalisation happens: the statement you prove is
*stronger* than the one you want, and that is precisely why the induction
goes through.

### Sum

Original (the specification):

```
sum([])       = 0
sum([h | t])  = h + sum(t)
```

Accumulator version:

```
sum_acc([], a)      = a
sum_acc([h | t], a) = sum_acc(t, a + h)
```

**Lemma.** ∀ xs, ∀ a. `sum_acc(xs, a) ≡ sum(xs) + a`.

*Proof* by structural induction on `xs`. Note the ∀ a: the accumulator is
universally quantified *inside* the induction, so the hypothesis may be used
at a different accumulator than the one in the goal. Without that, the proof
fails.

- Base `xs = []`:
  `sum_acc([], a) = a` and `sum([]) + a = 0 + a = a`. ✓

- Step `xs = [h | t]`, assuming IH: ∀ a. `sum_acc(t, a) ≡ sum(t) + a`.

  ```
  sum_acc([h | t], a)
    = sum_acc(t, a + h)        (definition)
    = sum(t) + (a + h)         (IH, instantiated at a + h  ← needs the ∀ a)
    = (h + sum(t)) + a         (associativity + commutativity of +)
    = sum([h | t]) + a         (definition of sum, backwards)
  ```
  ✓ ∎

**Corollary.** `sum_acc(xs, 0) ≡ sum(xs) + 0 ≡ sum(xs)`. So the wrapper
`def sum(xs), do: sum_acc(xs, 0)` is correct.

Notice what the proof needed: `+` associative, and `0` a unit for it. That
is a **monoid**. The transformation works for any monoid — `*`/`1`,
`++`/`[]`, `max`/`-∞`. Commutativity was used for cosmetics only; keeping
the operands in order, the step gives `sum_acc(t, a ⊕ h) = sum(t) ⊕ (a ⊕ h)
= (a ⊕ h) ⊕ sum(t)`, so for a non-commutative `⊕` the accumulator version
folds **left** where the original folded **right**. They agree exactly when
`⊕` is associative and the unit is two-sided. This is the whole content of
lesson 6's foldl/foldr distinction, met early.

### Reverse

```
rev([])      = []
rev([h | t]) = rev(t) ++ [h]          -- O(n²): ++ is O(length of left arg)

rev_acc([], a)      = a
rev_acc([h | t], a) = rev_acc(t, [h | a])
```

**Lemma.** ∀ xs, ∀ a. `rev_acc(xs, a) ≡ rev(xs) ++ a`.

- Base: `rev_acc([], a) = a` and `rev([]) ++ a = [] ++ a = a`. ✓
- Step, IH: ∀ a. `rev_acc(t, a) ≡ rev(t) ++ a`.

  ```
  rev_acc([h | t], a)
    = rev_acc(t, [h | a])          (definition)
    = rev(t) ++ [h | a]            (IH at [h | a])
    = rev(t) ++ ([h] ++ a)         ([h | a] ≡ [h] ++ a)
    = (rev(t) ++ [h]) ++ a         (associativity of ++, lesson 4)
    = rev([h | t]) ++ a            (definition)
  ```
  ✓ ∎

**Corollary.** `rev_acc(xs, []) ≡ rev(xs) ++ [] ≡ rev(xs)`.

Here the transformation buys more than stack: it changes the complexity
class. `rev` is O(n²) because each `++` copies its left argument; `rev_acc`
does one cons per element, O(n). Consing onto an accumulator *while walking
forwards* is the single most important idiom in Elixir — the result comes
out reversed, and one final `Enum.reverse` (itself O(n) and tail recursive)
fixes it. Two O(n) passes beat one O(n²).

### A fold

Both proofs above are instances of one theorem. Define

```
foldr(f, z, [])       = z
foldr(f, z, [h | t])  = f(h, foldr(f, z, t))      -- body recursive

foldl(f, z, [])       = z
foldl(f, z, [h | t])  = foldl(f, f(z, h), t)      -- tail recursive
```

**Theorem.** If `⊕` is associative with two-sided unit `z`, then
∀ xs, ∀ a. `foldl(⊕, a, xs) ≡ a ⊕ foldr(⊕, z, xs)`.

- Base: `foldl(⊕, a, []) = a` and `a ⊕ foldr(⊕, z, []) = a ⊕ z = a`. ✓
- Step, IH: ∀ a. `foldl(⊕, a, t) ≡ a ⊕ foldr(⊕, z, t)`.

  ```
  foldl(⊕, a, [h | t])
    = foldl(⊕, a ⊕ h, t)            (definition)
    = (a ⊕ h) ⊕ foldr(⊕, z, t)      (IH at a ⊕ h)
    = a ⊕ (h ⊕ foldr(⊕, z, t))      (associativity)
    = a ⊕ foldr(⊕, z, [h | t])      (definition)
  ```
  ✓ ∎

At `a = z`: `foldl(⊕, z, xs) ≡ foldr(⊕, z, xs)`. Sum is `⊕ = +, z = 0`;
reverse is `f = fn a, h -> [h | a] end` (not a monoid on the same type, but
the same induction with `++` supplies the proof, as above). Lesson 6 uses
this theorem constantly to swap a readable `foldr` for a cheap `foldl`.

### When body recursion is actually fine — or better

The received advice "always write tail-recursive code" is wrong on the BEAM.
Facts that change the calculus:

- **The stack is a heap-allocated, growable segment per process**, starting
  around 233 words and doubling. Deep body recursion is not a segfault
  risk the way a fixed 8 MB C stack is; it costs memory and GC pressure,
  not a crash, until it hits `:max_heap_size`.
- **A tail-recursive `map` must build its output backwards and reverse it**:
  two traversals and 2n conses (the reversal allocates a fresh spine). The
  body-recursive `map` does one traversal and n conses. Since OTP R12 the
  body-recursive version is typically as fast or faster, and it uses less
  total memory for lists of ordinary size.
- **Body recursion can return early.** `member?/2` written body-recursively
  stops at the first hit with nothing pending; there is no accumulator to
  unwind.
- **Body recursion is often the specification.** `foldr` on an infinite or
  lazily-produced structure can terminate; `foldl` cannot.

Practical rule:

| Situation | Use |
|---|---|
| Unbounded / user-controlled length (a server loop, a file's lines) | tail |
| Result is a scalar reduction (sum, count, max) | tail |
| Building a list from a list of ordinary size, order preserved | body is fine |
| You would need `reverse` at the end anyway | tail + `Enum.reverse` |
| Anything that must run in constant stack forever | tail, always |

"Ordinary size" means the list fits comfortably in memory and you know its
order of magnitude. When in doubt on the hot path, measure with
`:timer.tc/1`; do not guess.

## Worked examples

```elixir
iex> defmodule T do
...>   def sum(xs), do: do_sum(xs, 0)
...>   defp do_sum([], acc), do: acc
...>   defp do_sum([h | t], acc), do: do_sum(t, acc + h)
...>
...>   def reverse(xs), do: do_rev(xs, [])
...>   defp do_rev([], acc), do: acc
...>   defp do_rev([h | t], acc), do: do_rev(t, [h | acc])
...>
...>   def map(xs, f), do: do_map(xs, f, []) |> reverse()
...>   defp do_map([], _f, acc), do: acc
...>   defp do_map([h | t], f, acc), do: do_map(t, f, [f.(h) | acc])
...> end
iex> T.sum(Enum.to_list(1..1_000_000))
500000500000
iex> T.map([1, 2, 3], &(&1 * &1))
[1, 4, 9]
```

The million-element sum runs in constant stack. Define the body-recursive
`sum` from the top of this lesson and run it on the same input — it works,
but check `:erlang.process_info(self(), :stack_size)` before and after to
watch a million frames appear and go.

### Counting with a guard-driven loop

```elixir
iex> defmodule Count do
...>   def upto(n), do: loop(1, n, [])
...>   defp loop(i, n, acc) when i > n, do: Enum.reverse(acc)
...>   defp loop(i, n, acc), do: loop(i + 1, n, [i | acc])
...> end
iex> Count.upto(5)
[1, 2, 3, 4, 5]
```

That is a `for` loop. `i` is the induction variable, the guard is the exit
condition, `acc` is the mutable buffer — all explicit, none of them mutated.

### Two accumulators

Nothing stops you carrying several. Fibonacci in O(n) with a pair of
accumulators, versus the naive O(φⁿ) body recursion:

```elixir
iex> defmodule Fib do
...>   def fast(n), do: loop(n, 0, 1)
...>   defp loop(0, a, _b), do: a
...>   defp loop(n, a, b), do: loop(n - 1, b, a + b)
...> end
iex> Fib.fast(200)
280571172992510140037611932413038677189525
```

Invariant, provable by induction on `n`: `loop(n, fib(k), fib(k+1)) ≡
fib(k + n)`. At `k = 0` this gives `loop(n, 0, 1) ≡ fib(n)`. Writing the
invariant down first is usually the fastest way to get the base case right.

### Not tail calls (common mistakes)

```elixir
def f([h | t]), do: 1 + f(t)                       # + is pending
def f(xs), do: try do g(xs) after :ok end          # after is pending
def f([h | t]), do: [h | f(t)]                     # cons is pending (but see below)
def f(xs), do: {:ok, g(xs)}                        # wrapping is pending
```

The third is worth a note: `[h | f(t)]` is body recursion, but it is the
*good* kind — one traversal, n conses, and the natural definition of `map`.
The BEAM cannot make it a last call, and it does not need to.

## Exercises

`exercises/05_tail.exs`, module `Tail`. Every function must run in
constant stack — write an accumulator helper (`defp`) for each and keep the
public function as a thin wrapper. Hints:

- `sum/1`: accumulator `0`. State the lemma before you write it.
- `reverse/1`: accumulator `[]`, cons onto it.
- `count/1`: accumulator `0`; do not use `Kernel.length/1`.
- `map/2`: accumulate `[f.(h) | acc]`, then reverse. Compare to the
  body-recursive one-liner and say which you would ship.
- `range/2`: `range(a, b)` is `[a, a+1, ..., b]`, `[]` if `a > b`. Either
  count down consing (no reverse needed) or count up and reverse — the
  first is a nice illustration that the accumulator's *order* is a design
  choice.
- `fib/1`: two accumulators, as above. `fib(0) == 0`, `fib(1) == 1`.
- `running_sum/1`: `[1,2,3,4] -> [1,3,6,10]`. Carry the running total *and*
  the output list; that is leetcode 1480 exactly.

## Leetcode at this stage

- 1480 Running Sum of 1d Array — the exercise above.
- 7 Reverse Integer — `div`/`rem` with an accumulator; guard the 32-bit
  overflow range.
- 9 Palindrome Number — build the reversed number in an accumulator, no
  strings.
- 509 Fibonacci Number — the two-accumulator loop.
- 206 Reverse Linked List — literally `rev_acc`; the proof above *is* the
  correctness argument the interviewer wants.
- 1342 Number of Steps to Reduce a Number to Zero — a counter accumulator.
- 2235 Add Two Integers — trivial, but write the loop version of `a + b`
  with `succ`/`pred` if you want to feel the translation.
