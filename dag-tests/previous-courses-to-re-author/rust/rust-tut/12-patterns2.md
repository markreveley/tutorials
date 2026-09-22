# 12. Patterns II — Lists, Trees, Search, DP, Heaps

## Concept

The four remaining LeetCode families, in the shapes Rust actually forces on you.

### Linked lists: `Option<Box<ListNode>>`

```rust
pub struct ListNode {
    pub val: i32,
    pub next: Option<Box<ListNode>>,
}
```

This is LeetCode's Rust signature. Read it as "nullable owned pointer":
`Box<T>` is a non-null heap pointer with **unique** ownership, and `Option`
supplies the null. Thanks to the niche optimisation, `Option<Box<T>>` is the
same size as a pointer — the `None` case is represented by the address 0 that
`Box` can never hold. So this is C's `struct node *next` with no null
dereference and no leak.

The workhorse is `Option::take`:

```rust
pub fn take(&mut self) -> Option<T>   // replaces *self with None, returns the old value
```

### Trees: `Option<Rc<RefCell<TreeNode>>>`

```rust
pub struct TreeNode {
    pub val: i32,
    pub left:  Option<Rc<RefCell<TreeNode>>>,
    pub right: Option<Rc<RefCell<TreeNode>>>,
}
pub type Tree = Option<Rc<RefCell<TreeNode>>>;
```

- `Rc<T>` — **shared** ownership. `Rc::clone` bumps a non-atomic strong count
  in O(1) and hands you another handle to the *same* node; the node is dropped
  when the count hits 0. `Rc` gives out `&T` only.
- `RefCell<T>` — **interior mutability**. `borrow()` and `borrow_mut()` check
  the aliasing rule at run time against a counter in the cell, and **panic**
  (`already borrowed` / `already mutably borrowed`) instead of failing to
  compile.

Together, `Rc<RefCell<T>>` = shared mutable, aliasing checked dynamically.

```rust
let n = Rc::new(RefCell::new(TreeNode::new(1)));
let alias = Rc::clone(&n);                 // O(1), same node
n.borrow_mut().val = 7;
assert_eq!(alias.borrow().val, 7);
```

### DFS / BFS

DFS is recursion over the structure (or an explicit `Vec` stack). BFS is a
`VecDeque`, and the level-by-level shape is:

```rust
while !q.is_empty() {
    let width = q.len();            // snapshot: exactly one level
    for _ in 0..width { /* pop, record, push children */ }
}
```

### Dynamic programming

Bottom-up: a `Vec` indexed by subproblem, filled in an order where every
dependency is already computed.

```rust
let mut best = vec![INF; amount + 1];
best[0] = 0;
for a in 1..=amount { for &c in coins { /* best[a] = min(best[a], best[a-c]+1) */ } }
```

### Heaps

`BinaryHeap` + `Reverse` (lesson 09). Two shapes: size-k min-heap for top-k,
and a priority queue keyed by tentative distance for Dijkstra.

## Why

### Why list reversal needs `take()`, and why the obvious version does not compile

Here is the version everyone writes first:

```rust
let mut prev: Option<Box<ListNode>> = None;
let mut cur = head;
while let Some(node) = &mut cur {          // borrow the current node
    let next = node.next;                  // E0507: cannot move out of borrow
    node.next = prev;                      // E0382: prev was moved (last round)
    prev = cur;                            // E0506: cur is borrowed by `node`
    cur = next;
}
```

Three errors, one cause. Every node is owned by **exactly one place**: either
the `head`/`cur` binding, or the `next` field of its predecessor. Reversal is
precisely the operation that rewires those places, so at some instant a field
must give up its value. Rust has no "temporarily moved-out" state for a place
reached through a reference: a `&mut ListNode` must point at a *fully valid*
`ListNode` at every instant, because a panic (or any other code that sees it)
could observe it. Moving `node.next` out would leave a hole.

`take()` is the primitive that closes the hole in the same expression that
opens it: it writes `None` into the field and returns the old value. `None` is
a perfectly valid `Option<Box<ListNode>>`, so the type's invariant never breaks.

```rust
pub fn reverse_list(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut prev: Option<Box<ListNode>> = None;
    let mut cur = head;
    while let Some(mut node) = cur {       // MOVE the box out of cur
        cur = node.next.take();            // detach the tail, leaving None
        node.next = prev;                  // splice onto the reversed prefix
        prev = Some(node);                 // hand ownership to prev
    }
    prev
}
```

Why this one is accepted: `while let Some(mut node) = cur` **moves** out of
`cur`, which is legal because `cur` is a local variable, not a place behind a
reference — the compiler tracks it as moved-from and the very next line
reassigns it. `node` now owns its box outright, so mutating `node.next` needs no
outer borrow. At every line, each node has exactly one owner.

**Invariant.** `prev` is the reversal of the processed prefix, `cur` is the
untouched suffix, and the two lists are disjoint and together contain every
original node. Establishment: `prev = None`, `cur = head`. Preservation: the
loop body moves the head of `cur` to the front of `prev`. Exit: `cur = None`, so
`prev` is the reversal of the whole list. Measure: length of `cur`, strictly
decreasing. **O(n) time, O(1) extra space.** ∎

Recursive reversal is O(n) stack, and on LeetCode's 5·10⁴-node inputs that is a
real overflow risk. Prefer the loop.

### Why `Option<Box<_>>` cannot have a cycle — and what that means for LC 141

`Box` is *unique* ownership: each node has exactly one owner, and drop is
recursive. Suppose a cycle `v₀ → v₁ → … → v_k → v₀` existed through `next`
fields. Then `v₀` is owned by `v_k`, which is owned by `v_{k−1}`, … , which is
owned by `v₀`. But `v₀` was also owned by whatever handed it to the list head,
giving it two owners — contradiction with uniqueness. Constructively, to build
the cycle you would need `v₀` to already exist and be complete before `v_k` is
constructed, and then to move `v₀` into `v_k.next` while `v₀` still owns the
chain that reaches `v_k` — the move checker rejects it.

So "Linked List Cycle" is not expressible against this type. The honest
formulations are: use `Rc`/`Weak` (shared ownership admits cycles, at the cost
of leaks unless back-edges are `Weak`), use raw pointers with `unsafe`, or
represent the successor relation as data. This lesson takes the last option:

```rust
pub fn has_cycle(next: &[Option<usize>], start: usize) -> bool
```

Floyd on `i ↦ next[i]`: the hare takes two steps per tortoise step. If the walk
from `start` enters a cycle of length λ after a tail of length μ, then once both
are inside the cycle their separation changes by exactly 1 per round, so it hits
0 within λ rounds; if there is no cycle the hare falls off the end and returns
`false`. O(μ + λ) time, O(1) space.

### Why `Rc<RefCell<_>>` for trees, and what it costs

BFS is the forcing example. The queue must hold node handles while the parent
still holds them, so a `&`-borrow of the parent would have to outlive the loop
iteration that created it — the borrow checker cannot see that the tree is not
mutated meanwhile. `Rc` sidesteps it: the queue owns its own handles, and the
lifetime question disappears because there are no references, only counted
owners. And since problems that *build* or *rewrite* trees need mutation through
a shared handle, `RefCell` supplies it with a run-time check.

The costs, which you should state:

- **Space:** an `Rc` allocation carries two `usize` counters (strong, weak)
  beside the value, and `RefCell` adds one more `usize` borrow flag. On 64-bit,
  a `TreeNode` costs ~24 bytes of bookkeeping over its ~24 bytes of payload.
- **Time:** `Rc::clone`/drop are a non-atomic increment/decrement plus a branch;
  `borrow()`/`borrow_mut()` are a load, a check, a store, and a branch. All
  O(1), all unelidable — the check cannot be optimised out the way a compile-
  time borrow can.
- **Panics:** `borrow_mut()` while any borrow is live aborts the program. The
  usual trigger is holding a `Ref` across a recursive call that borrows the same
  node. Keep borrows short; bind them in the narrowest scope.
- **Leaks:** `Rc` cycles never drop. Trees are acyclic, so this is safe — but
  the moment you add parent pointers they must be `Weak<RefCell<TreeNode>>`.

`max_depth` shows the idiom: borrow, clone the children out, drop the borrow.

```rust
pub fn max_depth(root: Tree) -> i32 {
    match root {
        None => 0,
        Some(node) => {
            let n = node.borrow();
            1 + max_depth(n.left.clone()).max(max_depth(n.right.clone()))
        }
    }
}
```

Correctness is structural induction. Base: the empty tree has depth 0. Step:
assuming the result for both (strictly smaller) subtrees, the deepest root-to-
leaf path goes through one of them, so the depth is `1 + max(dl, dr)`. Every
node is visited once ⇒ **O(n) time, O(h) stack**, and `h = n` for a degenerate
tree.

### Why the BFS level snapshot is correct

**Invariant:** at the top of each outer iteration the queue holds exactly the
nodes of one depth level, in left-to-right order.

Establishment: the queue holds only the root, which is level 0.
Preservation: `width = q.len()` freezes the level's size *before* any children
are pushed. The `for` pops exactly those `width` nodes and appends their
children to the back. Since a `VecDeque` is FIFO, the children land after every
remaining node of the current level, so when the `for` finishes the queue
contains exactly the next level, left to right.
Termination: every node is enqueued exactly once (only via its unique parent),
so the total work is n pops and n pushes. **O(n) time, O(max width) space.** ∎

The same argument, with a `seen` grid replacing "unique parent", covers grid
BFS (`num_islands`): each cell is marked before it is enqueued, so it enters the
queue at most once ⇒ O(rows·cols).

### Why the DP recurrences are correct

**Climbing stairs.** Let `W(n)` be the number of ways to reach step n with
1- and 2-steps. Any path to n has a last move, from `n−1` or from `n−2`, and
these cases are disjoint and exhaustive, so `W(n) = W(n−1) + W(n−2)` for
`n ≥ 2`, with `W(0) = 1` (the empty path) and `W(1) = 1`. Two rolling variables
suffice because the recurrence has depth 2. **O(n) time, O(1) space.** Note
`W(n)` is Fibonacci shifted, and it exceeds `u32` at n = 47 — return `u64`.

**Coin change.** Let `B(a)` be the fewest coins summing to a, `∞` if
impossible. If a feasible solution for `a > 0` exists, it uses some coin c,
leaving a solution for `a − c`; that remainder must itself be optimal, or
replacing it would beat the optimum. Hence

    B(0) = 0
    B(a) = 1 + min { B(a − c) : c ∈ coins, c ≤ a }     (min ∅ = ∞)

Every `B(a − c)` has `a − c < a`, so filling `a` in increasing order means each
dependency is already final — this is the induction that bottom-up order
encodes. **O(amount·|coins|) time, O(amount) space.** Use a sentinel and check
it (`best[a-c] != INF`) rather than adding 1 to `u32::MAX`, which overflows.

**House robber.** `B(i) = max(B(i−1), B(i−2) + v[i])`: either skip house i, or
take it and forfeit `i−1`. Disjoint and exhaustive again. Two rolling scalars,
O(n) time, O(1) space.

### Why Dijkstra needs a min-heap, and why stale entries are fine

`BinaryHeap` has no `decrease_key`. The standard std-only workaround is **lazy
deletion**: push `(new_dist, v)` on every improvement, and when popping, skip
any entry whose distance no longer matches `dist[v]`.

```rust
while let Some(Reverse((d, u))) = heap.pop() {
    if dist[u] != Some(d) { continue; }        // stale
    ...
}
```

**Invariant:** when `(d, u)` is popped with `d == dist[u]`, `d` is the true
shortest distance to u. Proof sketch (requires non-negative weights): let P be a
true shortest path to u and let `(x, y)` be its first edge leaving the settled
set. Then `dist[y] ≤ d(x) + w(x,y) ≤ d(u)` was already pushed, so `y` would have
been popped before `u` unless `y = u`. Non-negativity is what makes the prefix
of P no longer than P; with a negative edge the argument collapses and you need
Bellman–Ford.

Each edge causes at most one push, so the heap holds ≤ E entries and each of the
≤ E pops costs O(log E) = O(log V) for simple graphs. **O((V + E) log V) time,
O(V + E) space.** Top-k via a size-k heap is the same machinery with a fixed
capacity: n pushes and ≤ n pops on a heap of size ≤ k ⇒ **O(n log k)**.

## Worked examples

```rust
// Lists: build / reverse / merge, all by moving ownership
assert_eq!(flatten_list(&reverse_list(build_list(&[1, 2, 3, 4]))), vec![4, 3, 2, 1]);
let m = merge_two_lists(build_list(&[1, 2, 4]), build_list(&[1, 3, 4]));
assert_eq!(flatten_list(&m), vec![1, 1, 2, 3, 4, 4]);

// merge_two_lists keeps a `tail: &mut Box<ListNode>` cursor into the output.
// Reborrowing it — `tail = tail.next.as_mut().unwrap()` — is legal because the
// old borrow ends at the assignment. A dummy head removes the empty-output case.

// Trees, from LeetCode's level-order serialization
let t = build_tree(&[Some(3), Some(9), Some(20), None, None, Some(15), Some(7)]);
assert_eq!(max_depth(t.clone()), 3);            // clone = Rc count bump, O(1)
assert_eq!(level_order(t.clone()), vec![vec![3], vec![9, 20], vec![15, 7]]);
assert_eq!(inorder(t), vec![9, 3, 15, 20, 7]);

// DP
assert_eq!(climb_stairs(5), 8);
assert_eq!(coin_change(&[1, 2, 5], 11), Some(3));   // 5 + 5 + 1
assert_eq!(coin_change(&[2], 3), None);
assert_eq!(house_robber(&[2, 7, 9, 3, 1]), 12);     // 2 + 9 + 1

// Heaps
assert_eq!(top_k_frequent(&[1, 1, 1, 2, 2, 3], 2), vec![1, 2]);
let adj = vec![vec![(1, 1u64), (2, 4)], vec![(2, 2)], vec![], vec![]];
assert_eq!(dijkstra(&adj, 0), vec![Some(0), Some(1), Some(3), None]);
```

Borrow-checker survival notes:

- Bind a `RefCell` borrow to a short-lived local: `let n = node.borrow();`.
  Do not hold it across a call that may borrow the same node again.
- `Rc::clone(&x)` is preferred over `x.clone()` at call sites: it says "this is
  a refcount bump, not a deep copy".
- Recursive helpers over trees should take `&Tree` (see `inorder`) so callers
  do not clone at every level; the LeetCode-facing signature still takes `Tree`
  by value.
- `vec![vec![false; cols]; rows]` is the idiomatic visited grid. Indices are
  `usize`, so do neighbour arithmetic in `i64` and bounds-check before casting
  back — `r - 1` underflows and panics at `r == 0`.

## Exercises

Open `exercises/src/l12_patterns2.rs`; run `cargo test -p exercises l12`.
Start with the helpers — the tests are written in terms of them.

- `ListNode::new`, `build_list`, `flatten_list` — the two conversions.
- `reverse_list`, `merge_two_lists` — ownership juggling with `take()` and a
  `&mut` tail cursor.
- `has_cycle` — Floyd over a successor table; explain in a comment why the
  `Box` list cannot be used.
- `TreeNode::new`, `build_tree`, `max_depth`, `inorder`, `level_order` —
  `Rc<RefCell<_>>`, structural induction, and the level snapshot.
- `num_islands` — grid BFS with a visited matrix.
- `climb_stairs`, `coin_change`, `house_robber` — bottom-up DP; write the
  recurrence as a comment first.
- `top_k_frequent`, `dijkstra` — `BinaryHeap` with `Reverse`, size-k eviction
  and lazy deletion.

## LeetCode

- 206 Reverse Linked List — `take()`, O(1) space.
- 21 Merge Two Sorted Lists — dummy head plus a `&mut` tail.
- 141 Linked List Cycle — Floyd; note the Rust representation problem.
- 876 Middle of the Linked List — fast/slow.
- 234 Palindrome Linked List — reverse the second half in place.
- 104 Maximum Depth of Binary Tree — structural induction.
- 226 Invert Binary Tree — `RefCell` mutation through `Rc`.
- 102 Binary Tree Level Order Traversal — the level snapshot.
- 94 Binary Tree Inorder Traversal — recursive, then the explicit stack.
- 98 Validate Binary Search Tree — carry (lo, hi) bounds down the recursion.
- 200 Number of Islands — grid BFS/DFS.
- 133 Clone Graph — `Rc` plus a `HashMap` from old node to new.
- 70 Climbing Stairs — the base DP.
- 198 House Robber — two rolling scalars.
- 322 Coin Change — unbounded knapsack.
- 300 Longest Increasing Subsequence — O(n²) DP, then O(n log n) with a
  lower-bound binary search (lesson 11).
- 347 Top K Frequent Elements — size-k heap, O(n log k).
- 215 Kth Largest Element in an Array — size-k min-heap.
- 23 Merge k Sorted Lists — a heap over list heads, plus lesson 12's list
  ownership dance.
- 743 Network Delay Time — Dijkstra, verbatim.
