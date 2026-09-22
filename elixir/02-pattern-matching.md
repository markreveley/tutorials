# 02 — Patterns, guards, multi-clause functions

## Concept

A **pattern** is a term with holes. The holes are variables and `_`. Lesson 1
introduced `match(p, v)`; this lesson makes patterns the primary control-flow
mechanism of the language.

Patterns are not a special form of expression — they appear anywhere the
language needs to ask "what shape is this?":

```elixir
{a, b} = pair                          # the = operator
def area({:rect, w, h}), do: w * h     # a function head
case term do {:ok, v} -> v end         # case
for {k, v} <- pairs, do: k             # comprehension generators
with {:ok, v} <- fetch(x), do: v       # with
receive do {:msg, m} -> m end          # mailbox (lesson 10)
```

### Destructuring

```elixir
{:point, x, y} = {:point, 3, 4}        # tuple: arity and every element
[h | t] = [1, 2, 3]                    # h = 1, t = [2, 3]
[a, b | rest] = [1, 2, 3, 4]           # a = 1, b = 2, rest = [3, 4]
%{name: n} = %{name: "ann", age: 31}   # map: n = "ann"
<<first, rest::binary>> = "hello"      # first = ?h, rest = "ello"
<<"GET ", path::binary>> = "GET /x"    # literal prefix, path = "/x"
%User{id: id} = user                   # struct (lesson 7)
```

Tuples and lists match **exactly**: `{a, b}` never matches a 3-tuple, `[a, b]`
never matches a 3-element list. Maps match **partially**: `%{name: n}` matches
any map with at least the key `:name`, and `%{}` matches *every* map. The
asymmetry follows from the types. A tuple's arity and a list's spine are part
of its structure, so a pattern naming a different arity would describe a
different term; a map is a finite function from keys to values, where "does it
send `:name` to something?" is a well-formed question about part of the term.

### Wildcards and pins

`_` matches anything and binds nothing. `_name` binds but silences the
"unused variable" warning. `^x` is the **pin operator**: it means "the value
already bound to `x`", so `^x` behaves as a literal rather than as a hole.

```elixir
x = 1
^x = 1                  # ok: compares
^x = 2                  # ** (MatchError)
[^x | t] = [1, 2, 3]    # t = [2, 3]
```

Without the pin, `x = 2` would silently rebind. The rule of thumb: a bare
variable in a pattern is a *question* ("call this thing x"); a pinned variable
is an *assertion* ("this must equal x").

### Guards

A clause may carry a `when` guard, tested after the pattern matches:

```elixir
def sign(n) when n < 0,  do: :negative
def sign(n) when n == 0, do: :zero
def sign(n) when is_number(n), do: :positive
```

Only a fixed vocabulary is allowed in a guard: comparisons
(`== != === !== < <= > >=`), `and`/`or`/`not`, arithmetic
(`+ - * / div rem abs trunc round floor ceil`), the `is_*` type tests
(`is_atom is_binary is_integer is_list is_map is_number is_tuple`, …), the
size and access primitives (`map_size tuple_size byte_size bit_size length
hd tl elem binary_part is_map_key`), `in` over a literal range or list, and
macros built from those (`defguard`).

Everything else — your own functions, `String.length/1`, `Enum.map/2`,
`IO.puts/1`, `send/2` — is rejected at compile time. "Why guards are
restricted", below, argues that this is the point rather than a limitation.

### Multi-clause functions

A function with several clauses is **case analysis on the shape of its
arguments**. Clauses are tried top to bottom; the first whose pattern matches
*and* whose guard is true wins.

```elixir
def describe([]),       do: :empty_list
def describe([_]),      do: :one_element_list
def describe([_ | _]),  do: :longer_list
def describe(t) when is_tuple(t), do: :tuple
def describe(_),        do: :other
```

Order matters and overlap is normal. `[_]` is subsumed by `[_ | _]`, so
swapping those two clauses would make `:one_element_list` unreachable. The
discipline is **specific first, general last**. If no clause matches you get a
`FunctionClauseError` — a missing case is a crash, not a silent `nil`.

### `case`, `cond`, `if`

`case` is multi-clause dispatch on one value; `cond` picks the first clause
whose *expression* is truthy, for conditions that are not about shape:

```elixir
case File.read(path) do
  {:ok, body} -> body
  {:error, :enoent} -> ""
  {:error, reason} -> raise "read failed: #{inspect(reason)}"
end
cond do
  n < 0  -> :negative
  n == 0 -> :zero
  true   -> :positive     # `true` is the else branch; without it, CondClauseError
end
```

`if`/`unless` are macros that expand to `case`:

```elixir
if c, do: a, else: b   ==>   case c do
                               x when x in [false, nil] -> b
                               _ -> a
                             end
```

`cond` is likewise a nest of two-armed `case`s. So there is exactly one
branching primitive in the language, and it is pattern matching.

## Grounding: matching as an inference system

Write the judgement

```
p ▷ v ⇓ σ        "pattern p matches value v, producing substitution σ"
```

where σ is a finite map from variables to values. Assume patterns are
**linear** (each variable occurs at most once); a repeated variable `{a, a}` is
sugar for `{a, ^a}`, handled by the pin rule. Let ρ be the ambient environment
that pins are resolved in. The rules, one per pattern form:

```
────────────────  (Var)          ──────────────  (Wild)
 x ▷ v ⇓ {x ↦ v}                  _ ▷ v ⇓ {}

  c ≡ v                            ρ(x) ≡ v
──────────────  (Lit)           ──────────────  (Pin)
 c ▷ v ⇓ {}                       ^x ▷ v ⇓ {}

 p₁ ▷ v₁ ⇓ σ₁   …   pₙ ▷ vₙ ⇓ σₙ
────────────────────────────────────────────  (Tup)
 {p₁,…,pₙ} ▷ {v₁,…,vₙ} ⇓ σ₁ ∪ … ∪ σₙ

────────────  (Nil)        p ▷ v ⇓ σ₁    ps ▷ vs ⇓ σ₂
 [] ▷ [] ⇓ {}            ──────────────────────────────  (Cons)
                           [p | ps] ▷ [v | vs] ⇓ σ₁ ∪ σ₂

 k₁,…,kₙ ∈ keys(m)     p₁ ▷ m[k₁] ⇓ σ₁   …   pₙ ▷ m[kₙ] ⇓ σₙ
───────────────────────────────────────────────────────────────  (Map)
 %{k₁ => p₁, …, kₙ => pₙ} ▷ m ⇓ σ₁ ∪ … ∪ σₙ
```

Binary patterns follow the same shape, recursing on a byte/bit prefix and the
remaining bitstring. **Failure is defined negatively**: `p` fails to match `v`
exactly when no derivation of `p ▷ v ⇓ σ` exists. There is no rule that
concludes failure, and no rule that inspects anything but the outermost
constructor of `p` and `v`.

The (Tup) rule takes a plain union: linearity guarantees the σᵢ have disjoint
domains, so no consistency check is needed — exactly what the pin buys us.

### Theorem 1 (determinism)

*For all p and v, there is at most one σ with `p ▷ v ⇓ σ`.*

**Proof.** By structural induction on `p`.

- `p` a variable, `_`, a literal, or `^x`: at most one rule applies (the rules
  are distinguished by the syntactic form of `p`), and each concludes a unique
  σ — `{x ↦ v}`, `{}`, `{}`, `{}` respectively.
- `p = {p₁,…,pₙ}`: only (Tup) applies, and only when `v` is a tuple of arity
  `n`; then `v₁,…,vₙ` are determined by `v`. By the induction hypothesis each
  `σᵢ` is unique, hence so is the union.
- `p = [p′ | ps]`: only (Cons) applies, and only when `v = [v′ | vs]`, which
  determines `v′` and `vs` uniquely. Apply the induction hypothesis to `p′`
  and to `ps` — both strict subterms of `p`.
- `p = []`: only (Nil), σ = {}.
- `p` a map pattern: the keys `kᵢ` are literals fixed by `p`, so each `m[kᵢ]`
  is determined by `v`; apply the induction hypothesis to each `pᵢ`.

In every case the conclusion is forced. ∎

### Theorem 2 (termination)

*The search for a derivation of `p ▷ v ⇓ σ` terminates.*

**Proof.** Each rule's premises mention only **proper subterms of the pattern**:
(Tup) recurses on `p₁,…,pₙ`, (Cons) on `p′` and `ps`, (Map) on `p₁,…,pₙ`. The
axioms (Var), (Wild), (Lit), (Pin), (Nil) have no premises. Patterns are
finite terms written in the source, so the recursion is well-founded on the
size of `p` (an integer that strictly decreases at every step and is bounded
below by 0). Hence every derivation attempt has finite depth and finite
branching, and the search halts. ∎

Note what termination does *not* depend on: the value. `v` may be a large or
even a cyclic-looking structure; the pattern is what bounds the work. This is
also the complexity statement — matching is O(size of p), not O(size of v).

**Corollary.** Matching is a total decision procedure: for any `p` and `v` it
halts and returns either a unique σ or failure. That is the licence to use it
as the branching primitive.

### Why guards are restricted

Clause selection is now definable. Given clauses `(p₁, g₁, e₁), …, (pₙ, gₙ, eₙ)`
and argument `v`:

```
choose(v) = the least i such that  pᵢ ▷ v ⇓ σ  and  gᵢ[σ] ⇓ true
```

and the clause body `eᵢ[σ]` is evaluated. If no such `i` exists, raise
`FunctionClauseError`. Determinism of `choose` follows from Theorem 1 plus
"least `i`".

For this definition to be a *decision procedure*, evaluating `gᵢ[σ]` must be
total and effect-free. Guards are restricted to a vocabulary of primitives
that are exactly that:

1. **Total.** A guard cannot diverge — there is no recursion or unbounded
   iteration in the guard language — so `choose(v)` always terminates. If
   guards could call arbitrary functions, deciding which clause runs would be
   undecidable in general.
2. **Effect-free.** Guards for clauses that are *not* selected are still
   evaluated. If a guard could `send/2` or write to a process dictionary, a
   rejected clause would leave traces, and clause order would be observable in
   the outside world. Matching would stop being a pure question about shape.
3. **Failure means "no", not "boom".** An exception raised inside a guard is
   caught and turned into `false`, so the next clause is tried:
   `def f(x) when hd(x) == 1` simply does not match `f(:atom)`. That
   silent-failure rule is only sane because a guard cannot do anything worth
   observing on its way to failing.
4. **Implementable everywhere.** Guards also run in `receive` clauses and in
   ETS match specifications, compiled to a tiny instruction set and executed
   outside your process. A guard language that could call user code could not
   live there.

The price is that "is this a valid ISBN?" cannot be a guard. Compute the
answer first and match on the result — the functionally honest shape anyway.

## Worked examples

```elixir
iex> %{name: n} = %{name: "ann", age: 31}   # partial: :age is not mentioned
iex> n
"ann"
iex> %{} = %{a: 1}                      # the empty map pattern matches any map
%{a: 1}
iex> %{a: 1} = %{}                      # ...but not the other way round
** (MatchError) no match of right hand side value: %{}
```

Pin versus rebind:

```elixir
iex> expected = 42
iex> {:score, ^expected} = {:score, 42}    # assertion
{:score, 42}
iex> {:score, expected} = {:score, 7}      # question — rebinds!
iex> expected
7
```

Clause ordering, and what goes wrong — `def f(_x), do: :anything` followed by
`def f(0), do: :zero` makes the second clause unreachable, and the compiler
says so: *this clause for f/1 cannot match because a previous clause always
matches*.

Guards fail quietly — an exception inside a guard means "no", not "boom":

```elixir
def first(xs) when hd(xs) > 0, do: :positive_head
def first(_), do: :other

iex> first([1, 2])
:positive_head
iex> first([])       # hd([]) raises inside the guard → guard is false → next clause
:other
iex> first(:nope)    # same story
:other
```

Binary patterns:

```elixir
iex> <<first, rest::binary>> = "hello"
iex> {first, rest}
{104, "ello"}                      # 104 is ?h — a byte, not a string
iex> <<"GET ", path::binary>> = "GET /users"
iex> path
"/users"
iex> <<a::4, b::4>> = <<0xAB>>     # bit-level: two nibbles
iex> {a, b}
{10, 11}
```

One `case` over one argument is almost always better written as clauses —
`def area({:rect, w, h}), do: w * h` and friends. Same dispatch, and it reads
as the rewrite-rule list from lesson 1, which is what it is.

## Exercises

`exercises/02_patterns.exs`, module `Patterns`. Hints:

- `head_or/2`: two clauses, `[h | _]` and `[]`. The order does not matter
  here; convince yourself why.
- `describe/1`: order matters a lot. `[_]` before `[_ | _]`; `{:ok, _}` before
  the `is_tuple/1` clause. `%{}` matches *every* map, so distinguish the empty
  one with a `map_size(m) == 0` guard.
- `sign/1`: three guarded clauses. The last needs `is_number/1` so `sign(:a)`
  raises `FunctionClauseError` rather than answering `:positive`.
- `pinned?/2`: `case value do ^target -> true; _ -> false end` — structural
  equality for free, at any depth.
- `full_name/1`: most specific map pattern first, then the single-key ones,
  then a catch-all `_`.
- `first_byte/1`: `<<b, _::binary>>` and `<<>>`. A byte is an integer.
- `method_and_path/1`: literal binary prefixes, `<<"GET ", path::binary>>`;
  `"GET " <> path` is the same pattern written with sugar.

## Leetcode at this stage

Shape-dispatch problems, before you have recursion over lists:

- 2235 Add Two Integers — one clause; use it to get the workflow going.
- 1281 Subtract the Product and Sum of Digits — with `Integer.digits/1`.
- 13 Roman to Integer — the pairwise cases are multi-clause matching on
  `<<a, b, rest::binary>>`; write the clause list now, finish after lesson 4.
- 20 Valid Parentheses — the push/pop rules are four clauses over
  `{char, stack}`; again, the recursion comes in lesson 4.

Questions to answer before moving on:

1. Why does `%{}` match every map, while `{}` matches only the empty tuple?
2. `def f(x, x)` compiles. What does it mean, and which rule above explains it?
3. Why is `def f(x) when g(x)` rejected for a user-defined `g`, even if `g` is
   provably total?
4. Write out the derivation tree for `{:ok, [h | t]} ▷ {:ok, [1, 2]}`.
