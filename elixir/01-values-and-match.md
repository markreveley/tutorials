# 01 — Values, atoms, tuples, and `=` as unification

## Concept

Elixir programs compute with **terms**. A term is one of:

```
integer      42  -7  1_000_000  0xff  0b1010      (arbitrary precision)
float        3.14  1.0e-3                          (64-bit IEEE)
atom         :ok  :error  :foo_bar  true  false  nil  MyModule
tuple        {}  {1, 2}  {:ok, "value"}            (fixed size, contiguous)
list         []  [1, 2, 3]  [1 | [2 | []]]         (linked, lesson 4)
binary       "hello"  <<1, 2, 3>>                  (bytes, lesson 9)
map          %{a: 1, "b" => 2}                     (lesson 7)
function     fn x -> x + 1 end                     (lesson 6)
pid, ref     #PID<0.105.0>                         (lesson 10)
```

Every term is **immutable**. Nothing you do to a term changes it; operations
produce new terms.

### Atoms

An atom is a constant whose value is its own name. `:ok` is equal only to
`:ok`. They are interned: comparing two atoms is a pointer compare. `true`,
`false`, `nil` are atoms (`:true == true`). Module names are atoms
(`String == :"Elixir.String"`). Use atoms as tags, enum-like labels, and map
keys. Never create atoms from untrusted input at runtime (they are never
garbage-collected).

### Tuples

A tuple is a fixed-size ordered group. Access is O(1) by index
(`elem(t, 0)`), but "updating" copies the whole tuple, so tuples are for
small fixed-shape records — especially tagged results:

```elixir
{:ok, 42}
{:error, :not_found}
{:point, 3, 4}
```

The convention `{:ok, value} | {:error, reason}` is used everywhere in the
standard library. Lesson 8 treats it formally as a sum type.

### Operators on values

```elixir
1 + 2 * 3          # 7; integer arithmetic is exact
7 / 2              # 3.5  (/ always returns float)
div(7, 2)          # 3
rem(-7, 2)         # -1   (sign follows dividend)
Integer.mod(-7, 2) # 1    (sign follows divisor)
1 == 1.0           # true   (value equality)
1 === 1.0          # false  (strict: type must match too)
:a < :b            # true   (atoms compare by name)
1 < :a             # true   — total order across types:
# number < atom < reference < function < port < pid < tuple < map < list < bitstring
```

The total order across types means `Enum.sort` never fails on mixed lists
and `min`/`max` are always defined. You will rarely rely on it, but it
explains why some sorts "work" unexpectedly.

## Grounding: `=` is not assignment

In C-family languages `x = 5` is an imperative command: store 5 in cell x.
In Elixir, `=` is the **match operator**. `lhs = rhs` means:

> evaluate `rhs` to a term `v`; find a substitution σ for the variables in
> `lhs` such that `lhs[σ] ≡ v`. If one exists, bind those variables and the
> whole expression evaluates to `v`. If none exists, raise `MatchError`.

This is one-sided **unification**: the right side is a ground term (no
variables), the left side is a *pattern* (a term with variables as holes).
A pattern matches a value iff there is a way to fill the holes so the two
terms are structurally identical.

Formally, define `match(p, v)` by structural recursion on the pattern `p`:

```
match(x, v)           = {x ↦ v}                  if x is a variable
match(c, v)           = {}                       if c is a literal and c ≡ v
match(c, v)           = fail                     if c is a literal and c ≢ v
match({p1..pn}, {v1..vn}) = match(p1,v1) ∪ … ∪ match(pn,vn)   (same arity)
match({..}, v)        = fail                     if v is not a tuple of that arity
match([p | ps], [v | vs]) = match(p,v) ∪ match(ps,vs)
match([], [])         = {}
match(_, v)           = {}                       (wildcard binds nothing)
```

Within a single pattern, a variable may appear once; if you need "the same
value in two places" use the pin operator `^x` (compares against the
existing binding) — that is what makes the union in the tuple rule a plain
union rather than needing a consistency check.

Why this matters: matching is *decidable, total, and structural*. It always
terminates (the pattern is finite), it always gives a definite answer, and
the answer depends only on the shape of the terms. That is what makes
pattern matching sound as a basis for control flow (lesson 2).

### Term rewriting view

The whole language can be read as a term-rewriting system. A function
definition

```elixir
def area({:rect, w, h}), do: w * h
```

is a rewrite rule `area({:rect, W, H}) → W * H`. Evaluation is repeatedly
finding a redex (an application whose arguments match a rule's patterns)
and rewriting. Because terms are immutable and rules are pure, the order in
which you rewrite independent redexes does not affect the result — this is
confluence, and lesson 3 shows why it gives you equational reasoning.

## Worked examples

```elixir
iex> x = 1             # pattern `x`, value 1 → bind x := 1
1
iex> 1 = x             # pattern `1`, value 1 → ok, binds nothing
1
iex> 2 = x
** (MatchError) no match of right hand side value: 1

iex> {a, b} = {10, 20} # structural: a := 10, b := 20
{10, 20}
iex> {a, a} = {1, 1}   # a appears twice: compiler treats this as a := 1 then check 1 ≡ 1
{1, 1}
iex> {a, a} = {1, 2}
** (MatchError) no match of right hand side value: {1, 2}

iex> {:ok, v} = {:ok, "file contents"}   # tag acts as a literal check
{:ok, "file contents"}
iex> {:ok, v} = {:error, :enoent}
** (MatchError) no match of right hand side value: {:error, :enoent}

iex> x = 5
iex> ^x = 5            # pin: do not rebind, compare
5
iex> ^x = 6
** (MatchError) no match of right hand side value: 6

iex> {_, second, _} = {1, 2, 3}   # wildcard matches anything, binds nothing
iex> second
2
```

### Rebinding is not mutation

```elixir
iex> x = 1
iex> f = fn -> x end     # closure captures the *value* 1
iex> x = 2               # a new binding named x; the old term 1 is untouched
iex> f.()
1
```

The second `x = 2` does not change anything `f` can see. Lesson 3 makes this
precise.

### Nested matching and destructuring

```elixir
iex> {:user, {name, age}, roles} = {:user, {"ann", 31}, [:admin, :dev]}
iex> name
"ann"
iex> [first_role | _] = roles
iex> first_role
:admin
```

A pattern can be arbitrarily deep; each level is checked by the `match`
rules above.

### Tuples in practice

```elixir
iex> t = {1, 2, 3}
iex> elem(t, 0)
1
iex> put_elem(t, 0, :x)      # returns a new tuple
{:x, 2, 3}
iex> t                       # original unchanged
{1, 2, 3}
iex> tuple_size(t)
3
iex> Tuple.to_list(t)
[1, 2, 3]
```

### Atoms in practice

```elixir
iex> is_atom(:ok)
true
iex> Atom.to_string(:hello)
"hello"
iex> String.to_existing_atom("hello")   # safe: fails if the atom was never seen
:hello
iex> :ok == :ok and true != false
true
```

## Exercises

`exercises/01_basics.exs`. Fill in each function. Hints:

- `swap/1` is a single match: `{a, b} = t`, then build `{b, a}`.
- `classify/1`: use `is_integer/1`, `is_float/1`, `is_atom/1`,
  `is_tuple/1`, `is_list/1`, `is_binary/1` with `cond`.
- `unwrap_ok/1`: match `{:ok, v}` and return `v`; for anything else return
  `:error` — you will need `case`, shown here:

```elixir
case term do
  {:ok, v} -> v
  _        -> :error
end
```

- `point_add/2` and `manhattan/2` work on `{x, y}` tuples.
- `safe_div/2` returns `{:ok, q}` or `{:error, :division_by_zero}`.

## Leetcode at this stage

You can already do problems that are pure arithmetic on fixed-shape data:

- 1480 Running Sum — skip for now; needs lists (lesson 4).
- 9 Palindrome Number — with `Integer.digits/1` and `Enum.reverse/1`
  (peek ahead) or arithmetic with `div`/`rem`.
- 7 Reverse Integer — `div`/`rem` loop by recursion (write it after lesson 4,
  but think about the arithmetic now).
- 1 Two Sum — the tuple `{i, j}` is your answer shape; the algorithm comes
  in lesson 11.

Questions to answer before moving on:

1. Why does `{a, a} = {1, 2}` fail? Trace the `match` rules.
2. Is `x = x + 1` mutation? What does `f` above return if you write it
   after `x = x + 1`?
3. Why can `=` on the left side contain `{:ok, v}` but not `f(v)`? (Hint:
   a pattern must be something `match` can recurse on structurally.)
