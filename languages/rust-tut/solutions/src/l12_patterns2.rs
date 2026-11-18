//! Lesson 12 — LeetCode patterns II: linked lists, trees, graph search, DP, heaps.

use std::cell::RefCell;
use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap, VecDeque};
use std::rc::Rc;

// ---------------------------------------------------------------- linked list

/// LeetCode's singly linked list. `Option<Box<T>>` = "nullable owned pointer",
/// with no null and no leak. `Box` is *unique* ownership, so this type is
/// structurally acyclic.
#[derive(Debug, PartialEq, Eq, Clone)]
pub struct ListNode {
    pub val: i32,
    pub next: Option<Box<ListNode>>,
}

impl ListNode {
    pub fn new(val: i32) -> Self {
        ListNode { val, next: None }
    }
}

/// Build a list from a slice. O(n).
pub fn build_list(xs: &[i32]) -> Option<Box<ListNode>> {
    let mut head: Option<Box<ListNode>> = None;
    for &x in xs.iter().rev() {
        head = Some(Box::new(ListNode { val: x, next: head }));
    }
    head
}

/// Collect the values, borrowing only. O(n).
pub fn flatten_list(head: &Option<Box<ListNode>>) -> Vec<i32> {
    let mut out = Vec::new();
    let mut cur = head;
    while let Some(node) = cur {
        out.push(node.val);
        cur = &node.next;
    }
    out
}

/// LC 206. Reverse in place by moving ownership node by node.
/// Invariant: `prev` is the already-reversed prefix, `cur` the untouched suffix,
/// and every node is owned by exactly one of them. O(n) time, O(1) space.
pub fn reverse_list(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut prev: Option<Box<ListNode>> = None;
    let mut cur = head;
    while let Some(mut node) = cur {
        cur = node.next.take();
        node.next = prev;
        prev = Some(node);
    }
    prev
}

/// LC 21. Merge two sorted lists into one sorted list, consuming both. O(n + m).
pub fn merge_two_lists(
    a: Option<Box<ListNode>>,
    b: Option<Box<ListNode>>,
) -> Option<Box<ListNode>> {
    let mut dummy = Box::new(ListNode::new(0));
    let mut tail = &mut dummy;
    let (mut a, mut b) = (a, b);
    loop {
        match (a.take(), b.take()) {
            (None, None) => break,
            (Some(x), None) => {
                tail.next = Some(x);
                break;
            }
            (None, Some(y)) => {
                tail.next = Some(y);
                break;
            }
            (Some(mut x), Some(y)) if x.val <= y.val => {
                a = x.next.take();
                b = Some(y);
                tail.next = Some(x);
                tail = tail.next.as_mut().unwrap();
            }
            (Some(x), Some(mut y)) => {
                b = y.next.take();
                a = Some(x);
                tail.next = Some(y);
                tail = tail.next.as_mut().unwrap();
            }
        }
    }
    dummy.next
}

/// LC 141-shaped. `Option<Box<_>>` cannot express a cycle, so the graph is given
/// as a successor table: `next[i]` is the node after `i`, `None` for the end.
/// Floyd's tortoise and hare: O(n) time, O(1) space.
pub fn has_cycle(next: &[Option<usize>], start: usize) -> bool {
    let step = |i: Option<usize>| -> Option<usize> { i.and_then(|i| next[i]) };
    let mut slow = Some(start);
    let mut fast = Some(start);
    loop {
        fast = step(step(fast));
        slow = step(slow);
        match (slow, fast) {
            (_, None) => return false,
            (Some(s), Some(f)) if s == f => return true,
            _ => {}
        }
    }
}

// ---------------------------------------------------------------------- trees

/// LeetCode's binary tree node. `Rc` gives shared ownership (a child handle can
/// live in a queue *and* in its parent); `RefCell` moves the borrow check to run
/// time so the shared node stays mutable.
#[derive(Debug, PartialEq, Eq)]
pub struct TreeNode {
    pub val: i32,
    pub left: Option<Rc<RefCell<TreeNode>>>,
    pub right: Option<Rc<RefCell<TreeNode>>>,
}

impl TreeNode {
    pub fn new(val: i32) -> Self {
        TreeNode { val, left: None, right: None }
    }
}

/// Exactly LeetCode's `root` type; the alias only saves typing.
pub type Tree = Option<Rc<RefCell<TreeNode>>>;

/// Build from LeetCode's level-order serialization, `None` for a missing child.
pub fn build_tree(vals: &[Option<i32>]) -> Tree {
    let first = vals.first().copied().flatten()?;
    let root = Rc::new(RefCell::new(TreeNode::new(first)));
    let mut q: VecDeque<Rc<RefCell<TreeNode>>> = VecDeque::new();
    q.push_back(Rc::clone(&root));
    let mut i = 1usize;
    while i < vals.len() {
        let node = match q.pop_front() {
            Some(n) => n,
            None => break,
        };
        for side in 0..2 {
            if i >= vals.len() {
                break;
            }
            if let Some(v) = vals[i] {
                let child = Rc::new(RefCell::new(TreeNode::new(v)));
                if side == 0 {
                    node.borrow_mut().left = Some(Rc::clone(&child));
                } else {
                    node.borrow_mut().right = Some(Rc::clone(&child));
                }
                q.push_back(child);
            }
            i += 1;
        }
    }
    Some(root)
}

/// LC 104. Depth by structural induction: 0 for the empty tree, else 1 + max of children.
/// O(n) time, O(h) stack.
pub fn max_depth(root: Tree) -> i32 {
    match root {
        None => 0,
        Some(node) => {
            let n = node.borrow();
            1 + max_depth(n.left.clone()).max(max_depth(n.right.clone()))
        }
    }
}

/// Inorder traversal (left, node, right) — sorted for a BST. O(n).
pub fn inorder(root: Tree) -> Vec<i32> {
    fn go(node: &Tree, out: &mut Vec<i32>) {
        if let Some(rc) = node {
            let n = rc.borrow();
            go(&n.left, out);
            out.push(n.val);
            go(&n.right, out);
        }
    }
    let mut out = Vec::new();
    go(&root, &mut out);
    out
}

/// LC 102. Level order (BFS). Invariant: at the top of each outer iteration the
/// queue holds exactly one full level, left to right. O(n) time, O(width) space.
pub fn level_order(root: Tree) -> Vec<Vec<i32>> {
    let mut out = Vec::new();
    let mut q: VecDeque<Rc<RefCell<TreeNode>>> = VecDeque::new();
    if let Some(r) = root {
        q.push_back(r);
    }
    while !q.is_empty() {
        let width = q.len();
        let mut level = Vec::with_capacity(width);
        for _ in 0..width {
            let node = q.pop_front().unwrap();
            let n = node.borrow();
            level.push(n.val);
            if let Some(l) = &n.left {
                q.push_back(Rc::clone(l));
            }
            if let Some(r) = &n.right {
                q.push_back(Rc::clone(r));
            }
        }
        out.push(level);
    }
    out
}

/// LC 200. Count connected components of '1' cells (4-neighbourhood) by BFS.
/// Each cell is enqueued at most once ⇒ O(rows·cols).
pub fn num_islands(grid: &[Vec<char>]) -> i32 {
    if grid.is_empty() {
        return 0;
    }
    let (rows, cols) = (grid.len(), grid[0].len());
    let mut seen = vec![vec![false; cols]; rows];
    let mut count = 0;
    for r in 0..rows {
        for c in 0..cols {
            if grid[r][c] != '1' || seen[r][c] {
                continue;
            }
            count += 1;
            let mut q = VecDeque::new();
            q.push_back((r, c));
            seen[r][c] = true;
            while let Some((y, x)) = q.pop_front() {
                let deltas = [(0i64, 1i64), (0, -1), (1, 0), (-1, 0)];
                for (dy, dx) in deltas {
                    let (ny, nx) = (y as i64 + dy, x as i64 + dx);
                    if ny < 0 || nx < 0 || ny >= rows as i64 || nx >= cols as i64 {
                        continue;
                    }
                    let (ny, nx) = (ny as usize, nx as usize);
                    if grid[ny][nx] == '1' && !seen[ny][nx] {
                        seen[ny][nx] = true;
                        q.push_back((ny, nx));
                    }
                }
            }
        }
    }
    count
}

// ------------------------------------------------------------------------- DP

/// LC 70. `ways(n) = ways(n-1) + ways(n-2)`, `ways(0) = ways(1) = 1`.
/// Bottom-up with two rolling variables: O(n) time, O(1) space.
pub fn climb_stairs(n: u32) -> u64 {
    let (mut a, mut b) = (1u64, 1u64);
    for _ in 0..n {
        let next = a + b;
        a = b;
        b = next;
    }
    a
}

/// LC 322. Fewest coins summing to `amount`, or `None`.
/// Recurrence: `best[a] = 1 + min over coins c ≤ a of best[a - c]`, `best[0] = 0`.
/// O(amount · |coins|) time, O(amount) space.
pub fn coin_change(coins: &[i32], amount: i32) -> Option<u32> {
    if amount < 0 {
        return None;
    }
    let amount = amount as usize;
    let inf = u32::MAX;
    let mut best = vec![inf; amount + 1];
    best[0] = 0;
    for a in 1..=amount {
        for &c in coins {
            if c <= 0 {
                continue;
            }
            let c = c as usize;
            if c <= a && best[a - c] != inf {
                best[a] = best[a].min(best[a - c] + 1);
            }
        }
    }
    if best[amount] == inf { None } else { Some(best[amount]) }
}

/// LC 198. Max non-adjacent sum. `best[i] = max(best[i-1], best[i-2] + v[i])`.
/// O(n) time, O(1) space.
pub fn house_robber(vals: &[i32]) -> i64 {
    let (mut skip, mut take) = (0i64, 0i64);
    for &v in vals {
        let new_take = skip + v as i64;
        skip = skip.max(take);
        take = new_take;
    }
    skip.max(take)
}

// ---------------------------------------------------------------------- heaps

/// LC 347. The `k` most frequent values, most frequent first; ties by larger value.
/// Counting is O(n); a size-`k` min-heap keyed by (count, value) is O(n log k).
pub fn top_k_frequent(nums: &[i32], k: usize) -> Vec<i32> {
    let mut counts: HashMap<i32, usize> = HashMap::new();
    for &x in nums {
        *counts.entry(x).or_insert(0) += 1;
    }
    let mut heap: BinaryHeap<Reverse<(usize, i32)>> = BinaryHeap::new();
    for (v, c) in counts {
        heap.push(Reverse((c, v)));
        if heap.len() > k {
            heap.pop();
        }
    }
    let mut out: Vec<(usize, i32)> = heap.into_iter().map(|Reverse(p)| p).collect();
    out.sort_unstable_by(|a, b| b.cmp(a));
    out.into_iter().map(|(_, v)| v).collect()
}

/// Dijkstra from `src` over non-negative weights; `None` = unreachable.
/// `Reverse` turns the max-heap into a min-heap. Invariant: when `(d, u)` is
/// popped with `d == dist[u]`, `d` is final. O((V + E) log V).
pub fn dijkstra(adj: &[Vec<(usize, u64)>], src: usize) -> Vec<Option<u64>> {
    let mut dist: Vec<Option<u64>> = vec![None; adj.len()];
    if src >= adj.len() {
        return dist;
    }
    let mut heap: BinaryHeap<Reverse<(u64, usize)>> = BinaryHeap::new();
    dist[src] = Some(0);
    heap.push(Reverse((0, src)));
    while let Some(Reverse((d, u))) = heap.pop() {
        if dist[u] != Some(d) {
            continue; // stale entry
        }
        for &(v, w) in &adj[u] {
            let nd = d + w;
            if dist[v].is_none_or(|old| nd < old) {
                dist[v] = Some(nd);
                heap.push(Reverse((nd, v)));
            }
        }
    }
    dist
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn lists() {
        assert_eq!(flatten_list(&build_list(&[1, 2, 3])), vec![1, 2, 3]);
        assert_eq!(flatten_list(&build_list(&[])), Vec::<i32>::new());
        assert_eq!(flatten_list(&reverse_list(build_list(&[1, 2, 3, 4]))), vec![4, 3, 2, 1]);
        assert_eq!(flatten_list(&reverse_list(build_list(&[]))), Vec::<i32>::new());
        assert_eq!(flatten_list(&reverse_list(build_list(&[7]))), vec![7]);
        let merged = merge_two_lists(build_list(&[1, 2, 4]), build_list(&[1, 3, 4]));
        assert_eq!(flatten_list(&merged), vec![1, 1, 2, 3, 4, 4]);
        assert_eq!(flatten_list(&merge_two_lists(None, build_list(&[5]))), vec![5]);
        assert_eq!(flatten_list(&merge_two_lists(None, None)), Vec::<i32>::new());
    }

    #[test]
    fn cycles() {
        // 0 -> 1 -> 2 -> 3 -> None
        let acyclic = [Some(1), Some(2), Some(3), None];
        assert!(!has_cycle(&acyclic, 0));
        // 0 -> 1 -> 2 -> 1 -> ...
        let cyclic = [Some(1), Some(2), Some(1), None];
        assert!(has_cycle(&cyclic, 0));
        // self loop
        assert!(has_cycle(&[Some(0)], 0));
        assert!(!has_cycle(&[None], 0));
    }

    #[test]
    fn trees() {
        let t = build_tree(&[Some(3), Some(9), Some(20), None, None, Some(15), Some(7)]);
        assert_eq!(max_depth(t.clone()), 3);
        assert_eq!(level_order(t.clone()), vec![vec![3], vec![9, 20], vec![15, 7]]);
        assert_eq!(inorder(t), vec![9, 3, 15, 20, 7]);
        assert_eq!(max_depth(None), 0);
        assert_eq!(level_order(None), Vec::<Vec<i32>>::new());
        let bst = build_tree(&[Some(4), Some(2), Some(6), Some(1), Some(3), Some(5), Some(7)]);
        assert_eq!(inorder(bst), vec![1, 2, 3, 4, 5, 6, 7]);
    }

    #[test]
    fn grids() {
        let g: Vec<Vec<char>> = ["11000", "11000", "00100", "00011"]
            .iter()
            .map(|r| r.chars().collect())
            .collect();
        assert_eq!(num_islands(&g), 3);
        assert_eq!(num_islands(&[]), 0);
        assert_eq!(num_islands(&[vec!['0']]), 0);
    }

    #[test]
    fn dp() {
        assert_eq!(climb_stairs(0), 1);
        assert_eq!(climb_stairs(1), 1);
        assert_eq!(climb_stairs(2), 2);
        assert_eq!(climb_stairs(5), 8);
        assert_eq!(coin_change(&[1, 2, 5], 11), Some(3));
        assert_eq!(coin_change(&[2], 3), None);
        assert_eq!(coin_change(&[2], 0), Some(0));
        assert_eq!(house_robber(&[2, 7, 9, 3, 1]), 12);
        assert_eq!(house_robber(&[]), 0);
    }

    #[test]
    fn heaps() {
        assert_eq!(top_k_frequent(&[1, 1, 1, 2, 2, 3], 2), vec![1, 2]);
        assert_eq!(top_k_frequent(&[1], 1), vec![1]);
        assert_eq!(top_k_frequent(&[4, 4, 5, 5, 6], 2), vec![5, 4]);
        // 0 --1-- 1 --2-- 2, 0 --4-- 2, node 3 isolated
        let adj: Vec<Vec<(usize, u64)>> =
            vec![vec![(1, 1), (2, 4)], vec![(2, 2)], vec![], vec![]];
        assert_eq!(dijkstra(&adj, 0), vec![Some(0), Some(1), Some(3), None]);
        assert_eq!(dijkstra(&adj, 3), vec![None, None, None, Some(0)]);
    }
}
