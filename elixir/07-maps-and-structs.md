# 07 — Maps, keyword lists, MapSet, structs, and persistence

## Concept

### Maps

A map is an unordered key→value association. Any term may be a key.

```elixir
%{}                             # empty
%{"a" => 1, :b => 2, {1,2} => 3}   # arbitrary keys
%{a: 1, b: 2}                   # sugar for %{:a => 1, :b => 2}
```

```elixir
m = %{a: 1, b: 2}

m[:a]                 # 1     — Access syntax, nil if missing
m.a                   # 1     — strict: KeyError if missing
Map.get(m, :z)        # nil
Map.get(m, :z, 0)     # 0
Map.fetch(m, :a)      # {:ok, 1}
Map.fetch!(m, :z)     # ** (KeyError)
Map.put(m, :c, 3)     # %{a: 1, b: 2, c: 3}
Map.delete(m, :a)     # %{b: 2}
Map.update(m, :a, 0, &(&1 + 1))    # %{a: 2, b: 2}   (default 0 if absent)
Map.update!(m, :z, &(&1 + 1))      # ** (KeyError)   (must exist)
Map.merge(m, %{b: 9, c: 3})        # %{a: 1, b: 9, c: 3}  — right wins
Map.merge(m, other, fn _k, v1, v2 -> v1 + v2 end)   # resolve collisions
Map.keys/values/to_list/map_size/Map.filter/Map.new
%{m | b: 20}          # update-existing-only; raises if :b is absent
```

`%{m | k: v}` is the *update* syntax. It cannot add keys — which is a
feature: it is a typo-catcher, and it is what makes struct updates safe.

### Pattern matching on maps is a SUBSET match

```elixir
iex> %{a: x} = %{a: 1, b: 2, c: 3}
%{a: 1, b: 2, c: 3}
iex> x
1
iex> %{a: 1, z: _} = %{a: 1}
** (MatchError)
```

The pattern `%{a: x}` says "this map has *at least* key `:a`". Contrast
tuples and lists, where the pattern must describe the whole term. The
asymmetry is deliberate: maps are open records, and a subset match lets a
function state only the fields it needs, so adding a field to your data
never breaks existing clauses.

```elixir
def area(%{shape: :circle, r: r}), do: 3.14159 * r * r
def area(%{shape: :rect, w: w, h: h}), do: w * h
# works on %{shape: :rect, w: 2, h: 3, colour: :red, id: 77}
```

Two consequences to internalise: `%{} = anything_map` always matches (the
empty pattern demands nothing), and a variable key needs a pin —
`%{^k => v} = m` — because a pattern key must be a fixed term, not a
binder.

### Keyword lists

A keyword list is a *list* of `{atom, value}` pairs, with sugar:

```elixir
[a: 1, b: 2]  ≡  [{:a, 1}, {:b, 2}]
Keyword.get(kw, :a, 0)
Keyword.put(kw, :c, 3)
```

| | map | keyword list |
|---|---|---|
| keys | any term | atoms only |
| duplicates | no | yes (first wins on `get`) |
| ordered | no | yes, insertion order |
| lookup | O(log₃₂ n) | O(n) |
| pattern match | subset | exact (or awkward) |
| trailing-call sugar | no | `f(x, opt: 1)` |

Use a **keyword list** for options to a function (small, ordered,
duplicates allowed, `do:`/`opt:` sugar — this is why `Enum.sort_by(xs, f,
:desc)` and `String.split(s, ",", trim: true)` look the way they do). Use a
**map** for data, always, once there is more than a handful of entries.

### MapSet

```elixir
s = MapSet.new([1, 2, 3])
MapSet.member?(s, 2)          # true — O(log₃₂ n)
MapSet.put(s, 4)
MapSet.delete(s, 1)
MapSet.union / intersection / difference / subset? / size
MapSet.to_list(s)             # order unspecified — sort if you need order
```

A `MapSet` is a map with `[]` values plus a struct tag. `Enum.uniq/1`
preserves order in O(n) with an internal map; `MapSet` is the right tool
when you need membership tests, not deduplication.

### Structs

```elixir
defmodule User do
  @enforce_keys [:name]
  defstruct [:name, age: 0, roles: []]
end

u = %User{name: "ann"}          # %User{name: "ann", age: 0, roles: []}
u.age                           # 0
%User{u | age: 31}              # new struct
%User{name: n} = u              # matches only Users
is_struct(u, User)              # true
Map.from_struct(u)              # %{name: "ann", age: 0, roles: []}
```

A struct **is a map** with the key `:__struct__ => User` and a
compile-time-fixed key set. That gives you three things a bare map does not
have: typo detection at compile time (`%User{nmae: x}` fails to compile),
dispatch (`%User{} = x` in a pattern, and protocol implementations keyed on
the tag), and documented shape. Structs do not implement `Access` by
default, so `u[:name]` fails — use `u.name`, or `@derive`/implement
`Access` if you really want bracket syntax.

### get_in / put_in / update_in

```elixir
data = %{user: %{name: "ann", scores: %{math: 90}}}

get_in(data, [:user, :name])                 # "ann"
get_in(data, [:user, :missing, :x])          # nil — nil-safe all the way down
put_in(data, [:user, :scores, :math], 95)
update_in(data, [:user, :scores, :math], &(&1 + 1))
put_in(data.user.name, "bea")                # macro form, strict, no list
Access.key(:x, %{}) / Access.at(0) / Access.all()
```

The list form goes through the `Access` behaviour and returns `nil` for
missing intermediate keys; the macro form (`data.user.name`) compiles to
direct field access and raises. Both return a **new** structure — which is
the whole subject of the next section.

## Grounding: persistent data structures

### The requirement

Immutability plus "update" looks contradictory. `Map.put(m, :c, 3)` must
return a map with the new key while `m` still denotes exactly what it did
before — because lesson 3's equational reasoning depends on it. The naive
implementations both fail:

- Mutable hash table: O(1) update, but destroys the old version.
- Copy the whole map: O(n) per update, and O(n) memory per version.

A **persistent** structure gives you both: every operation returns a new
version, all old versions remain valid, and the cost is sublinear because
versions **share structure**.

### Elixir maps are HAMTs

A Hash Array Mapped Trie. For a key `k`, compute `h = hash(k)`, a 32-bit
integer, and read it as a sequence of 5-bit digits (`log₂ 32 = 5`):

```
h = 11010 01100 00011 10111 ...
     d0    d1    d2    d3
```

Each node is an array of up to 32 slots. Digit `d0` selects the slot at the
root, `d1` at depth 1, and so on: the key's hash *is* the path to it. A node
stores a 32-bit bitmap of which slots are occupied plus a dense array of
only those children, so an empty branch costs one bit, not one word.

Depth is therefore ⌈log₃₂ n⌉ for n well-spread keys: 1 level to 32 keys,
2 to 1024, 3 to 32768, 4 to ~10⁶, 5 to ~3·10⁷. Lookup walks that path:
**O(log₃₂ n)** node visits, each an O(1) bitmap-and-index step.

### Path copying

`Map.put(m, k, v)`:

1. Walk from the root along `d0, d1, …` to where `k` belongs.
2. Build a **new** leaf holding `{k, v}`.
3. Build a new node at each level of that path, identical to the old one
   except that one slot now points at the newly built child below.
4. Return the new root.

Every node *not on the path* is not copied — the new root and the old root
share it by pointer. Cost: ⌈log₃₂ n⌉ new nodes, each ≤ 33 words. Everything
else is shared.

```
        old root ────┬──► A ──► ...        (shared subtree, untouched)
                     └──► B
        new root ────┬──► A                 (same pointer as old root's A)
                     └──► B'                (copy of B, one slot changed)
```

**Claim.** After `m2 = Map.put(m1, k, v)`, every lookup in `m1` returns
exactly what it did before.

*Proof.* Lookup of key `j` in `m1` visits the nodes reachable from `m1`'s
root along `hash(j)`'s digits. `Map.put` writes to no existing node: steps
2 and 3 only *allocate* nodes, and step 3 initialises each new node's slots
by copying pointers out of the old one. So the set of nodes reachable from
`m1`'s root, and every field in them, is bit-for-bit what it was. Lookup is
a pure function of that reachable subgraph, hence unchanged. ∎

The proof is short precisely because "no existing node is ever written" is
the entire discipline. It is also why sharing is *safe*: a node that is
never mutated may be pointed at by any number of versions, so no version
needs to defend itself with a copy.

Corollary: `m1` and `m2` together occupy `|m1| + O(log₃₂ n)` words, not
`2·|m1|`. Keeping every intermediate version of a map you fold over costs
O(n log₃₂ n) total, not O(n²).

### Why O(log₃₂ n) is "effectively constant" — and why that is a lie

For n ≤ 10⁶, ⌈log₃₂ n⌉ ≤ 4. The depth is bounded by 7 for any map that fits
in memory. So people say maps are O(1). Be precise about what is true:

- The *number of node visits* is bounded by a small constant in practice.
  That part is fair.
- It is still **Θ(log n)** asymptotically, and the base does not change the
  class.
- The constant hidden per level is not small: each level is a pointer
  dereference into a fresh cache line, and at depth 4 that is 4 likely cache
  misses versus 1 for a flat array — plus, on update, 4 allocations that the
  GC must later trace.

So: treat map operations as O(1) when *choosing an algorithm* (a hash-map
solution to two-sum really is linear-time in the sense leetcode means), and
remember they are not O(1) when *tuning a hot loop* (a tuple or a binary
with O(1) indexing can be several times faster).

Contrast with a mutable hash table: amortised O(1) with occasional O(n)
rehashing, one cache miss, no allocation on update — and no old version. The
BEAM's trade is: give up the constant factor, buy back the ability for
thousands of processes to share the same immutable term with no locks at all
(lesson 10). Persistence is not a tax paid for purity; it is what makes
lock-free concurrency possible.

### The small-map representation

Below and at 32 keys, the BEAM does not use a HAMT at all. A *flatmap* is
two tuples: a sorted key tuple and a parallel value tuple.

```
#{a => 1, b => 2}   ≈   { {:a, :b}, {1, 2} }
```

Consequences you can observe:

- Lookup is a linear scan (or binary search) over ≤ 32 keys — genuinely
  O(1)-bounded, and cache-friendly since both tuples are contiguous.
- Update copies both tuples: O(k) for k ≤ 32 keys, still a bounded constant.
- Small maps with the same key set share the key tuple, so a list of 10⁶
  records `%{name: _, age: _}` stores the key names once.
- Two maps with equal contents compare equal in O(k) directly.
- At the 33rd key the map is converted to a hashmap; the conversion is O(n)
  and happens once.
- Because a struct's key set is fixed and usually small, structs are almost
  always flatmaps — one more reason to prefer them for records.

You never choose the representation; the VM does. But it explains why a
micro-benchmark on 10-key maps tells you nothing about 10⁵-key maps.

## Worked examples

```elixir
iex> freq = Enum.reduce(~w(a b a c a), %{}, fn w, acc ->
...>   Map.update(acc, w, 1, &(&1 + 1))
...> end)
%{"a" => 3, "b" => 1, "c" => 1}
iex> Enum.max_by(freq, fn {_k, v} -> v end)
{"a", 3}
```

`Map.update/4` with a default is *the* counting idiom; `Enum.frequencies/1`
is the same thing in the standard library.

```elixir
iex> users = [%{name: "ann", status: :active}, %{name: "bo", status: :banned}]
iex> for %{status: :active, name: n} <- users, do: n     # pattern as filter
["ann"]
```

The generator pattern is a subset match, so it both filters (wrong status
is skipped, not an error) and destructures.

```elixir
iex> Map.merge(%{a: 1, b: 2}, %{b: 10, c: 5}, fn _k, x, y -> x + y end)
%{a: 1, b: 12, c: 5}
iex> defmodule P do defstruct x: 0, y: 0 end
iex> p = %P{x: 1, y: 2}
iex> q = %P{p | x: 10}       # p is untouched; q shares nothing it needs to
iex> {p.x, q.x}
{1, 10}
iex> %P{nmae: 1}
** (CompileError) unknown key :nmae for struct P
```

```elixir
iex> db = %{users: %{1 => %{name: "ann", tags: [:admin]}}}
iex> get_in(db, [:users, 1, :name])
"ann"
iex> update_in(db, [:users, 1, :tags], &[:new | &1])
%{users: %{1 => %{name: "ann", tags: [:new, :admin]}}}
iex> get_in(db, [:users, 99, :name])
nil
```

Each `update_in` copies exactly the spine `db → :users → 1 → :tags` — three
nodes — and shares everything else with `db`.

## Exercises

`exercises/07_maps.exs`, module `Maps`. Hints:

- `get_or/3`: `Map.get/3` — one line, but note it is not `map[key] || default`
  (that is wrong when the stored value is `false` or `nil`).
- `bump/2`: `Map.update/4` with default `1`. Watch the default: it is the
  value used when the key is *absent*, not the starting point for the
  function.
- `frequencies/1`: `Enum.reduce/3` over `bump/2`. Do not call
  `Enum.frequencies/1`.
- `merge_sums/2`: `Map.merge/3` with a conflict resolver.
- `unique/1`: `MapSet.new` then `MapSet.to_list` then sort — `MapSet` order
  is unspecified, so the sort is required for a deterministic test.
- `active_names/1`: a comprehension whose generator pattern is
  `%{status: :active, name: n}`. No `Enum.filter`.
- `move/3`: takes a `%Maps.Point{}` (defined for you at the top of the file)
  and returns a new one via `%Maps.Point{p | ...}`.
- `deep_put/3`: `put_in/3` with a path list. Think about which nodes get
  copied.

## Leetcode at this stage

- 1 Two Sum — now do it properly: one pass, a map from value → index,
  looking for `target - x` *before* inserting `x`. O(n).
- 217 Contains Duplicate — `MapSet` size vs list length, one pass.
- 242 Valid Anagram — compare `Enum.frequencies/1` of both.
- 383 Ransom Note — frequency map subtraction.
- 771 Jewels and Stones — `MapSet` of jewels, count stones.
- 349 / 350 Intersection of Two Arrays I & II — `MapSet.intersection` for I,
  frequency maps for II (multiplicities matter).
- 705 Design HashSet — implement it *over* a map, and say what persistence
  buys and costs you versus the array-of-buckets the problem expects.
