# 06 — Enum, Stream, higher-order functions, and the fold laws

## Concept

You will almost never write the recursion of lesson 5 by hand again. `Enum`
has it, once, correct.

```elixir
Enum.map([1, 2, 3], fn x -> x * 2 end)      # [2, 4, 6]
Enum.filter(1..10, fn x -> rem(x, 2) == 0 end)
Enum.reduce([1, 2, 3], 0, fn x, acc -> acc + x end)   # 6
Enum.sum([1, 2, 3])                          # 6
Enum.sort([3, 1, 2])                         # [1, 2, 3]
Enum.sort_by(words, &String.length/1)
Enum.uniq([1, 1, 2])                         # [1, 2]
Enum.zip([1, 2], [:a, :b])                   # [{1, :a}, {2, :b}]
Enum.with_index([:a, :b])                    # [{:a, 0}, {:b, 1}]
Enum.group_by(1..6, &rem(&1, 3))             # %{0 => [3, 6], 1 => [1, 4], 2 => [2, 5]}
Enum.chunk_every([1, 2, 3, 4, 5], 2)         # [[1, 2], [3, 4], [5]]
Enum.take_while([1, 2, 9, 1], &(&1 < 5))     # [1, 2]
Enum.frequencies(~w(a b a))                  # %{"a" => 2, "b" => 1}
Enum.all?/any?/find/count/min_by/max_by/split/flat_map/reduce_while
```

`Enum` works on anything implementing the `Enumerable` protocol: lists,
ranges, maps, `MapSet`, `Stream`, `File.stream!`.

### Anonymous functions and `&`

```elixir
fn x -> x * 2 end                # a lambda
fn x, y -> x + y end
fn                               # multi-clause, patterns and all
  {:ok, v}    -> v
  {:error, _} -> :default
end
```

Calling needs a dot: `f.(3)`. The dot is not decoration — `f` is a *value*
bound to a variable, and `f(3)` would mean "call the named function f/1 in
this module". The two namespaces are separate.

The **capture operator** `&` is sugar:

```elixir
&(&1 * 2)              ≡  fn x -> x * 2 end
&(&1 + &2)             ≡  fn x, y -> x + y end
&String.length/1       ≡  fn s -> String.length(s) end
&Kernel.>=/2           ≡  fn a, b -> a >= b end
&[&1 | &2]             ≡  fn h, t -> [h | t] end
&{&1, &2}              ≡  fn a, b -> {a, b} end
```

`&Mod.fun/arity` captures an existing named function; `&(expr)` builds one,
where `&1`, `&2` are positional holes. `&(&1)` is a compile error — the
captured expression must be a call or a container, not a bare hole; for
identity write `fn x -> x end`.

### Enum is eager, Stream is lazy

```elixir
1..5 |> Enum.map(&(&1 * 2)) |> Enum.filter(&(&1 > 4))
# builds [2,4,6,8,10], then builds [6,8,10]      — 2 intermediate lists

1..5 |> Stream.map(&(&1 * 2)) |> Stream.filter(&(&1 > 4)) |> Enum.to_list()
# builds nothing until Enum.to_list; then one element at a time
```

A `Stream` is a value describing a computation, not a computation performed.
`Stream.map/2` returns a `%Stream{}` struct immediately. Nothing runs until
a *terminal* `Enum` function (`to_list`, `reduce`, `sum`, `take`,
`Enum.each`) pulls on it.

### Comprehensions

```elixir
for x <- 1..5, do: x * x                       # [1, 4, 9, 16, 25]
for x <- 1..20, rem(x, 3) == 0, do: x          # generator + filter
for x <- 1..3, y <- 1..3, x < y, do: {x, y}    # nested generators
for {:ok, v} <- results, do: v                 # pattern in generator = filter
for x <- 1..5, into: %{}, do: {x, x * x}       # collect into anything
for <<b <- "abc">>, do: b                      # binary generator (lesson 9)
```

A `for` is not a loop; it is a *collection builder*. A generator whose
pattern fails simply skips that element — no `MatchError`. `into:` accepts
any `Collectable` (`%{}`, `MapSet.new()`, `""`, an open file).

## Grounding: folds

### Definitions

For lists, defined by `[] | [h | t]`:

```
foldr(f, z, [])       = z
foldr(f, z, [h | t])  = f(h, foldr(f, z, t))

foldl(f, z, [])       = z
foldl(f, z, [h | t])  = foldl(f, f(z, h), t)
```

`foldr` replaces the list's own constructors: it rewrites
`[a, b, c] ≡ a : (b : (c : []))` into `f(a, f(b, f(c, z)))`. That is the
sense in which `foldr` *is* the list — it is the type's induction principle
turned into a function.

`Enum.reduce/3` is `foldl` with the accumulator first:
`Enum.reduce(xs, z, fn x, acc -> f.(acc, x) end)`. There is no `Enum.foldr`;
`List.foldr/3` exists, and `foldr(f, z, xs) ≡ foldl(flip f, z, reverse(xs))`
covers the rest.

### map is a fold

**Claim.** `map(f, xs) ≡ foldr(fn h, acc -> [f.(h) | acc] end, [], xs)`.

Write `g = fn h, acc -> [f.(h) | acc] end`. Induction on `xs`:

- Base: `map(f, []) = []` and `foldr(g, [], []) = []`. ✓
- Step, IH `map(f, t) ≡ foldr(g, [], t)`:

  ```
  map(f, [h | t]) = [f.(h) | map(f, t)]        (definition of map)
                  = [f.(h) | foldr(g, [], t)]  (IH)
                  = g(h, foldr(g, [], t))       (definition of g)
                  = foldr(g, [], [h | t])       (definition of foldr)
  ```
  ✓ ∎

### filter is a fold

**Claim.** `filter(p, xs) ≡ foldr(fn h, acc -> if p.(h), do: [h | acc], else: acc end, [], xs)`.

Same shape. Base is `[] = []`. Step: `filter(p, [h|t])` is `[h | filter(p,t)]`
when `p.(h)`, else `filter(p, t)`; the fold's `g(h, foldr(g, [], t))` is
`[h | foldr(g,[],t)]` when `p.(h)`, else `foldr(g,[],t)`. Apply the IH to
both branches. ✓ ∎

Length is a fold (`fn _, n -> n + 1 end`, 0). Append is a fold
(`foldr(&[&1 | &2], ys, xs) ≡ xs ++ ys`). Reverse is a fold
(`foldl(fn acc, h -> [h | acc] end, [], xs)`). Every list function you have
written so far is a fold.

### Fold universality

**Theorem (universal property of foldr).** For a function `h` on lists,

```
h([]) ≡ z  ∧  ∀ x, xs. h([x | xs]) ≡ f(x, h(xs))     ⟺     h ≡ foldr(f, z, ·)
```

*Proof.* (⇐) is the definition of `foldr`. (⇒) by induction on the argument:
base `h([]) = z = foldr(f, z, [])`; step
`h([x | xs]) = f(x, h(xs)) = f(x, foldr(f, z, xs)) = foldr(f, z, [x | xs])`,
using the IH in the middle. ∎

Read the left-hand side: it says exactly "`h` is defined by structural
recursion on a list". So **every structurally recursive list function is a
fold**, and the two equations *uniquely determine* it. That uniqueness is
the useful half: to prove two list functions equal, show they satisfy the
same pair of equations. No induction needed at the call site — it was done
once, here.

### Instance: sum is the unique fold

`sum([]) = 0` and `sum([x | xs]) = x + sum(xs)`. Take `z = 0`, `f = &+/2`.
The theorem's left side holds by definition, so `sum ≡ foldr(&+/2, 0, ·)`,
directly — no fresh induction. And by lesson 5's foldl/foldr theorem (`+`
is associative with unit 0), `sum ≡ foldl(&+/2, 0, ·) ≡ Enum.reduce(·, 0, &+/2)`,
which is the tail-recursive one. Two lines of reasoning replaced two
inductions.

### The fusion law

**Theorem.** ∀ f, g. `map(f) ∘ map(g) ≡ map(f ∘ g)`.

*Proof* by induction on `xs`, where `(f ∘ g).(x) = f.(g.(x))`:

- Base: `map(f, map(g, [])) = map(f, []) = []` and `map(f ∘ g, []) = []`. ✓
- Step, IH `map(f, map(g, t)) ≡ map(f ∘ g, t)`:

  ```
  map(f, map(g, [h | t]))
    = map(f, [g.(h) | map(g, t)])         (map on the inner list)
    = [f.(g.(h)) | map(f, map(g, t))]     (map on the outer list)
    = [(f ∘ g).(h) | map(f ∘ g, t)]       (IH, and definition of ∘)
    = map(f ∘ g, [h | t])                 (definition of map)
  ```
  ✓ ∎

This is a *licence to refactor*. `xs |> Enum.map(&f/1) |> Enum.map(&g/1)`
traverses twice and allocates an intermediate list; the fused version does
one traversal and no intermediate. The compiler will not do this for you
(the functions may be arbitrary), so you do it, and the theorem says the
result is the same program. Related laws, all provable the same way:

```
filter(p) ∘ filter(q)  ≡  filter(fn x -> p.(x) and q.(x) end)
map(f) ∘ filter(p)     ≡  filter-then-map, never map-then-filter-on-f's-output
reduce ∘ map(f)        ≡  reduce with f applied in the reducer
length ∘ map(f)        ≡  length                          (map preserves shape)
reverse ∘ reverse      ≡  id                              (lesson 4)
```

### When Stream actually saves memory

Take `xs` of length n, and

```elixir
xs |> Enum.map(f) |> Enum.filter(p) |> Enum.take(3)
```

`Enum.map` allocates a full list of n cells. `Enum.filter` allocates up to n
more. Peak live memory: **O(n)** extra beyond the input, and n calls to `f`
even though at most 3 results are wanted.

```elixir
xs |> Stream.map(f) |> Stream.filter(p) |> Enum.take(3)
```

`Enum.take(3)` drives the pipeline element by element: pull `x₁`, apply `f`,
test `p`, keep or drop; then `x₂`; and halt via `{:halt, acc}` the moment 3
have been kept. At any instant exactly one element is in flight, so extra
memory is **O(1)** (the output list of 3 is O(1) in n), and `f` runs at most
until the third hit.

The rule follows from that argument, and so do its limits:

- Stream wins when the source is huge or **infinite**
  (`Stream.iterate/2`, `Stream.cycle/1`), or the consumer stops early
  (`take`, `find`, `any?`), or the source is I/O (`File.stream!`).
- Stream loses on short lists: each element pays a closure call per stage,
  and there is no intermediate list to be saved. `Enum` on a 100-element
  list is faster.
- Stream cannot help a stage that must see everything: `Enum.sort` in the
  middle of a stream forces the whole thing into memory anyway.

```elixir
iex> Stream.iterate(1, &(&1 * 2)) |> Stream.filter(&(rem(&1, 3) == 1)) |> Enum.take(4)
[1, 4, 16, 64]          # an infinite source, finite work
```

### λ-calculus connection

`fn x -> e end` is λx.e; `f.(a)` is application; β-reduction is
`(fn x -> e end).(a) → e[x := a]`, and because Elixir is pure, β-reduction
is *sound as an equation* — you may substitute in either direction (this is
lesson 3's equational reasoning again).

A closure is the pair (code, environment) needed because `e` may mention
variables bound outside:

```elixir
iex> add = fn x -> fn y -> x + y end end     # λx.λy.x+y  — curried
iex> add5 = add.(5)                          # a closure capturing x := 5
iex> add5.(3)
8
```

Elixir captures **by value**, and values are immutable, so a closure can
never observe a later change (lesson 1's rebinding example). That is why
higher-order code here has none of the "captured loop variable" hazards of
imperative languages. Note also that `add5` is genuine partial application
by currying — Elixir functions are not auto-curried, `&f(1, &1)` is how you
partially apply an existing named function.

## Worked examples

```elixir
iex> 1..10 |> Enum.filter(&(rem(&1, 2) == 0)) |> Enum.map(&(&1 * &1)) |> Enum.sum()
220

iex> Enum.reduce([3, 1, 4, 1, 5], fn x, acc -> max(x, acc) end)   # /2: first elem is z
5

iex> words = ~w(apple fig banana kiwi)
iex> Enum.group_by(words, &String.length/1)
%{3 => ["fig"], 4 => ["kiwi"], 5 => ["apple"], 6 => ["banana"]}

iex> Enum.reduce([1,2,3,4], {0, 0}, fn x, {s, c} -> {s + x, c + 1} end)  # two accs
{10, 4}

iex> Enum.reduce_while(1..1000, 0, fn x, acc ->
...>   if acc > 20, do: {:halt, acc}, else: {:cont, acc + x}
...> end)
21
```

`reduce_while` is early exit for folds: `{:cont, acc}` continues,
`{:halt, acc}` stops and returns `acc`.

### Everything from reduce

```elixir
iex> my_map = fn xs, f -> xs |> Enum.reduce([], &[f.(&1) | &2]) |> Enum.reverse() end
iex> my_map.([1,2,3], &(&1 + 1))
[2, 3, 4]
iex> my_filter = fn xs, p -> Enum.reduce(xs, [], fn x, a -> if p.(x), do: [x|a], else: a end) end
iex> my_filter.([1,2,3,4], &(rem(&1,2)==0)) |> Enum.reverse()
[2, 4]
```

### Fusion, measured

```elixir
iex> xs = Enum.to_list(1..1_000_000)
iex> :timer.tc(fn -> xs |> Enum.map(&(&1 + 1)) |> Enum.map(&(&1 * 2)) |> Enum.sum() end)
iex> :timer.tc(fn -> xs |> Enum.map(&((&1 + 1) * 2)) |> Enum.sum() end)
```

The fused version is faster and allocates one list fewer. The theorem says
it also computes the same answer.

## Exercises

`exercises/06_enum.exs`, module `Folds`. Hints:

- `sum/1`: `Enum.reduce/3`, not `Enum.sum/1` — the point is the fold.
- `map/2` and `filter/2`: build with `Enum.reduce/3` and one final
  `Enum.reverse/1`. Do not call `Enum.map/2` or `Enum.filter/2`.
- `foldr/3`: `foldr(f, z, xs)` with `f.(h, acc)`. Either write the body
  recursion directly, or use `Enum.reduce` over the reversed list — say
  which and why.
- `compose/2`: returns a function. `compose(f, g).(x) == f.(g.(x))`.
- `evens_squared/1`: one comprehension with a filter — no `Enum` calls.
- `pairs_summing_to/2`: two generators, `i < j` on *indices* so each pair is
  reported once; return `{i, j}` index pairs sorted ascending. This is
  brute-force two-sum (leetcode 1) — lesson 7 makes it O(n).
- `first_n_matching/3`: `Stream.iterate/2` or `Stream.filter/2` over an
  infinite source plus `Enum.take/2`. It must terminate on an infinite
  stream, so no `Enum` before the `take`.

## Leetcode at this stage

- 1 Two Sum — brute force with a comprehension now; hash map in lesson 7.
- 1470 Shuffle the Array — `Enum.zip` + `Enum.flat_map`.
- 1512 Number of Good Pairs — a comprehension over index pairs, or
  `Enum.frequencies` + a fold.
- 1913 Maximum Product Difference — `Enum.sort` then take ends.
- 1672 Richest Customer Wealth — `Enum.map(&Enum.sum/1) |> Enum.max()`.
- 1732 Find the Highest Altitude — `Enum.scan/2` (a fold that keeps every
  intermediate) then `Enum.max`.
- 561 Array Partition — sort, `Enum.chunk_every(2)`, sum the minima.
- 1281 Subtract the Product and Sum of Digits — `Integer.digits` + two folds.
