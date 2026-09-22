# 11. Recursion, Backtracking, Linked Lists, Trees

## Concept

Lesson 10 exhausted what you can do by sweeping an array with indices. The
problems left over share one feature: the input has *structure that refers
to itself*. A linked list is a node plus a linked list. A tree is a node
plus two trees. A search space is a first choice plus a smaller search
space. Self-referential data wants self-referential code, and
self-referential code is proved by induction.

### The backtracking template

Every "enumerate all X" problem is a walk over a **decision tree**: each
level fixes one decision, each leaf is a candidate answer. The walk is
always the same three lines.

```python
def solve(...):
    out, path = [], []

    def explore(state):
        if is_complete(state):
            out.append(path[:])          # copy — path keeps mutating
            return
        for choice in choices(state):
            if not allowed(choice):      # pruning (optional)
                continue
            path.append(choice)          # choose
            explore(advance(state, choice))   # explore
            path.pop()                   # unchoose

    explore(initial)
    return out
```

`path` is one mutable buffer reused by the whole traversal. That is why
`out.append(path[:])` copies: append `path` itself and every entry in `out`
is the same object, empty by the time you look at it.

### Linked lists

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

There is no length, no index, no O(1) random access. You get one pointer
and the right to follow it. Three moves cover most problems:

- **Sentinel (dummy) head.** `dummy = ListNode(); tail = dummy` removes the
  "is this the first node?" special case; return `dummy.next`.
- **Three-pointer rewrite.** `prev`, `node`, `nxt` — reversal, in place.
- **Two speeds.** One pointer per step, one per two steps: finds the middle
  and detects cycles in O(1) space.

### Binary trees

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

Depth-first traversal is one recursion with three places to put the visit:

```python
def preorder(t):  return [] if t is None else [t.val] + preorder(t.left) + preorder(t.right)
def inorder(t):   return [] if t is None else inorder(t.left) + [t.val] + inorder(t.right)
def postorder(t): return [] if t is None else postorder(t.left) + postorder(t.right) + [t.val]
```

Same node order visited; different moment of recording. Preorder sees a
node before its subtrees (good for copying/serialising), inorder between
them (sorted order in a BST), postorder after (good for anything a node
needs from its children: heights, sums, deletions).

Breadth-first traversal is a queue, not a recursion. Take the current
queue length *first* and pop exactly that many, and each batch is exactly
one level:

```python
from collections import deque

def levels(root):
    out, q = [], deque([root] if root else [])
    while q:
        out.append([n.val for n in q])
        q = deque(c for n in q for c in (n.left, n.right) if c)
    return out
```

Python's recursion limit is ~1000 frames (`sys.getrecursionlimit()`). A
balanced tree of a million nodes is 20 deep and fine; a degenerate tree or
a long linked list is not. When depth is O(n), write the traversal with an
explicit stack.

## Why

### Why the choose/explore/unchoose template is correct

Model the run as a tree: a node is a state, its children are the states
reached by the allowed choices. `path` holds the choices on the path from
the root to the current node.

**Claim.** When `explore(s)` is called with `path = p`, it appends to `out`
exactly the completions of `p` — every complete solution whose choice
sequence begins with `p` — each exactly once, and it restores `path` to `p`
before returning.

**Proof** by induction on the height of the subtree rooted at `s` (finite,
because every choice strictly shrinks the remaining decisions).

*Base.* `s` is complete. The only completion of `p` is `p` itself; the code
appends a copy of it and returns without touching `path`. ✓

*Step.* `s` is incomplete. Every completion of `p` extends `p` by exactly
one allowed first choice c, so the set of completions of `p` is the
disjoint union over allowed c of the completions of `p + [c]` — disjoint
because different c give different sequences. The loop runs `explore` once
per allowed c with `path = p + [c]`; by the induction hypothesis each call
appends exactly the completions of `p + [c]`, once each, and leaves `path`
as `p + [c]`, which the `pop` returns to `p`. So the loop appends the
disjoint union, once each, and `path` is `p` on exit. ∎

Two things fall out. **The `pop` is not bookkeeping, it is the induction
hypothesis**: the IH assumes the caller's `path` is intact, so a missing
`unchoose` breaks correctness at every level above. And **pruning is safe
exactly when the pruned branch has no completions** — that is the proof
obligation for every `continue` you add.

### Counting the search space

A recursion tree with branching factor ≤ b and depth d has at most
(b^(d+1) − 1)/(b − 1) = O(b^d) nodes, and the leaves dominate. So the cost
is (number of leaves) × (work per leaf) plus (internal nodes) × (work per
node).

- **Subsets:** at each of n positions, include or exclude — 2^n leaves,
  each copied in O(n): Θ(2^n · n). The output alone is that big, so this
  is optimal.
- **Permutations:** n choices, then n−1, …: n! leaves. Total nodes
  Σ_{k=0..n} n!/(n−k)! < e·n!, so Θ(n! · n) with the copies.
- **Combinations of size k:** C(n, k) leaves.

Backtracking is exponential by nature. You are not trying to make it
polynomial; you are trying to make the constant and the pruning good.

### Why reversal works: the invariant

```python
prev, node = None, head
while node is not None:
    nxt = node.next
    node.next = prev
    prev, node = node, nxt
```

Invariant P: *`prev` heads the reversal of the first k nodes, `node` heads
the remaining n − k nodes in original order, and the two lists are disjoint
and together hold all n nodes.*

P holds before the loop with k = 0 (`prev` is None, `node` is the whole
list). One iteration: `nxt` saves the suffix *before* the link is
destroyed — omit that line and the rest of the list is unreachable —
`node.next = prev` makes `node` the new front of the reversed prefix, and
the rebinding re-establishes P with k+1. Each iteration decreases n − k, so
the loop ends with `node is None`, i.e. k = n, and P then says `prev` heads
the reversal of all n nodes. n iterations, O(1) extra space. ∎

### Why the fast and slow pointers must meet

Suppose the list has μ ≥ 0 nodes before the cycle and a cycle of length
λ ≥ 1. Number the nodes by distance from the head. After t steps
(with t ≥ μ) `slow` is at position μ + ((t − μ) mod λ) and `fast` at
μ + ((2t − μ) mod λ), both inside the cycle.

They occupy the same node iff 2t − μ ≡ t − μ (mod λ), i.e. **iff t ≡ 0
(mod λ)**. Take t = λ·⌈μ/λ⌉: it is a multiple of λ and t ≥ μ, so the two
pointers coincide at step t. And t < μ + λ ≤ n, so a meeting happens within
n steps. Conversely, if there is no cycle, `fast` reaches the end after
⌈n/2⌉ steps and the loop exits. Hence the algorithm returns True iff a
cycle exists, in O(n) time and O(1) space. ∎

(The step sizes 1 and 2 matter only in that the *gap* grows by exactly 1
per step, so it eventually hits a multiple of λ. Any pair (1, k) with k ≥ 2
also works; 2 is the cheapest.)

### Why merging two sorted lists is correct

Invariant: *the nodes already spliced after `dummy` are sorted, and every
one of them is ≤ every value still in `a` or `b`.* Initially the spliced
part is empty. Each iteration moves the smaller of the two heads. Because
both inputs are sorted, that head is ≤ everything remaining in its own
list, and by the branch test ≤ the other head, hence ≤ everything remaining
in the other list — so the invariant survives, and the appended value is ≥
the previous tail. When one list empties, the invariant says the other list
is entirely ≥ the output so far and already sorted, so appending it whole
finishes the job. Taking from `a` on ties makes the merge **stable**.
O(m + n) time, O(1) extra space — no new nodes are allocated. ∎

### Structural induction over trees

The induction principle for binary trees: to prove Q(T) for all finite
binary trees, prove Q(None) and prove Q(T) assuming Q(T.left) and
Q(T.right). This is exactly the shape of a recursive function, which is
why the proofs are short.

**Claim 1.** A binary tree of height h (h = nodes on the longest
root-to-leaf path) has at most 2^h − 1 nodes.

*Proof.* Base: the empty tree has height 0 and 0 = 2^0 − 1 nodes. Step: a
tree of height h ≥ 1 is a root plus two subtrees, each of height ≤ h − 1,
so by the IH n ≤ 1 + 2(2^(h−1) − 1) = 2^h − 1. ∎

Contrapositive, the bound you actually use: h ≥ log₂(n + 1). A balanced
tree achieves it; a chain has h = n. Every "O(h)" claim about trees is a
claim about *balance*, not about size.

**Claim 2.** In a binary tree, (number of nodes with 2 children) + 1 =
(number of leaves).

*Proof.* Induction on the tree. Empty: 0 + 1 ≠ 0 — so state it for
non-empty trees, where it reads d₂ + 1 = L. A single node: 0 + 1 = 1. ✓
A root with one non-empty subtree S: the root is not a leaf and has 1
child, so d₂ = d₂(S) and L = L(S), and the IH gives it. A root with two
non-empty subtrees S, T: d₂ = d₂(S) + d₂(T) + 1 and L = L(S) + L(T), so
d₂ + 1 = (L(S) − 1) + (L(T) − 1) + 2 = L. ∎

**Claim 3.** The inorder traversal of a BST is strictly increasing.

*Proof.* Induction. Empty: the empty sequence is sorted. For a node x with
subtrees L and R, inorder(T) = inorder(L) ++ [x.val] ++ inorder(R). By the
IH both parts are strictly increasing. The BST property says *every* value
in L is < x.val and *every* value in R is > x.val, so the concatenation is
strictly increasing across both joins. ∎

That "every value in the subtree", not "the child value", is the whole
difficulty of `is_valid_bst`. Checking `node.left.val < node.val` at each
node is *not* the BST property: the tree 5 / (4, 6) with 6's left child 3
passes every local check and fails Claim 3. The fix is to carry the
interval a subtree is allowed to occupy, and narrow it on the way down:
descending left replaces the upper bound with the node's value, descending
right replaces the lower bound. By induction on depth, the interval at a
node is exactly the constraint the ancestors impose, so the check is
complete.

## Worked examples

```python
>>> t = build_tree([3, 9, 20, None, None, 15, 7])
>>> inorder(t), preorder(t), postorder(t)
([9, 3, 15, 20, 7], [3, 9, 20, 15, 7], [9, 15, 7, 20, 3])
>>> level_order(t)
[[3], [9, 20], [15, 7]]
>>> max_depth(t)
3
```

Postorder is the shape to reach for whenever a node's answer is a function
of its children's answers — height, subtree sum, "is this subtree
balanced", diameter:

```python
>>> def diameter(t):
...     best = 0
...     def height(n):
...         nonlocal best
...         if n is None:
...             return 0
...         l, r = height(n.left), height(n.right)
...         best = max(best, l + r)      # path through n, in edges
...         return 1 + max(l, r)
...     height(t)
...     return best
>>> diameter(build_tree([1, 2, 3, 4, 5]))
3
```

One traversal, O(n) — the naive version recomputing heights per node is
O(n²) on a chain.

Backtracking, with and without pruning:

```python
>>> subsets([1, 2, 3])          # 2**3 leaves
[[], [3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]]
>>> len(permutations([1, 2, 3, 4]))
24
```

An n-queens-style prune is just an `allowed()` test — legal because a
partial placement with two queens attacking each other has *no*
completions, which is precisely the obligation from the proof above.

The two-speed pointer, used for the middle rather than a cycle:

```python
>>> def middle(head):
...     slow = fast = head
...     while fast and fast.next:
...         slow, fast = slow.next, fast.next.next
...     return slow
>>> middle(from_list([1, 2, 3, 4, 5])).val
3
```

After k iterations slow is at index k and fast at 2k; the loop ends at
k = ⌊n/2⌋, so slow lands on the upper middle. That plus `reverse_list` is
the whole of "is this list a palindrome" in O(1) space.

## Exercises

Open `exercises/11_patterns_trees.py`; run `python3 -m pytest exercises/11_patterns_trees.py`.

- `reverse_list(head)` — in place, O(1) space, with the invariant above.
- `has_cycle(head)` — Floyd's two pointers.
- `merge_two_lists(a, b)` — splice, don't copy; sentinel head.
- `max_depth(root)` — one line of structural induction.
- `level_order(root)` — BFS, one list per level.
- `is_valid_bst(root)` — carry the (low, high) interval down.
- `permutations(nums)` — choose/explore/unchoose over used positions.
- `subsets(nums)` — include/exclude at each index.

`ListNode`, `TreeNode`, `from_list`, `to_list`, and `build_tree` are given.

## LeetCode

- 206 Reverse Linked List — the invariant, verbatim.
- 141 Linked List Cycle — the meeting proof; 142 asks where the cycle starts.
- 21 Merge Two Sorted Lists — sentinel head; 23 generalises with a heap (lesson 12).
- 234 Palindrome Linked List — middle by two speeds, reverse the second half.
- 104 Maximum Depth of Binary Tree — the h ≤ n, h ≥ log₂(n+1) discussion.
- 102 Binary Tree Level Order Traversal — snapshot the queue length.
- 98 Validate Binary Search Tree — bounds, not local comparisons.
- 226 Invert Binary Tree / 101 Symmetric Tree — structural induction on two trees at once.
- 46 Permutations / 78 Subsets / 77 Combinations — the same template three ways.
- 39 Combination Sum / 51 N-Queens — the same template with a pruning proof.
- 236 Lowest Common Ancestor — postorder; the answer is where two searches meet.

## Next

Lesson 12: when the decision tree has *repeated* states, memoising it turns
exponential backtracking into polynomial dynamic programming — plus heaps
and graphs.
