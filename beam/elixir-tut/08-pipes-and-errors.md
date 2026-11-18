# 08 — Pipes, `with`, and errors as sum types

## Concept

### The pipe operator

`|>` is pure syntax. The compiler rewrites it before anything else happens:

```
x |> f()            ≡  f(x)
x |> f(a, b)        ≡  f(x, a, b)
x |> f() |> g()     ≡  g(f(x))
```

The left operand is inserted as the **first** argument of the call on the
right. That is the whole rule: no runtime pipe, no protocol, no overhead.

```elixir
iex> [3, 1, 2] |> Enum.sort() |> Enum.map(&(&1 * 10)) |> Enum.sum()
60
# ≡ Enum.sum(Enum.map(Enum.sort([3, 1, 2]), &(&1 * 10)))
```

Read a pipeline left to right; read the desugared form right to left. Same
term, different reading order.

### Pipes are function composition, written forwards

If `f` and `g` are one-argument functions, `x |> f() |> g() ≡ (g ∘ f)(x)`.
A pipeline is a composite function applied to a seed value — composition
*is* sequencing for pure functions.

Composition is associative, so you may cut a pipeline anywhere and name
the halves without changing the result: `a |> f() |> g() |> h()` ≡
`mid = a |> f() |> g(); mid |> h()`. It also has an identity,
`Function.identity/1`. That is the formal reason refactoring pipelines is
always safe.

### Data first

The rule "left operand becomes argument 1" is a design constraint on your
own functions. Put the thing being transformed first:

```elixir
def scale(list, k)          # pipes:     list |> scale(2)
def scale(k, list)          # does not:  list |> scale(2) means scale(list, 2) — wrong
```

The whole standard library obeys this: `Enum.map(enumerable, fun)`,
`String.split(string, sep)`, `Map.put(map, k, v)`. Subject first,
configuration after. Write your functions the same way and they compose
with everything else.

Pipe hygiene: always use parentheses in a pipeline (`|> Enum.sort()`, not
`|> Enum.sort`) — without them the compiler warns, because `|> f a, b` is
ambiguous. `|>` binds *looser* than arithmetic, so `a + b |> f()` is
`f(a + b)`; that is usually what you meant, but starting a pipeline from a
plain variable or literal removes the need to know.

## Errors as a sum type

A **sum type** (tagged union) is a type whose values come from one of
several disjoint cases, each carrying its own payload. Elixir has no static
checker for this, but it has the shape:

```
Result(v, e)  =  {:ok, v}  |  {:error, e}
```

Two constructors, disjoint because the first element is a distinct atom. A
`case` over them is **case analysis on the constructor**; because the tags
differ, the analysis is exhaustive and unambiguous. Same idea as `Either e a` in Haskell or `Result<T, E>` in Rust. The value
of the discipline: an error is an ordinary term — returnable, storable in a
list, mappable, matchable. No separate control channel.

### `case` chains and the pyramid

Sequencing fallible steps by hand nests one level per step:

```elixir
case fetch_user(id) do
  {:ok, user} ->
    case fetch_account(user) do
      {:ok, acct} -> charge(acct, 10)
      {:error, e} -> {:error, e}
    end
  {:error, e} -> {:error, e}
end
```

Every `{:error, e} -> {:error, e}` line is noise — one per step, all saying
"propagate".

### `with` is bind

`with` collapses that pyramid:

```elixir
with {:ok, user}    <- fetch_user(id),
     {:ok, acct}    <- fetch_account(user),
     {:ok, receipt} <- charge(acct, 10) do
  {:ok, receipt}
end
```

Semantics: each `<-` clause evaluates its right side and matches it against
the pattern on the left. On success, bindings are added and the next clause
runs. If **any** match fails, `with` stops immediately and evaluates to
*the unmatched value itself* — no later clause runs, and the `do` block
never runs.

Note carefully: `with` short-circuits on *pattern-match failure*, not on
"error". `{:ok, v} <- expr` short-circuits on anything that is not an
`{:ok, _}` tuple — which is what makes it work uniformly over `:error`,
`{:error, e}`, `nil`, and `false`.

An optional `else` intercepts the failure value:

```elixir
with {:ok, n} <- parse(s), {:ok, q} <- safe_div(100, n) do
  {:ok, q}
else
  {:error, :division_by_zero} -> {:ok, :infinity}
  {:error, e}                 -> {:error, {:bad_input, e}}
end
```

Without `else` the failing value is returned unchanged, which is usually
what you want and is why `with` composes cleanly with functions that
already return `{:ok, _} | {:error, _}`.

### The desugaring

`with` is a macro. Two clauses desugar to nested `case`:

```elixir
with p1 <- e1, p2 <- e2 do body end

# ≡

case e1 do
  p1 -> case e2 do
          p2 -> body
          other -> other        # or: else clauses applied to `other`
        end
  other -> other
end
```

Name the propagation step:

```
bind(m, k)  =  case m do {:ok, v} -> k.(v); {:error, e} -> {:error, e} end
return(v)   =  {:ok, v}
```

The payment example is then literally

```
bind(fetch_user(id), fn user ->
  bind(fetch_account(user), fn acct ->
    bind(charge(acct, 10), return)))
```

`bind` with `return` is the **error monad**, and `with` is do-notation for
it. Unfold the `case` to check the monad laws:

```
bind(return(v), k)        ≡ case {:ok, v} do {:ok, x} -> k.(x); ... end  ≡ k.(v)      (left identity)
bind(m, return)           ≡ m                                                        (right identity)
bind(bind(m, k), j)       ≡ bind(m, fn v -> bind(k.(v), j) end)                      (associativity)
```

All three are proved by a two-case split on `m`: either `m ≡ {:ok, v}` and
both sides reduce to the same term, or `m ≡ {:error, e}` and both sides
reduce to `{:error, e}`. Associativity is the useful one — it says the
*grouping* of steps does not matter, which is the licence to extract a
middle chunk of a `with` into its own function.

## Grounding: the first error wins, and no later step runs

**Claim.** For a `with` of clauses `p1 <- e1, …, pn <- en` and body `b`,
let `k` be the least index such that `ek` produces a value not matching
`pk` (if there is no such `k`, the result is `b`). Then:

1. the value of the whole `with` is the value of `ek` (modulo `else`), and
2. `e(k+1) … en` and `b` are never evaluated.

**Proof** by induction on `n`, the number of clauses.

*Base, n = 0.* `with do b end ≡ b`. There is no `k`; the claim holds
vacuously and the result is `b`. ✓

*Step.* Assume the claim for `n` clauses; consider `n+1`. By the
desugaring the term is `case e1 do p1 -> W'; other -> other end`, where
`W'` is the `with` over clauses `2..n+1` with body `b`.

`case` evaluates `e1` to a value `v1`, then selects a branch by matching
patterns *in order*. Matching is total and decidable (lesson 1), so exactly
one branch is selected, and — the load-bearing fact — `case` evaluates
**only** the selected branch.

- If `v1` does not match `p1`: the first branch is not selected, so `W'` is
  never evaluated; hence no `ei` for `i ≥ 2` is evaluated, and neither is
  `b`. The second branch returns `v1`. Here `k = 1` and both parts hold. ✓
- If `v1` matches `p1`: `k ≠ 1`, and the result is the value of `W'` under
  the bindings from the match. By the induction hypothesis applied to `W'`,
  its value is the first non-matching `ek` (k ≥ 2) with nothing after it
  evaluated, or `b` if all match. ✓

∎

Two corollaries. **Short-circuiting is the semantics, not an
optimisation** — it follows from `case` evaluating one branch, with nothing
about `{:ok, _}` built in. And **effects after the first failure cannot
happen**: if `e3` writes a file and `e2` fails, the write does not occur.
That is why `with` suits a sequence of fallible side-effecting steps, and
why you order clauses cheapest-and-likeliest-to-fail first.

One caution the proof makes visible: the failure value is returned *raw*,
so two clauses that both fail with `{:error, :not_found}` are
indistinguishable. Tag at the source — `{:error, {:user, :not_found}}` —
rather than recovering provenance in `else`.

## Bang functions and exceptions

```elixir
Map.fetch(m, :k)         # {:ok, v} | :error     — failure is a value
Map.fetch!(m, :k)        # v | raises KeyError   — failure is an exception
Integer.parse("x")       # :error
String.to_integer("x")   # raises ArgumentError
```

The trailing `!` means: *this function raises on failure instead of
returning a tagged tuple*. It is a naming convention only — the compiler
does not enforce it — but it is universal, so honour it. Define the tuple
version as the primitive and the bang version on top of it:

```elixir
def fetch!(map, key) do
  case fetch(map, key) do
    {:ok, v} -> v
    {:error, e} -> raise ArgumentError, "missing key: #{inspect(e)}"
  end
end
```

Which to use: **tuple version when failure is expected** (user input, a
missing file, a network call), **bang version when failure means a bug**
(a key you just put in the map). A bang call in a pipeline is a deliberate
assertion that this step cannot fail.

### raise / rescue / throw

```elixir
raise "boom"                          # RuntimeError
raise ArgumentError, "bad thing"      # a specific exception struct
try do
  raise ArgumentError, "bad"
rescue
  e in ArgumentError -> {:rescued, e.message}
after
  IO.puts("always runs")
end
```

`throw`/`catch` is a separate, lower-level non-local jump (early exit out
of deep recursion); prefer restructuring the recursion. `exit/1` terminates
the process (lesson 10).

Exceptions are for the **exceptional**: what you did not model in the
return type because it is not part of the function's contract. Using them
for ordinary control flow throws away what the sum type bought you — that
failure is data you can match, store, and compose. A `rescue` in the middle
of a pipeline is a smell; a `with` is not.

### Let it crash

A process that hits an unmodelled failure should die, not limp along with
half-valid state. Its **supervisor** notices, discards the corrupt state,
and restarts it from a known-good initial state. This works only because
processes are isolated — one dying cannot corrupt another's memory
(lesson 10). Defensive `try/rescue` everywhere is therefore worse than
noisy: it converts "restart from a clean state" into "continue from an
unknown one". Model the failures you expect as `{:error, e}`; let the rest
crash.

## Worked examples

```elixir
iex> "  Hello, World!  " |> String.trim() |> String.downcase() |> String.split(", ")
["hello", "world!"]

iex> with {:ok, a} <- Map.fetch(%{a: 1}, :a),
...>      {:ok, b} <- Map.fetch(%{a: 1}, :b) do
...>   {:ok, a + b}
...> end
:error                     # the raw failing value of clause 2, not {:error, _}

iex> with {n, ""} <- Integer.parse("42"), true <- n > 0, do: {:ok, n * 2}
{:ok, 84}
iex> with {n, ""} <- Integer.parse("-42"), true <- n > 0, do: {:ok, n * 2}
false                      # `true <- ...` failed; the raw value is `false`

iex> Enum.reduce_while([1, 2, -3, 4], {:ok, 0}, fn
...>   x, {:ok, acc} when x >= 0 -> {:cont, {:ok, acc + x}}
...>   x, _ -> {:halt, {:error, {:negative, x}}}
...> end)
{:error, {:negative, -3}}
```

`reduce_while` is the list-shaped version of the same idea: a fold that
short-circuits, for when the number of fallible steps is data-dependent
rather than written out as `with` clauses.

## Exercises

`exercises/08_errors.exs`. Hints:

- `slugify/1`: one pipeline — `String.downcase`, `String.trim`,
  `String.replace(~r/[^a-z0-9]+/, "-")`, then `String.trim("-")`.
- `parse_int/1`: `Integer.parse/1` returns `{int, rest}` or `:error`;
  demand `rest == ""` so `"12abc"` is rejected. Three `case` branches.
- `fetch/2`: wrap `Map.fetch/2` so failure carries the key.
- `unit_cost/1`: a three-clause `with` over `fetch/2` twice and
  `safe_div/2`. Do not add an `else` — the raw failure is the answer.
- `unwrap!/1`: match `{:ok, v}`; otherwise `raise ArgumentError`.
- `traverse/1`: fold with `reduce_while`, or recurse with two clauses.
  It must return the *first* error and stop.

## Leetcode at this stage

Pipelines and `{:ok, _}`/`{:error, _}` are plumbing rather than algorithms,
but these lean on them:

- 8 String to Integer (atoi) — a `with` chain over sign, digits, clamping.
- 65 Valid Number — a sequence of fallible parse steps; `with` beats
  nested `case`.
- 1071 Greatest Common Divisor of Strings — pipeline-friendly.
- 20 Valid Parentheses — `reduce_while` returning `{:error, _}` on the
  first bad close.

Questions before moving on:

1. Check in iex: does `1 + 2 |> Integer.to_string()` give `"3"` or
   `"2"`? What does that tell you about `|>`'s precedence relative to `+`?
2. Rewrite a two-clause `with` as nested `case` by hand, then as two
   `bind` calls. Convince yourself all three are the same term.
3. If clause 2 of a `with` fails, can clause 3's side effect happen? Which
   step of the proof rules it out?
