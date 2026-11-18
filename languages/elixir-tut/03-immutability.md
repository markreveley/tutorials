# 03 — Immutability, rebinding, referential transparency

## Concept

Every term in Elixir is immutable. There is no operation anywhere in the
language that changes a term in place. Functions that look like mutation
return new terms:

```elixir
iex> t = {1, 2, 3}
iex> put_elem(t, 0, :x)
{:x, 2, 3}
iex> t
{1, 2, 3}                    # unchanged

iex> m = %{a: 1}
iex> Map.put(m, :b, 2)
%{a: 1, b: 2}
iex> m
%{a: 1}                      # unchanged

iex> xs = [2, 3]
iex> [1 | xs]
[1, 2, 3]
iex> xs
[2, 3]                       # unchanged
```

### Rebinding is not mutation

```elixir
x = 1
x = 2
```

This is legal, and it is *not* an assignment to a cell. The second line is a
match of the pattern `x` against the value `2`; since a bare variable in a
pattern is a hole, it binds. The name `x` now refers to a different term. The
term `1` still exists, unchanged, for as long as anything refers to it:

```elixir
iex> x = 1
iex> f = fn -> x end       # the closure captures the value 1
iex> x = 2                 # rebind the *name*
iex> f.()
1                          # the closure is unaffected
iex> x
2
```

Compare a mutable language, where `f` would print 2. Two distinct things are
being conflated in imperative code — "a name for a value" and "a box holding a
value" — and Elixir only has the first.

Erlang, the language underneath, does not allow rebinding at all: you would
have to write `X1`, `X2`, `X3`. Elixir's rebinding is a convenience that keeps
the same property, because each rebinding introduces a *new* binding rather
than writing into an old one. Inside a `case`, `if`, or comprehension body,
rebinding is scoped and does not escape:

```elixir
iex> x = 1
iex> if true, do: (x = 99)
iex> x
1                          # the inner binding died with the block
```

That is why you write `x = if cond, do: a, else: b` instead — everything is an
expression with a value.

## Grounding: nothing else can observe a rebinding

### The model

Give evaluation an environment ρ: a finite map from names to values. Values
are terms, built from constructors; a value has no identity separate from its
structure — there is no address you can write through, no `&x`. The only
operations on ρ are:

```
lookup(ρ, x)   = ρ(x)
extend(ρ, x, v) = ρ[x ↦ v]      -- produces a NEW environment
```

Evaluation is `eval(e, ρ) = v`. The rules that matter:

```
eval(x, ρ)              = ρ(x)
eval(c, ρ)              = c                                     (literal)
eval({e₁,…,eₙ}, ρ)      = {eval(e₁,ρ), …, eval(eₙ,ρ)}
eval(fn -> e end, ρ)    = ⟨closure e, ρ⟩                        (captures ρ)
eval((p = e; rest), ρ)  = eval(rest, ρ ⊎ σ) where p ▷ eval(e,ρ) ⇓ σ
```

The last rule is the whole story about rebinding: a match produces a σ and
evaluation *continues in a new environment* `ρ ⊎ σ` (right-biased union). The
old ρ is not modified; it is simply no longer the environment of the
continuation.

### Theorem 3 (rebinding is unobservable)

*Let `v = eval(e, ρ)`, and let `ρ′ = ρ[x ↦ w]` be any subsequent rebinding.
Then (i) `v` is unchanged by the rebinding, and (ii) any evaluation already in
progress under ρ — a closure awaiting a call, a caller's frame, another
process — still evaluates under ρ and yields exactly what it would have
yielded had the rebinding never happened.*

Stated the practical way: **once a value has been computed and handed to
someone, rebinding a name can never change what they hold.**

**Proof.** Two parts.

*(a) Values do not depend on the environment.* By structural induction on the
value `v` produced by `eval`. `v` is built by the constructor rules above from
literals and from sub-values; none of the value forms — integer, atom, tuple,
cons cell, binary, map — contains a name. The one form that does contain an
environment is a closure `⟨e, ρ⟩`, and it stores the environment *by value* at
creation time, so it contains a fixed finite map, not a reference to a mutable
one. Hence `v` mentions no name that could later be rebound. ∎(a)

*(b) The environment is only ever extended, never updated in place.* The only
rule that changes the environment is the match rule, and it evaluates the
continuation in `ρ ⊎ σ`; every other rule passes ρ down unchanged. Therefore
for any *already-running* evaluation holding some ρ — a closure, a pending
argument, a caller's frame — that ρ is still the same finite map after the
rebinding, because the rebinding constructed a different map for a different
continuation. ∎(b)

Together: the only two ways to observe a change would be a value that names
something mutable (ruled out by (a)) or an environment shared by reference
(ruled out by (b)). ∎

The corollary is worth stating separately because it is what makes the rest of
the course possible.

### Referential transparency

An expression `e` is **referentially transparent** when it can be replaced by
its value anywhere it occurs without changing the meaning of the program.
Precisely:

> If `eval(e, ρ) = v`, then for any context `C[·]`,
> `eval(C[e], ρ) ≡ eval(C[v], ρ)`.

In Elixir this holds for every expression built from pure functions — which is
everything except explicit effects (`send`, `IO`, ETS, process dictionary,
`:rand`). Two consequences you will use constantly:

- **Equals may be substituted for equals.** If `a ≡ b` then `f(a) ≡ f(b)`,
  and any subexpression may be replaced by an equal one, at any depth.
- **Evaluation order does not matter.** Independent redexes can be reduced in
  any order and reach the same normal form (confluence, lesson 1). Sharing a
  computation with a `let` cannot change a result, only how often it is
  performed.

### Equational reasoning: a worked proof

Take these definitions:

```elixir
def scale({x, y}, k), do: {x * k, y * k}
def norm1({x, y}), do: abs(x) + abs(y)
```

**Claim.** ∀ p = {x, y}, ∀ k: `norm1(scale(p, k)) ≡ abs(k) * norm1(p)`.

We reason by rewriting, using each definition as an equation, plus the
arithmetic facts `abs(a*b) = abs(a)*abs(b)` and distributivity.

```
   norm1(scale({x, y}, k))
≡  norm1({x * k, y * k})            -- unfold scale (its clause matched)
≡  abs(x * k) + abs(y * k)          -- unfold norm1
≡  abs(x) * abs(k) + abs(y) * abs(k)   -- abs is multiplicative
≡  abs(k) * (abs(x) + abs(y))       -- distributivity, commutativity
≡  abs(k) * norm1({x, y})           -- FOLD norm1 (the same equation, backwards)
```

∎

Every step replaced a subexpression by an equal one. Three features made this
legal, and all three are consequences of immutability:

1. **Unfolding a call is sound.** `scale({x,y}, k)` may be replaced by its
   body because the clause's pattern matched and the body is the right-hand
   side of a rewrite rule. Nothing else in the program could have been
   affected by the call.
2. **Folding backwards is sound.** The last step used `norm1`'s definition
   right-to-left. An equation may be read in both directions only if the
   function has no effects — otherwise unfolding would duplicate them.
3. **Context is irrelevant.** We rewrote under `+` and under `*` without
   worrying what the surrounding program was doing, because there is no
   surrounding state.

Try the same argument in a language where `scale` might mutate its argument or
increment a counter. Step 1 already fails: the two sides differ in what has
happened to the world.

### Why this makes the induction proofs valid

Lesson 4 proves things like `length(xs ++ ys) = length(xs) + length(ys)` by
induction. The inductive step always has the shape:

```
   f([h | t])
≡  <body of f, with the recursive call f(t) inside>     -- unfold
≡  <body with f(t) replaced by what the IH says it equals>   -- IH + substitution
≡  <the goal>
```

The middle step is *exactly* substitution of equals for equals inside a
context, applied to a recursive call. Without referential transparency the
induction hypothesis would be unusable: knowing "`f(t)` returns `n`" would not
license replacing the call `f(t)` by `n`, because the call might also have
done something. Referential transparency is what turns "the function returns
this value" into "the call *is* this value".

## Worked examples

### Structure sharing

Immutability sounds expensive — surely everything is copied? It is not, and
the reason is that immutable data can be **shared** safely. If nobody can
mutate a term, two structures may point at the same term with no risk.

```elixir
iex> xs = [2, 3]
iex> ys = [1 | xs]      # O(1): allocates ONE cons cell whose tail is xs
iex> :erts_debug.same(tl(ys), xs)
true                    # not a copy — the same memory
```

A list `[1, 2, 3]` is three cons cells:

```
ys ──▶ [1|•] ──▶ [2|•] ──▶ [3|•] ──▶ []
                  ▲
xs ───────────────┘
```

`xs` and `ys` share the tail. Consing is O(1) in time and space; taking `tl`
is O(1) and allocates nothing. This is why the "prepend and reverse at the
end" idiom (lesson 5) is cheap while "append to the end" is not.

Sharing is **shallow**: only what is structurally reachable and unchanged is
shared, and a new cell is allocated exactly for the part that differs.

```elixir
iex> t = {1, 2, 3}
iex> u = put_elem(t, 0, :x)     # tuples are contiguous: the 3-word body IS copied,
                                # but the ELEMENTS are shared, not deep-copied
iex> big = String.duplicate("x", 1_000_000)
iex> pair = {big, 1}
iex> other = put_elem(pair, 1, 2)   # still O(1)-ish: the big binary is shared
```

The rule: copying happens at the level of the container you change, never
below it. `put_elem` on a 3-tuple copies 3 words regardless of how large the
elements are. `Map.put` on a large map copies O(log n) nodes and shares the
rest (lesson 7).

What sharing buys you:

- **No defensive copying.** Passing a list to a function you did not write is
  free and safe. In a mutable language, half of "clean code" advice is about
  who is allowed to mutate what; that entire category of bug is absent.
- **Old versions stay alive for free.** Undo, snapshots, and
  "compare before/after" are just keeping the old reference.
- **Cheap concurrency.** Terms sent between processes need no locks; nothing
  can change under a reader (lesson 10).

The cost you do pay: updating deep inside a structure is O(depth), not O(1),
and array-style random-access mutation is not available. Lesson 7 quantifies
that price for maps.

### The two things `=` is not

```elixir
iex> x = 1
iex> x = x + 1        # NOT mutation: evaluate x+1 to 2, then bind a new x
iex> x
2

iex> list = [1, 2, 3]
iex> _ = List.replace_at(list, 0, :x)   # the result was thrown away...
iex> list
[1, 2, 3]                               # ...so nothing happened at all
```

The second is a real beginner bug: in Elixir, ignoring a return value means
ignoring the entire effect of the call.

## Exercises

`exercises/03_immutability.exs`, module `Immutability`. Hints:

- `rebind/1`: bind `y = n`, then rebind `y` twice, then return `{n, y}`. The
  test asserts `n` came back unchanged — write it and confirm the compiler is
  fine with three bindings named `y`.
- `closure_sees_old_value/1`: build `f = fn -> n end` *before* rebinding `n`.
  This is Theorem 3(a) in executable form.
- `put_elem_pure/3` and `map_put_pure/3`: one line each; the point is that
  returning `{new, original}` is possible at all.
- `cons_shares_tail/2`: `consed = [x | xs]`, then compare `tl(consed)` with
  `xs` using `:erts_debug.same/2` (an Erlang debug function that tests
  identity rather than equality — never use it in real code, but it makes
  sharing visible).
- `square_of_succ/1`: bind `s = n + 1` once and return `s * s`. The `let`
  version and the duplicated version are equal by referential transparency;
  only the number of additions differs.
- `swap_twice/1`: define an anonymous `swap` and apply it twice. Prove on
  paper that `swap ∘ swap ≡ id` by unfolding twice — a two-line version of
  the worked proof above.

## Leetcode at this stage

Nothing new algorithmically; what changes is how you write solutions. Rules to
adopt now, before recursion makes them essential:

- Never reach for a "variable I update in a loop". Compute a new value and
  name it, or pass it as an argument.
- A function that returns nothing is a function that did nothing.
- Problems phrased as "modify the array in place" (e.g. 27 Remove Element,
  283 Move Zeroes) become "return the new list". Read the problem, then
  restate it as a pure transformation before writing any code — that
  restatement is most of the work in functional leetcode.

Questions to answer before moving on:

1. `x = 1; f = fn -> x end; x = 2; f.()` returns 1. Which half of Theorem 3
   is doing the work — (a) or (b)?
2. Is `:rand.uniform/0` referentially transparent? Which step of the worked
   proof would break for a function that calls it?
3. `xs = [1, 2, 3]; ys = [0 | xs]`. How many cons cells exist in total? How
   many were allocated by the second line?
4. Why can two processes hold the same list with no lock?
