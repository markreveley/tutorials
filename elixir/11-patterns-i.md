# 11 — Two pointers, sliding window, prefix sums, hashing, binary search

## Concept

The leetcode pattern catalogue was written for arrays: O(1) random access
plus in-place mutation. Elixir has neither. Ported naively, every pattern
turns quadratic; ported properly, most get shorter, and the ones that do not
tell you something true about the structure you chose. One fact drives the
whole lesson:

```
list        [h | t]      head O(1), tail O(1), Enum.at(xs, i)  O(i)
tuple       {a, b, c}    elem(t, i) O(1), put_elem O(n) (copies)
map         %{k => v}    fetch/put O(log n) (effectively O(1) for small n)
```

A list is a **one-way cursor**. There is no "index i" to hold; the thing you
hold is the suffix of the list starting at i. Once you accept that, "two
pointers" stops meaning "two integers" and starts meaning "two suffixes",
and the translation becomes mechanical.

### The `Enum.at/2` trap

Here is the naive port of the classic two-pointer palindrome check:

```elixir
# WRONG — this is O(n²)
def pal?(xs) do
  n = length(xs)
  Enum.all?(0..div(n, 2), fn i -> Enum.at(xs, i) == Enum.at(xs, n - 1 - i) end)
end
```

`Enum.at(xs, i)` walks `i` cons cells, so the loop costs
`Σ(i = 0 .. n/2) [ i + (n-1-i) ] = (n/2)(n-1) ∈ Θ(n²)`. The code *looks*
like the array version and is asymptotically worse. Two honest fixes exist:
walk the structure instead of indexing it, or change to a structure where
indexing is O(1) (tuple, or `:array`). The rest of the lesson is those two
fixes, applied five times.

## Pattern 1 — Two pointers

### Form A: two cursors moving the same way

Both pointers only move forward, and they never cross back. Represent each
as a list suffix; recur on both at once.

```elixir
def merge([], ys), do: ys                                     # the archetype
def merge(xs, []), do: xs
def merge([x | xs], [y | ys]) when x <= y, do: [x | merge(xs, [y | ys])]
def merge(xs, [y | ys]), do: [y | merge(xs, ys)]
```

**Invariant.** Each call receives the untouched tails of both inputs, and
everything already emitted is ≤ every element of `xs ++ ys`.
**Variant.** `length(xs) + length(ys)` strictly decreases, bounded below by
0 ⇒ termination. **Cost.** O(n + m), one cons per output element.

### Form B: converging pointers, from both ends

Now one pointer moves forward and one backward. A list gives you no
backward step, so either reverse it once (Θ(n), then you have two forward
cursors) or convert to a tuple and hold two integers.

Palindrome, the reverse trick — `fwd` and `bwd` *are* the two pointers, and
we stop after ⌊n/2⌋ steps because past that the halves swap roles:

```elixir
def palindrome?(cs), do: walk(cs, Enum.reverse(cs), div(length(cs), 2))

defp walk(_fwd, _bwd, 0), do: true
defp walk([a | fwd], [b | bwd], k) when a == b, do: walk(fwd, bwd, k - 1)
defp walk(_fwd, _bwd, _k), do: false
```

**Correctness.** Write `xs!i` for the i-th element; `Enum.reverse(xs)!i ≡
xs!(n-1-i)`. After k steps the guard `a == b` is exactly `xs!k ≡ xs!(n-1-k)`,
and `xs` is a palindrome iff that holds ∀ k < n/2. ∎
**Cost.** Θ(n) time, Θ(n) extra space for the reversal.

Container With Most Water needs the *distance* `hi - lo`, so integers it is,
which forces a tuple:

```elixir
def max_area(hs) do
  t = List.to_tuple(hs)
  area(t, 0, tuple_size(t) - 1, 0)
end

defp area(_t, lo, hi, best) when lo >= hi, do: best
defp area(t, lo, hi, best) do
  a = elem(t, lo); b = elem(t, hi)
  best = max(best, min(a, b) * (hi - lo))
  if a < b, do: area(t, lo + 1, hi, best), else: area(t, lo, hi - 1, best)
end
```

**Invariant.** Some optimal pair `(i, j)` satisfies `lo ≤ i < j ≤ hi`.
**Why discarding is safe.** Suppose `h[lo] < h[hi]`. Any pair `(lo, j)` with
`j < hi` has area `min(h[lo], h[j]) · (j - lo) ≤ h[lo] · (j - lo) <
h[lo] · (hi - lo)`, which we have already recorded. So no pair using `lo`
other than `(lo, hi)` can beat the current best ⇒ dropping `lo` preserves
the invariant. Symmetrically for the other branch. ∎
**Variant.** `hi - lo` strictly decreases ⇒ at most n steps. **Cost.** Θ(n)
time after a Θ(n) conversion, Θ(n) space for the tuple.

## Pattern 2 — Sliding window

Imperatively you keep `lo`, `hi`, and an aggregate. Functionally you keep
the same three things as *arguments to a recursion* — the window state is
the accumulator. What makes it O(1) per step on lists: the left end is a
suffix `lo`, the right end a further suffix `hi`, and the window is the gap
between them. Grow right = take the head of `hi`; shrink left = take the
head of `lo`.

```elixir
def min_subarray_len(target, nums), do: window(nums, nums, 0, 0, nil, target) || 0

defp window(lo, hi, sum, len, best, target) when sum >= target do
  [x | lo] = lo                                   # shrink from the left
  best = if best == nil, do: len, else: min(best, len)
  window(lo, hi, sum - x, len - 1, best, target)
end
defp window(_lo, [], _sum, _len, best, _target), do: best
defp window(lo, [y | hi], sum, len, best, target),  # grow on the right
  do: window(lo, hi, sum + y, len + 1, best, target)
```

**Invariant.** `sum ≡ Σ` of the `len` elements between cursor `lo` and
cursor `hi`; `best` is the length of the shortest qualifying window whose
right end has already been consumed.
**Variant.** `(elements left in hi) + (elements left in lo)` strictly
decreases at every step: growth consumes one from `hi`, shrinking consumes
one from `lo`.
**Cost.** Each cursor advances at most n times ⇒ Θ(n) total, O(1) extra
space — the imperative amortised argument, restated as a decreasing variant.

When the state is a *map* rather than a running total, a fold is cleaner:
you never shrink one step at a time, you jump the left edge.

```elixir
def longest_unique_substring(s) do
  s
  |> String.to_charlist()
  |> Enum.with_index()
  |> Enum.reduce({%{}, 0, 0}, fn {c, i}, {last, start, best} ->
    start = case Map.fetch(last, c) do
      {:ok, j} when j >= start -> j + 1     # c repeats inside the window
      _ -> start
    end
    {Map.put(last, c, i), start, max(best, i - start + 1)}
  end)
  |> elem(2)
end
```

**Invariant.** After index i, `s[start..i]` has no repeats and `start` is
minimal with that property; `last` maps each seen character to its latest
index. **Cost.** Θ(n) map operations, O(k) space for alphabet size k.

## Pattern 3 — Prefix sums

Define `p[i] = xs[0] + … + xs[i]`. Then any range sum is a difference:

```
sum(xs[i..j]) ≡ p[j] - p[i-1]        (p[-1] = 0)
```

That telescoping identity is why prefix sums turn range queries from O(n)
into O(1). In Elixir the pattern is one function: `Enum.scan/2` is a fold
that keeps every intermediate accumulator.

```elixir
iex> Enum.scan([1, 2, 3, 4], &+/2)
[1, 3, 6, 10]
```

**Law.** `Enum.scan(xs, f) |> List.last() ≡ Enum.reduce(tl(xs), hd(xs), f)`
for non-empty `xs` — both sides are the same left fold, one discarding its
intermediates (induction on `xs`).
**Cost.** Θ(n) time and Θ(n) space, one pass.

Because the prefix list is a list, *querying* it by index is O(i). If you
need many range queries, `List.to_tuple` the prefix list once (Θ(n)) and
query with `elem/2` at O(1).

## Pattern 4 — Hashing and frequency counting

Maps replace "array indexed by value" and "set of things seen". Persistent
maps are O(log₃₂ n) — a HAMT of branching factor 32, so below ~10⁹ keys the
depth is ≤ 6: O(1) for every practical purpose.

```elixir
iex> Enum.frequencies(~c"mississippi")
%{105 => 4, 109 => 1, 112 => 2, 115 => 4}
iex> Enum.group_by(["ate", "eat", "tan"], &Enum.sort(String.to_charlist(&1)))
%{~c"aet" => ["ate", "eat"], ~c"ant" => ["tan"]}   # anagram grouping, free
```

Two Sum is the canonical "one pass plus a map": for each `x` at index `j`,
ask whether `target - x` was already seen.

```elixir
def two_sum(nums, target) do
  nums
  |> Enum.with_index()
  |> Enum.reduce_while(%{}, fn {x, j}, seen ->
    case Map.fetch(seen, target - x) do
      {:ok, i} -> {:halt, {i, j}}
      :error   -> {:cont, Map.put_new(seen, x, j)}
    end
  end)
  |> case do
    {i, j} -> {i, j}
    _map   -> nil
  end
end
```

**Invariant.** Before step j, `seen` maps every value in `nums[0..j-1]` to
its *earliest* index (hence `put_new`, not `put`), and no pair inside
`nums[0..j-1]` sums to target.
**Correctness.** If a solution `(i, j)` with i < j exists, take the one with
smallest j. At step j, `nums[i]` is in `seen`, so the fetch succeeds and we
halt with a valid pair. ∎
**Cost.** Θ(n) map operations, Θ(n) space.

`reduce_while` is the functional `break`: the accumulator carries `{:cont,
acc}` or `{:halt, result}`, so early exit is a value, not a jump.

## Pattern 5 — Binary search, with the invariant spelled out

Binary search needs O(1) indexing, so on lists it is *impossible* — halving
buys you nothing when reaching the midpoint already costs n/2 steps. Convert
to a tuple (`List.to_tuple/1`, Θ(n)) or use Erlang's `:array` module for
large sparse cases. Then:

```elixir
def binary_search(t, target) when is_tuple(t), do: bsearch(t, target, 0, tuple_size(t))

defp bsearch(_t, _target, lo, hi) when lo >= hi, do: :error
defp bsearch(t, target, lo, hi) do
  mid = lo + div(hi - lo, 2)
  case elem(t, mid) do
    ^target          -> {:ok, mid}
    v when v < target -> bsearch(t, target, mid + 1, hi)
    _                -> bsearch(t, target, lo, mid)
  end
end
```

Note `^target` — a pin inside a `case` pattern, comparing against the
existing binding rather than rebinding (lesson 1).

### The half-open formulation

The range is `[lo, hi)`: `lo` included, `hi` excluded. This is not
cosmetic; it is what makes the proof short.

- The size of the range is exactly `hi - lo` (no ±1 fudge).
- Empty is exactly `lo ≥ hi`.
- The initial call is `(0, n)` with no `n - 1`.
- Both recursive calls shrink the range without ever re-testing `mid`.

**Precondition.** `t` is sorted ascending: ∀ i < j < n, `elem(t,i) ≤
elem(t,j)`.

**Invariant I(lo, hi).**
```
0 ≤ lo ≤ hi ≤ n   ∧   (∃ i. elem(t,i) ≡ target)  ⇒  (∃ i ∈ [lo, hi). elem(t,i) ≡ target)
```
"If the target is anywhere, it is in the window."

**Establishment.** The first call has `lo = 0, hi = n`, so `[lo, hi)` is the
whole tuple and I holds trivially.

**Preservation.** Assume I(lo, hi) and `lo < hi`. Then `lo ≤ mid < hi`,
because `0 ≤ div(hi - lo, 2) < hi - lo` whenever `hi - lo ≥ 1`.
- If `elem(t, mid) < target`: by sortedness ∀ i ≤ mid, `elem(t,i) ≤
  elem(t,mid) < target`, so no index in `[lo, mid]` holds the target.
  Combined with I(lo, hi), any occurrence lies in `[mid+1, hi)` ⇒
  I(mid+1, hi).
- If `elem(t, mid) > target`: symmetrically no index in `[mid, hi)` holds it
  ⇒ I(lo, mid).
- If equal, we return `{:ok, mid}` and `elem(t, mid) ≡ target` by the match.

**Termination (variant).** Let V = `hi - lo` ∈ ℕ.
- Right branch: V' = `hi - (mid+1) = hi - lo - div(hi-lo,2) - 1 < V`.
- Left branch: V' = `mid - lo = div(hi - lo, 2) < V` for V ≥ 1.

V strictly decreases and is bounded below by 0, so the recursion reaches
`lo ≥ hi` after finitely many steps. In fact V halves (up to a floor) each
step, so the number of steps is ≤ ⌈log₂(n+1)⌉.

**Partial correctness on failure.** On exit `lo ≥ hi`, so `[lo, hi)` is
empty. By I, if the target existed anywhere it would be in an empty range —
contradiction. Hence `:error` is correct. ∎

**Cost.** Θ(log n) `elem/2` calls, each O(1); O(1) space (the recursion is a
tail call, so BEAM reuses the frame). The Θ(n) conversion from list to tuple
dominates a single search — binary search pays off only when you search the
same converted structure many times, or when the tuple was your
representation to begin with.

### The generalisation worth memorising

Most binary-search leetcode problems are not "find x" but "find the first
index where a monotone predicate flips". Same invariant, one comparison:

```elixir
# smallest i in [lo, hi) with pred.(i) true; hi if none. Requires:
# pred monotone — false…false,true…true
def lower_bound(lo, hi, _pred) when lo >= hi, do: hi
def lower_bound(lo, hi, pred) do
  mid = lo + div(hi - lo, 2)
  if pred.(mid), do: lower_bound(lo, mid, pred), else: lower_bound(mid + 1, hi, pred)
end
```

Invariant: everything below `lo` fails `pred`, everything at or above `hi`
satisfies it. This is the whole "binary search on the answer" family (875,
1011) — the search space is a range of candidate answers, not an existing
structure, so there is nothing to convert and no Θ(n) penalty.

## Honest accounting: what ports, what does not

| Pattern | Elixir status |
|---|---|
| Two pointers, same direction | **Clean.** Multi-clause recursion on two lists. Often *shorter*. |
| Two pointers, converging | **Needs help.** Reverse once (Θ(n) space) or use a tuple. |
| Sliding window, running aggregate | **Clean.** Window = gap between two list cursors; state = arguments. |
| Sliding window, map state | **Clean.** A fold with a map in the accumulator. |
| Prefix sums | **Better.** `Enum.scan/2`, one line. Tuple-ify for O(1) queries. |
| Hashing / frequency | **Better.** `Enum.frequencies`, `group_by`, `reduce_while`. |
| Binary search | **Different structure required.** Tuple or `:array`, never a list. |
| In-place array mutation (sort in place, Dutch flag, cyclic sort) | **Does not port.** Rebuild instead, or drop to `:array`/`:atomics`. |
| Backtracking with an undo step | **Better.** The old state *is* the undo; nothing to restore (lesson 12). |

Rule of thumb: forward-only pointers translate directly; arbitrary indexing
or writing into the input forces a representation change. Paying a stated
Θ(n) conversion for it is engineering. Paying it accidentally, one
`Enum.at/2` at a time, is a bug no test suite catches — only the complexity
claim does.

## Exercises

`exercises/11_patterns_i.exs`. Hints:

- `two_sum/2` — `Enum.with_index/1`, then `Enum.reduce_while/3` with a map
  accumulator. `Map.put_new/3` keeps the earliest index.
- `is_palindrome/1` — downcase, `String.to_charlist/1`, filter to
  alphanumerics, then the `walk/3` two-cursor recursion above.
- `max_area/1` — `List.to_tuple/1` first; converging indices; base case
  `lo >= hi`.
- `longest_unique_substring/1` — fold `Enum.with_index/1` carrying
  `{last_seen_map, window_start, best}`.
- `min_subarray_len/2` — the two-suffix window; bind both `lo` and `hi` to
  the whole list with `sum = 0`.
- `binary_search/2` — half-open `[lo, tuple_size(t))`; return `{:ok, i}` or
  `:error`; pin the target with `^target`.
- `prefix_sums/1` — `Enum.scan/2` with `&+/2`.

## Leetcode at this stage

- Two pointers: 1 Two Sum, 167 Two Sum II, 15 3Sum, 125 Valid Palindrome,
  344 Reverse String, 26 Remove Duplicates from Sorted Array,
  11 Container With Most Water, 42 Trapping Rain Water.
- Sliding window: 3 Longest Substring Without Repeating Characters,
  209 Minimum Size Subarray Sum, 424 Longest Repeating Character
  Replacement, 567 Permutation in String.
- Prefix sums / hashing: 1480 Running Sum of 1d Array, 560 Subarray Sum
  Equals K, 242 Valid Anagram, 49 Group Anagrams, 217 Contains Duplicate.
- Binary search: 704 Binary Search, 35 Search Insert Position,
  33 Search in Rotated Sorted Array, 875 Koko Eating Bananas,
  1011 Capacity To Ship Packages Within D Days.

For each: state the invariant and the variant before writing code. No
variant ⇒ no termination proof — and on a list, probably no proof of the
complexity you think you have either.
