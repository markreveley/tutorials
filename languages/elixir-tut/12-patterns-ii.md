# 12 — Trees, graphs, BFS/DFS, DP as memoisation, heaps

## Concept

Lesson 11 dealt with linear data. What is left is *branching* — trees, graphs,
recursion with overlapping subproblems, priority queues. Imperative versions
are held together by mutation: a `visited` array you flip, a `dp` table you
fill, a heap you sift in place. One technique replaces all of it:

> **State threading.** A function that would mutate shared state instead
> *takes that state as an argument and returns the updated copy* alongside
> its result. `f(x)` becomes `f(x, s) → {value, s'}`.

That is all "the state monad" means, stripped of ceremony, and persistence
makes it cheap: `s'` is not a copy of `s`, it is `s` plus O(log n) nodes. Trees
need no threading at all (subtrees are independent), so start there.

## Trees

### Definition

A tree is `nil | {:node, term(), tree(), tree()}` — inductive, one base case
and one step case: lesson 4's list with two recursive positions. A struct
(`defstruct [:val, :left, :right]`) works equally well; a tagged tuple matches
more tersely. The exercise file gives you `Tree.leaf/1`, `Tree.node/3`, and
`Tree.from_list/1` (leetcode's level-order layout — children of i at 2i+1 and
2i+2, `nil` = absent — read via a tuple, since that layout needs O(1)
indexing):

```elixir
iex> Tree.from_list([3, 9, 20, nil, nil, 15, 7])
{:node, 3, {:node, 9, nil, nil}, {:node, 20, {:node, 15, nil, nil}, {:node, 7, nil, nil}}}
```

### DFS: three orders, one shape

```elixir
def preorder(nil, acc),  do: acc
def preorder({:node, v, l, r}, acc), do: [v | preorder(l, preorder(r, acc))]
def inorder(nil, acc),   do: acc
def inorder({:node, v, l, r}, acc),  do: inorder(l, [v | inorder(r, acc)])
def postorder(nil, acc), do: acc
def postorder({:node, v, l, r}, acc), do: postorder(l, postorder(r, [v | acc]))
```

The three differ only in *where the node's value is consed*. The obvious
`inorder(l) ++ [v] ++ inorder(r)` is O(n²) on a left spine — `++` costs
O(length of its left argument), re-run at every level. The accumulator makes
each value cost one cons ⇒ Θ(n).

### Grounding: structural induction on trees

The induction principle is read straight off the type. To prove `P(t)` ∀ t:

```
P(nil)                                                    (base)
∀ v l r.  P(l) ∧ P(r)  ⇒  P({:node, v, l, r})             (step)
──────────────────────────────────────────────────────────────
∀ t. P(t)
```

**Theorem.** `length(inorder(t, acc)) ≡ size(t) + length(acc)`, with
`size(nil) = 0`, `size({:node,_,l,r}) = 1 + size(l) + size(r)`.

*Proof.* Induction on `t`. Base: `inorder(nil, acc) ≡ acc` ✓. Step: assume
it for `l` and `r` and for *every* accumulator (generalising over `acc` is what
makes the induction go through).

```
length(inorder({:node,v,l,r}, acc))
  ≡ length(inorder(l, [v | inorder(r, acc)]))            (unfold)
  ≡ size(l) + length([v | inorder(r, acc)])              (IH on l)
  ≡ size(l) + 1 + length(inorder(r, acc))                (length of cons)
  ≡ size(l) + 1 + size(r) + length(acc)                  (IH on r)
  ≡ size({:node,v,l,r}) + length(acc)                    (def of size) ∎
```

Every value appears exactly once, so `inorder/1` permutes the tree's values;
the same induction tracking *positions* instead of lengths proves that for a
BST it is sorted. **Cost.** Θ(n) time, Θ(h) stack (h = n degenerate, ⌊log₂ n⌋
balanced).

### BFS: level by level

DFS follows the recursion of the type; BFS crosses the structure sideways, so
the frontier must be carried explicitly:

```elixir
defp levels([], acc), do: Enum.reverse(acc)
defp levels(frontier, acc) do
  values = Enum.map(frontier, fn {:node, v, _l, _r} -> v end)
  next = Enum.flat_map(frontier, fn {:node, _v, l, r} -> Enum.reject([l, r], &is_nil/1) end)
  levels(next, [values | acc])
end
```

**Invariant.** On entry `frontier` is exactly the depth-d nodes, left to
right, `acc` levels 0…d-1 reversed. **Variant.** Nodes at depth ≥ d strictly
decreases; the tree is finite ⇒ termination. **Cost.** Θ(n), Θ(w) space (w =
widest level).

Working level-at-a-time avoids a queue entirely. For a *true* FIFO use
`:queue`, a banker's queue of two lists (`:queue.in/2`, `:queue.out/1` →
`{{:value, x}, q}`), amortised O(1): `out` on an empty front reverses the back
in Θ(k), but each element is reversed at most once. Never fake a queue with
`list ++ [x]` — Θ(n) per push.

## Graphs

### Representation

`%{node => [neighbour]}` — O(log n) lookup, O(1) neighbour list. Reading with
`Map.get(g, v, [])` makes the neighbour function *total*, sparing a case
analysis on "unknown vertex" at every call site.

```elixir
def from_edges(edges) do
  Enum.reduce(edges, %{}, fn {u, v}, g ->
    g |> Map.put_new(v, []) |> Map.update(u, [v], &[v | &1])
  end)
end

def neighbours(g, v), do: Map.get(g, v, [])   # total: unknown vertex ⇒ []
```

### DFS with a threaded visited set

State threading in its purest form: imperative DFS mutates a global `visited`;
here `seen` goes in and comes back out, `Enum.reduce` chaining it across the
children.

```elixir
def visit(g, v, seen) do   # call as visit(g, start, MapSet.new()) -> seen
  if MapSet.member?(seen, v) do
    seen                                    # already done — return unchanged
  else
    seen = MapSet.put(seen, v)
    Enum.reduce(Graph.neighbours(g, v), seen, &visit(g, &1, &2))
  end
end
```

Read the `reduce` carefully: the accumulator *is* the mutable variable and the
closure the loop body — every imperative "for each neighbour: recurse, updating
visited" is exactly this. **Termination.** Variant `|V| - |seen|` ∈ ℕ
strictly decreases on every call that does not return immediately. **Cost.**
each vertex expanded once, each edge examined once ⇒ O((V + E) log V).

Flood fill (Number of Islands) is this exact function over an *implicit* graph:
vertices are a MapSet of land cells, `neighbours({r,c})` is computed as
`[{r-1,c}, {r+1,c}, {r,c-1}, {r,c+1}]` rather than stored. Backtracking is free
too — the "undo" an imperative backtracker needs is just *not using* the
returned state; the old value is still bound.

### BFS shortest path, and why it is optimal

The same `levels/2` loop plus a `seen` set — graphs have cycles:

```elixir
def path_len(g, from, to), do: bfs(g, [from], MapSet.new([from]), 0, to)

defp bfs(_g, [], _seen, _d, _to), do: :infinity
defp bfs(g, frontier, seen, d, to) do
  if to in frontier do
    d
  else
    {next, seen} =
      for v <- frontier, w <- Graph.neighbours(g, v), reduce: {[], seen} do
        {next, seen} ->
          if w in seen, do: {next, seen}, else: {[w | next], MapSet.put(seen, w)}
      end
    bfs(g, next, seen, d + 1, to)
  end
end
```

**Theorem (optimality on unweighted graphs).** When BFS first places `w` in
a frontier, `d ≡ dist(from, w)`: the least number of edges on any path.

*Proof.* Induction on d, invariant: *the frontier at step d is exactly
`{w : dist(from, w) = d}` and `seen` is exactly `{w : dist(from, w) ≤ d}`.*
Base d = 0: frontier `[from]`, `dist(from, from) = 0`, seen `{from}` ✓. Step:
if `dist(from, w) = d + 1`, some shortest path to `w` ends `u → w` with
`dist(from, u) = d` (a prefix of a shortest path is shortest), so `u` is in the
frontier by the IH and `w` gets examined; and `w ∉ seen`, since `seen` holds
only distance ≤ d. So `w` enters the next frontier. Conversely anything
entering it has a neighbour at distance d (⇒ ≤ d+1) and was not in `seen` (⇒ >
d). Exactly the distance-(d+1) set. ∎

Marking `w` seen *on enqueue*, not on pop, is what makes "exactly" hold — mark
on pop and a vertex can enter two frontiers. **Cost.** O((V + E) log V) time,
O(V) space. The proof breaks once edges carry weights: the frontier stops being
a distance level set and you need Dijkstra — this loop with a priority queue
(below).

### Topological sort (Kahn)

```elixir
def can_finish(n, prereqs) do
  adj = Enum.reduce(prereqs, %{}, fn [a, b], m -> Map.update(m, b, [a], &[a | &1]) end)
  zero = Map.new(0..(n - 1)//1, &{&1, 0})
  indeg = Enum.reduce(prereqs, zero, fn [a, _b], m -> Map.update!(m, a, &(&1 + 1)) end)
  ready = for {v, 0} <- indeg, do: v
  kahn(ready, adj, indeg, 0) == n
end

defp kahn([], _adj, _indeg, done), do: done
defp kahn([v | rest], adj, indeg, done) do
  {ready, indeg} =
    Enum.reduce(Map.get(adj, v, []), {rest, indeg}, fn w, {q, d} ->
      d = Map.update!(d, w, &(&1 - 1))
      if d[w] == 0, do: {[w | q], d}, else: {q, d}
    end)
  kahn(ready, adj, indeg, done + 1)
end
```

`for {v, 0} <- indeg` is a comprehension whose *pattern* filters — pairs that
fail to match are skipped: matching as a filter, no predicate.

**Invariant.** `indeg[w]` counts w's not-yet-emitted predecessors; `ready`
holds every unemitted vertex with none left. **Correctness.** Emitting `v` only
at `indeg[v] = 0` means all its predecessors came earlier ⇒ the output is a
topological order. Completeness: unemitted vertices of an acyclic graph form a
non-empty finite DAG while any remain, and every finite DAG has a source
(walking predecessors forever would force a cycle), so `ready` stays non-empty
⇒ all n are emitted; and `done < n` ⇔ a cycle. ∎ **Cost.** O(V + E) up to logs.

## Dynamic programming = memoised recursion

DP is a recurrence plus a table: write the recurrence honestly, then thread the
table. Table = map; return shape = `{value, memo}`.

```elixir
def coin_change(coins, amount) do                # -1 for "impossible"
  {best, _memo} = cc(amount, coins, %{})
  if best == :inf, do: -1, else: best
end

defp cc(0, _coins, memo), do: {0, memo}
defp cc(a, _c, memo) when a < 0, do: {:inf, memo}
defp cc(a, coins, memo) do
  case Map.fetch(memo, a) do
    {:ok, v} -> {v, memo}
    :error ->
      {best, memo} = Enum.reduce(coins, {:inf, memo}, fn c, {best, memo} ->
        {sub, memo} = cc(a - c, coins, memo)            # thread the memo
        {min_inf(best, succ(sub)), memo}
      end)
      {best, Map.put(memo, a, best)}
  end
end
```

**Recurrence**, `f(a)` = fewest coins summing to exactly `a`:
`f(0) = 0`; `f(a) = ∞` for `a < 0`; `f(a) = 1 + min{f(a-c) : c ∈ coins}`.

*Justification (optimal substructure — every DP proof has this shape).* An
optimal solution for `a > 0` uses some coin `c`; removing it solves `a - c`
in `f(a) - 1` coins ⇒ `f(a) ≥ 1 + min_c f(a - c)`. Conversely any solution
for `a - c` extends by `c` ⇒ `f(a) ≤ 1 + f(a - c)` ∀ c. ∎

**Memo invariant.** `memo[a] ≡ f(a)` for every key present — we write only
after the full minimum is computed, and `f` is pure in `a`. **Termination.**
Each call strictly decreases `a`, bounded by the `a < 0` clause. **Cost.** Each
`a ∈ [0, amount]` is expanded at most once (later hits go through `Map.fetch`),
doing |coins| work ⇒ O(amount · |coins|) time, O(amount) space. Unmemoised, the
same recursion is exponential.

### The bottom-up alternative

If the subproblem order is obvious, iterate it and drop the threading — one
`Enum.reduce` whose accumulator is the whole table:

```elixir
def coin_change_bu(coins, amount) do
  t = Enum.reduce(1..amount//1, %{0 => 0}, fn a, t ->
    Map.put(t, a, Enum.reduce(coins, :inf, fn c, best ->
      if a - c >= 0, do: min_inf(best, succ(t[a - c])), else: best
    end))
  end)

  if t[amount] == :inf, do: -1, else: t[amount]
end
```

**Why it is correct.** `a` is visited in increasing order and `f(a)` depends
only on `f(a - c)`, `c > 0` — strictly smaller, already in `t`. Formally:
strong induction on `a`, invariant "after iteration a, `t[k] ≡ f(k)` ∀ k ≤ a".
Same complexity, no stack — but it computes *every* subproblem, where
memoisation computes only reachable ones: top-down when that set is sparse,
bottom-up when dense.

When the state is a fixed-width window the table collapses to a tuple —
Climbing Stairs (`f(0) = f(1) = 1`, `f(n) = f(n-1) + f(n-2)`) is
`Enum.reduce(1..n//1, {1, 1}, fn _k, {a, b} -> {b, a + b} end)`, taking the
first component. **Invariant.** After k iterations the accumulator is `{f(k),
f(k+1)}`: base `{1, 1}`, step `{a,b} → {b, a+b} ≡ {f(k+1), f(k+2)}` by the
recurrence. After n iterations component 0 is `f(n)`. ∎ **Cost.** Θ(n), O(1).

## Heaps

Elixir has no built-in priority queue. Three options:

1. **`:gb_sets`** — a balanced *set* in Erlang term order: `add/2`,
   `take_smallest/1`, `take_largest/1`, all O(log n). Being a set, store
   `{priority, unique_tag}` so equal priorities do not collide.
2. **Sorting** — if you pop everything anyway `Enum.sort_by` is Θ(n log n)
   and simpler; use a heap only to pop *k* of n, or when priorities change
   as you go (Dijkstra).
3. **A pairing heap** — ~15 lines, genuinely O(1) insert:

```elixir
defmodule Heap do                          # empty heap is the atom :empty
  def insert(h, x), do: merge({x, []}, h)               # O(1)
  def merge(:empty, h), do: h
  def merge(h, :empty), do: h
  def merge({x, hx} = a, {y, hy} = b),                  # O(1)
    do: if(x <= y, do: {x, [b | hx]}, else: {y, [a | hy]})
  def pop(:empty), do: :error                           # O(log n) amortised
  def pop({x, hs}), do: {:ok, x, pair(hs)}
  defp pair([]), do: :empty
  defp pair([h]), do: h
  defp pair([a, b | rest]), do: merge(merge(a, b), pair(rest))
end
```

**Invariant** (maintained by `merge`): the root is the minimum — the larger
root becomes a child of the smaller. `pop` drops the root and merges the
orphans *in pairs first*, then right to left; that two-pass rule buys O(log n)
amortised `pop`, and a naive left fold degrades to O(n).

Bounded top-k: fold `Enum.frequencies(nums)` into a `:gb_sets` min-heap of
`{count, value}`, dropping the minimum with `:gb_sets.take_smallest/1` whenever
the size exceeds k. What survives is the k largest, and `:gb_sets.to_list/1` is
ascending, so reverse it.

**Invariant.** After any prefix of the distinct values the heap holds the k
largest `{count, value}` pairs so far (all of them if fewer than k). Evicting
the minimum never discards a true top-k member: whatever goes sits below k
elements already held. **Cost.** Θ(n) to count, Θ(m log k) for m distinct
values ⇒ O(n log k), O(n) space; sorting is O(m log m) — worse when k ≪ m.

## Exercises

`exercises/12_patterns_ii.exs` — `Tree` and `Graph` are given; only
`PatternsII` is yours. Hints:

- `max_depth/1` — two clauses; the second is `1 + max(...)`.
- `inorder/1` — delegate to a private `inorder/2` with an accumulator, no
  `++`; `level_order/1` — the `levels/2` frontier recursion above.
- `num_islands/1` — a comprehension with `into: MapSet.new()` turns rows
  into land coordinates; then reduce over the land, flood-filling each
  unvisited cell and threading `seen`.
- `can_finish/2` — Kahn; `Map.new(0..(n-1)//1, &{&1, 0})` seeds in-degrees
  so isolated courses are counted.
- `coin_change/2` — memoised recursion returning `{value, memo}`, `:inf` as
  the impossible element (`succ/1`, `min_inf/2`).
- `climb_stairs/1` — one `Enum.reduce` over `1..n//1` carrying a pair; the
  `//1` matters, `1..0` counts *down* without it.
- `top_k_frequent/2` — `Enum.frequencies/1`, bounded `:gb_sets` min-heap,
  reversed at the end.

## Leetcode at this stage

- Trees: 104 Maximum Depth, 94 Inorder Traversal, 102 Level Order, 226
  Invert Binary Tree, 98 Validate BST, 236 Lowest Common Ancestor.
- Graphs: 200 Number of Islands, 133 Clone Graph, 207 / 210 Course Schedule
  I & II, 417 Pacific Atlantic, 127 Word Ladder, 743 Network Delay Time
  (Dijkstra — heap required).
- DP: 70 Climbing Stairs, 322 Coin Change, 198 House Robber, 139 Word Break,
  300 Longest Increasing Subsequence, 416 Partition Equal Subset Sum.
- Heaps: 347 Top K Frequent, 215 Kth Largest, 23 Merge k Sorted Lists, 295
  Find Median from Data Stream (two heaps).

That closes the course. The through-line: `=` is unification, functions are
case analysis, immutability buys equational reasoning, inductive types come
with induction principles, folds are universal, persistence makes threaded
state cheap. Every pattern here is one of those six wearing an algorithm's
name.
