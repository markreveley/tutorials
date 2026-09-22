# 12. Dynamic Programming, Heaps, Graphs

## Concept

Backtracking (lesson 11) explores a decision tree. When two branches reach
the *same remaining problem*, the tree repeats work — usually an
exponential amount. Dynamic programming is the observation that such a tree
is really a **DAG of states**, and a DAG is solved by evaluating each node
once.

Two conditions license the move.

**Optimal substructure.** The value of an optimal solution is expressible
from the values of optimal solutions to strictly smaller subproblems:
there is a finite set of first choices c such that

    best(s) = combine over c of  g(c, best(next(s, c)))

with `g` monotone in its second argument and `next(s, c)` strictly smaller
under a well-founded order. Monotonicity is the part people skip: it is
what lets you store a subproblem's *value* instead of all its solutions.

**Overlapping subproblems.** The set of reachable states is small —
polynomial — even though the number of root-to-leaf paths is not. Given
both, you get two implementations of the same recurrence.

```python
from functools import lru_cache

@lru_cache(maxsize=None)              # memoisation: top-down
def f(state):
    if base(state): return base_value(state)
    return combine(g(c, f(next(state, c))) for c in choices(state))

dp = [None] * (n + 1)                 # tabulation: bottom-up
for s in topological_order_of_states:
    dp[s] = base_value(s) if base(s) else combine(...)
```

Memoisation visits only reachable states and needs no ordering; tabulation
needs an order in which dependencies come first, but has no recursion-depth
limit and no per-call overhead. The cost is the same either way:

    time  = (distinct states) × (work per state, transitions included)
    space = (number of states), often reducible — see below

### Heaps

`heapq` maintains a **min-heap** inside an ordinary list — no wrapper
class, the functions operate on your list directly.

```python
import heapq
h = [5, 1, 3]
heapq.heapify(h)            # O(n)
heapq.heappush(h, 2)        # O(log n)
heapq.heappop(h)            # O(log n) -> 1, the minimum
h[0]                        # O(1) peek
heapq.heapreplace(h, 9)     # pop-then-push, one sift
heapq.nlargest(3, xs, key=...)
```

For a max-heap, push `-x`, or push tuples `(-priority, tiebreak, item)`.

### Graphs

The default representation is an adjacency list — a dict or list of lists.

```python
from collections import deque

adj = {0: [1, 2], 1: [2], 2: []}     # directed
adj = [[] for _ in range(n)]         # when labels are 0..n-1

def bfs(adj, src):                   # unweighted shortest paths
    dist = {src: 0}
    q = deque([src])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                q.append(w)
    return dist
```

DFS is the same with a stack and no distance guarantee. A grid is a graph
you never build: vertices are cells, edges are the four orthogonal steps.

## Why

### How to prove a recurrence

Every DP recurrence is proved as two inequalities.

**(≤) Achievability.** Each right-hand-side candidate corresponds to a real
feasible solution, so the optimum is at least as good.

**(≥) Exchange / cut-and-paste.** Take an optimal solution, identify its
first (or last) choice c, and delete that choice. What remains is feasible
for the subproblem `next(s, c)`, so its value is ≥ (for a max problem, ≤)
`best(next(s, c))` — otherwise you could paste in the better subsolution
and beat the optimum, a contradiction.

Then induct on the well-founded order. Below, every case is one paragraph
of exactly this.

**Climbing stairs.** f(n) = number of ways to reach step n by 1- and
2-steps. The first move is 1 or 2; the two cases are disjoint (different
first move) and exhaustive, and after it the problem is literally the same
with n−1 or n−2 stairs. So f(n) = f(n−1) + f(n−2), f(0) = f(1) = 1. This
is counting, not optimising, so the proof is a bijection rather than an
exchange. Θ(n) time; only the last two values are ever read, so **Θ(1)
space**.

**House robber** (max sum of a subset of a[0..n) with no two adjacent).
Let R(i) be the best over a[0..i]. An optimal selection either omits a[i]
— then it is a legal selection for the prefix ending at i−1, so its value
is ≤ R(i−1) — or includes a[i], which forbids a[i−1], leaving a legal
selection for i−2, so its value is ≤ R(i−2) + a[i]. Both candidates are
achievable, hence R(i) = max(R(i−1), R(i−2) + a[i]). Θ(n) time, Θ(1) space.

**Coin change** (fewest coins summing to `amount`, unlimited supply). Let
b(a) be that minimum, +∞ if impossible. For a > 0 an optimal multiset S is
non-empty; remove any coin c ∈ S. The rest sums to a − c, so
|S| − 1 ≥ b(a − c), giving b(a) ≥ 1 + min over c ≤ a of b(a − c). For (≤),
any coin c ≤ a plus an optimal solution for a − c is feasible. Since every
c ≥ 1, a − c < a, so induction on a is well founded, with b(0) = 0. ∎
Θ(amount · |coins|) time, Θ(amount) space. Note this is **pseudo-
polynomial**: linear in the *value* `amount`, exponential in its digits.

Greedy (take the biggest coin that fits) is wrong in general: with
[1, 3, 4] and amount 6 it gives 4+1+1 = 3, but 3+3 = 2 is optimal. Greedy
needs its own exchange proof, and here there is none.

**Longest increasing subsequence.** Let L(i) be the length of the longest
strictly increasing subsequence *ending exactly at* index i. Deleting the
last element of such a subsequence leaves one ending at some j < i with
a[j] < a[i], so L(i) ≤ 1 + max{L(j)}; extending any such subsequence by
a[i] is feasible, so ≥. The answer is max L(i) (0 for an empty list).
Θ(n²) time, Θ(n) space.

The Θ(n log n) version keeps `tails`, where `tails[j]` is the *smallest*
value that can end an increasing subsequence of length j+1. Invariant:
`tails` is strictly increasing and every entry is achievable. For a new x,
`bisect_left` finds the first entry ≥ x; overwriting it with x keeps that
entry achievable (x extends the length-j subsequence, whose tail is
tails[j−1] < x) and can only lower it, so the invariant survives; if no
entry is ≥ x, x extends the longest run and is appended. `len(tails)` is
the answer, but `tails` itself is **not** an LIS.

**Edit distance.** d(i, j) = fewest insert/delete/replace edits turning
word1[0..i) into word2[0..j). d(i, 0) = i (delete everything),
d(0, j) = j (insert everything). For i, j > 0 look at how the last
characters are aligned in an optimal script: either they are matched — free
if equal, one replace if not, leaving d(i−1, j−1) — or word1[i−1] is
deleted, leaving d(i−1, j), or word2[j−1] is inserted, leaving d(i, j−1).
Those cases are exhaustive, each is achievable, so

    d(i, j) = d(i-1, j-1)                                    if a == b
            = 1 + min(d(i-1, j), d(i, j-1), d(i-1, j-1))     otherwise

Θ(m·n) time. Row i depends only on row i−1, so one rolling row plus one
saved diagonal gives **Θ(min(m, n)) space** — swap the arguments so the row
is the shorter one. Recovering the actual script needs the full table.

**0/1 knapsack.** Items with weights w[i] and values v[i], capacity W, each
item usable at most once. K(i, c) = best value from the first i items with
capacity c. Item i−1 is either left out (K(i−1, c)) or taken, which needs
c ≥ w[i−1] and leaves K(i−1, c − w[i−1]) + v[i−1] — an exchange argument
identical to house robber. Θ(n·W) time, Θ(W) space with a rolling array,
provided you iterate capacity **downward**:

```python
dp = [0] * (W + 1)
for wt, val in items:
    for c in range(W, wt - 1, -1):        # downward: dp[c-wt] is still row i-1
        dp[c] = max(dp[c], dp[c - wt] + val)
```

Ascending order would read a cell already updated in this row, which
re-uses the item — that is exactly the *unbounded* knapsack recurrence, and
also why `coin_change` above (unlimited coins) sweeps upward. The direction
of a loop is a correctness property, not a style choice.

### Why space optimisation is safe

Nothing about the recurrence changes; you are choosing a schedule. If a
state's dependencies all live in the previous layer (row, or the last k
values), earlier layers are unreachable once that layer is done and may be
overwritten. The obligation is to check that no cell you overwrite is still
needed by a later cell *in the same layer* — exactly what the downward
sweep above guarantees.

### Heaps: the invariant and the log

A binary heap is a **complete** binary tree — every level full except
possibly the last, filled left to right — stored in an array with
`children(i) = (2i+1, 2i+2)` and `parent(i) = (i−1)//2`. Completeness is
what makes the array embedding hole-free.

*Heap invariant:* `a[parent(i)] ≤ a[i]` for every i > 0.

By induction, the invariant implies `a[i] ≤ a[j]` for every descendant j
(chain the parent-child inequalities up the path), so `a[0]` is a minimum —
which is all a heap promises. It is *not* sorted.

A complete tree with n nodes has height ⌈log₂(n+1)⌉ (lesson 11, Claim 1,
with the bound tight). `heappush` appends at the end — the only slot that
preserves completeness — and sifts up: each step compares with the parent
and either stops or swaps, moving one level closer to the root, so at most
h = O(log n) steps. `heappop` moves the last element to the root and sifts
down: each step swaps with the smaller child, descending one level, again
O(log n). Both restore the invariant on the single broken path, since only
nodes on that path change. `heapify` is O(n), not O(n log n): sifting down
from the bottom costs Σ over heights h of (n/2^(h+1))·h ≤ n·Σ h/2^(h+1) = n.

**Top-k.** Keeping a min-heap of the k best seen so far: each element does
one O(1) comparison against `h[0]` and at most one O(log k) replace, so
Θ(n log k) time and Θ(k) space — better than sorting's Θ(n log n) when
k ≪ n, and it works on a stream where sorting cannot. Correctness is an
invariant: *after processing a prefix, the heap holds exactly the k largest
elements of that prefix*; an incoming x smaller than the heap minimum
cannot belong to the k largest, and a larger one displaces exactly the
current minimum.

### Why BFS gives shortest paths

Claim: on an unweighted graph, BFS from s sets `dist[v] = δ(v)`, the
minimum number of edges on any s–v path, for every reachable v.

*Lemma (monotone queue).* At all times the queue holds vertices whose
assigned distances are non-decreasing and span at most two consecutive
values d, d+1. Initially it holds only s (value 0). Popping the front
removes a d; pushing appends d+1 values, which is consistent with the
claim. So vertices are dequeued in non-decreasing distance order.

*(≥)* Each assigned `dist[v]` counts the edges on an actual s–v path built
by the algorithm, so δ(v) ≤ dist[v].

*(≤)* Induction on δ(v). δ(s) = 0 = dist[s]. Let δ(v) = d > 0 and take a
shortest path s … u v; then δ(u) = d − 1, so by the IH u is discovered with
dist[u] = d − 1 and enqueued. When u is dequeued, either v is already
discovered — and by the lemma everything discovered by then has dist ≤ d —
or v is discovered now with dist[v] = d. Either way dist[v] ≤ d. ∎

Each vertex is enqueued once (the `if w not in dist` guard) and each edge
scanned once, so Θ(V + E) time, Θ(V) space. The proof breaks the moment
edges have unequal weights — the queue is no longer monotone, and you need
a priority queue instead: that is Dijkstra, BFS with a heap.

### Why Kahn's topological sort is correct

Repeatedly output a vertex whose in-degree among the *remaining* vertices
is 0, and decrement its successors.

*Validity.* v is output only once every predecessor of v has been removed,
i.e. already output. So for every edge u → v, u precedes v in the output —
the definition of a topological order.

*Completeness.* If the graph has a cycle, every vertex on it always has an
un-output predecessor on the cycle, so none is ever output: fewer than V
vertices come out. Conversely, if fewer than V come out, let R be the
non-empty remaining set; every vertex of R has a predecessor in R (else its
in-degree would be 0). Walk backwards from any vertex of R; after |R| steps
some vertex repeats, and the walk between the repeats is a cycle. Hence
**placed == V iff the graph is acyclic**, which is what `can_finish` needs.
Each vertex is enqueued once and each edge decremented once: Θ(V + E). ∎

### Union-find

For "are these two things connected", when edges arrive over time and you
never need the paths themselves.

```python
parent = list(range(n))
size = [1] * n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]    # path halving
        x = parent[x]
    return x

def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False                     # already together
    if size[ra] < size[rb]:
        ra, rb = rb, ra                  # union by size: smaller under larger
    parent[rb] = ra
    size[ra] += size[rb]
    return True
```

*Invariant:* the parent array is a forest, each tree is exactly one
equivalence class, and its root is the representative. `find` returns the
root and `union` links two roots, so the invariant holds and
`find(a) == find(b)` iff a and b are in the same class.

Union by size alone keeps every tree depth ≤ log₂ n — a node's depth grows
only when its tree is merged under one at least as large, doubling its
class size, which can happen at most log₂ n times — so O(log n) per
operation. Adding path compression, Tarjan's bound is **O(m·α(n))**
amortised over m operations, where α is the inverse Ackermann function:
α(n) ≤ 4 for every n below 2^65536. Say "amortised near-constant", not
"O(1)".

## Worked examples

```python
>>> from functools import lru_cache
>>> @lru_cache(maxsize=None)
... def fib(n): return n if n < 2 else fib(n - 1) + fib(n - 2)
>>> fib(200)                       # 2**200 calls without the cache
280571172992510140037611932413038677189525
>>> fib.cache_info().hits          # every state computed once
198
```

Tabulation of the same DAG, plus the two-variable form:

```python
>>> def climb(n):
...     prev, cur = 1, 1
...     for _ in range(n - 1):
...         prev, cur = cur, prev + cur
...     return cur if n >= 1 else 1
>>> [climb(i) for i in range(7)]
[1, 1, 2, 3, 5, 8, 13]
```

The coin table, read as "best[a] = 1 + min over reachable predecessors":

```python
>>> coins, amount = [1, 3, 4], 6
>>> INF = float('inf'); best = [0] + [INF] * amount
>>> for a in range(1, amount + 1):
...     best[a] = min([best[a - c] + 1 for c in coins if c <= a] or [INF])
>>> best
[0, 1, 2, 1, 1, 2, 2]
```

Heaps, as a priority queue and as top-k:

```python
>>> import heapq
>>> h = []
>>> for task in [(3, 'c'), (1, 'a'), (2, 'b')]: heapq.heappush(h, task)
>>> [heapq.heappop(h) for _ in range(3)]      # tuples compare lexicographically
[(1, 'a'), (2, 'b'), (3, 'c')]
```

## Exercises

Open `exercises/12_patterns_dp.py`; run `python3 -m pytest exercises/12_patterns_dp.py`.

- `climb_stairs(n)` — the Fibonacci recurrence in Θ(1) space.
- `coin_change(coins, amount)` — unbounded, sweeping upward; −1 for ∞.
- `length_of_lis(nums)` — Θ(n log n) with the `tails` invariant.
- `edit_distance(word1, word2)` — one rolling row and a saved diagonal.
- `k_largest(nums, k)` — a size-k min-heap, Θ(n log k).
- `top_k_frequent(nums, k)` — counts, then the same heap.
- `num_islands(grid)` — connected components on an implicit grid graph.
- `can_finish(n, prerequisites)` — Kahn; acyclic iff all n vertices come out.

## LeetCode

- 70 Climbing Stairs / 746 Min Cost Climbing Stairs — the two-variable form.
- 198 House Robber / 213 House Robber II — the exchange argument above.
- 322 Coin Change / 518 Coin Change II — min vs count; loop order decides.
- 300 Longest Increasing Subsequence — Θ(n²), then patience.
- 72 Edit Distance / 1143 Longest Common Subsequence — the same table.
- 416 Partition Equal Subset Sum — 0/1 knapsack; sweep capacity downward.
- 215 Kth Largest Element / 703 Kth Largest in a Stream — a size-k heap.
- 347 Top K Frequent Elements / 23 Merge k Sorted Lists — heap of size k.
- 200 Number of Islands / 733 Flood Fill — components; 542 needs multi-source BFS.
- 127 Word Ladder — BFS optimality on an implicit graph.
- 207 Course Schedule / 210 Course Schedule II — Kahn, then report the order.
- 547 Number of Provinces / 684 Redundant Connection — union-find.
