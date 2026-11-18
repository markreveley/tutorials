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
        todo!()
    }
}

/// Build a list from a slice. O(n).
pub fn build_list(xs: &[i32]) -> Option<Box<ListNode>> {
    todo!()
}

/// Collect the values, borrowing only. O(n).
pub fn flatten_list(head: &Option<Box<ListNode>>) -> Vec<i32> {
    todo!()
}

/// LC 206. Reverse in place by moving ownership node by node.
/// Invariant: `prev` is the already-reversed prefix, `cur` the untouched suffix,
/// and every node is owned by exactly one of them. O(n) time, O(1) space.
pub fn reverse_list(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    todo!()
}

/// LC 21. Merge two sorted lists into one sorted list, consuming both. O(n + m).
pub fn merge_two_lists(
    a: Option<Box<ListNode>>,
    b: Option<Box<ListNode>>,
) -> Option<Box<ListNode>> {
    todo!()
}

/// LC 141-shaped. `Option<Box<_>>` cannot express a cycle, so the graph is given
/// as a successor table: `next[i]` is the node after `i`, `None` for the end.
/// Floyd's tortoise and hare: O(n) time, O(1) space.
pub fn has_cycle(next: &[Option<usize>], start: usize) -> bool {
    todo!()
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
        todo!()
    }
}

/// Exactly LeetCode's `root` type; the alias only saves typing.
pub type Tree = Option<Rc<RefCell<TreeNode>>>;

/// Build from LeetCode's level-order serialization, `None` for a missing child.
pub fn build_tree(vals: &[Option<i32>]) -> Tree {
    todo!()
}

/// LC 104. Depth by structural induction: 0 for the empty tree, else 1 + max of children.
/// O(n) time, O(h) stack.
pub fn max_depth(root: Tree) -> i32 {
    todo!()
}

/// Inorder traversal (left, node, right) — sorted for a BST. O(n).
pub fn inorder(root: Tree) -> Vec<i32> {
    todo!()
}

/// LC 102. Level order (BFS). Invariant: at the top of each outer iteration the
/// queue holds exactly one full level, left to right. O(n) time, O(width) space.
pub fn level_order(root: Tree) -> Vec<Vec<i32>> {
    todo!()
}

/// LC 200. Count connected components of '1' cells (4-neighbourhood) by BFS.
/// Each cell is enqueued at most once ⇒ O(rows·cols).
pub fn num_islands(grid: &[Vec<char>]) -> i32 {
    todo!()
}

// ------------------------------------------------------------------------- DP

/// LC 70. `ways(n) = ways(n-1) + ways(n-2)`, `ways(0) = ways(1) = 1`.
/// Bottom-up with two rolling variables: O(n) time, O(1) space.
pub fn climb_stairs(n: u32) -> u64 {
    todo!()
}

/// LC 322. Fewest coins summing to `amount`, or `None`.
/// Recurrence: `best[a] = 1 + min over coins c ≤ a of best[a - c]`, `best[0] = 0`.
/// O(amount · |coins|) time, O(amount) space.
pub fn coin_change(coins: &[i32], amount: i32) -> Option<u32> {
    todo!()
}

/// LC 198. Max non-adjacent sum. `best[i] = max(best[i-1], best[i-2] + v[i])`.
/// O(n) time, O(1) space.
pub fn house_robber(vals: &[i32]) -> i64 {
    todo!()
}

// ---------------------------------------------------------------------- heaps

/// LC 347. The `k` most frequent values, most frequent first; ties by larger value.
/// Counting is O(n); a size-`k` min-heap keyed by (count, value) is O(n log k).
pub fn top_k_frequent(nums: &[i32], k: usize) -> Vec<i32> {
    todo!()
}

/// Dijkstra from `src` over non-negative weights; `None` = unreachable.
/// `Reverse` turns the max-heap into a min-heap. Invariant: when `(d, u)` is
/// popped with `d == dist[u]`, `d` is final. O((V + E) log V).
pub fn dijkstra(adj: &[Vec<(usize, u64)>], src: usize) -> Vec<Option<u64>> {
    todo!()
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
