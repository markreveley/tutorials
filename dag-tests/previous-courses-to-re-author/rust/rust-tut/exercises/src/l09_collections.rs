//! Lesson 09 — collections: Vec, String, HashMap/Set, VecDeque, BinaryHeap, BTree*.

use std::cmp::Reverse;
use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};

/// Number of Unicode scalar values in `s`. O(n): the UTF-8 bytes must be walked.
pub fn char_count(s: &str) -> usize {
    todo!()
}

/// The `n`-th `char` of `s`, or `None`. O(n) — there is no O(1) answer (see the lesson).
pub fn nth_char(s: &str, n: usize) -> Option<char> {
    todo!()
}

/// `(bytes, chars)`. Equal for pure ASCII, different as soon as a multi-byte scalar appears.
pub fn byte_len_vs_char_len(s: &str) -> (usize, usize) {
    todo!()
}

/// Reverse by scalar value. Note this is *not* grapheme reversal.
pub fn reverse_chars(s: &str) -> String {
    todo!()
}

/// Lowercase whitespace-separated word counts, built with the Entry API.
pub fn word_frequencies(text: &str) -> HashMap<String, usize> {
    todo!()
}

/// The first value that has already been seen while scanning left to right. O(n) expected.
pub fn first_duplicate(xs: &[i32]) -> Option<i32> {
    todo!()
}

/// Remove duplicates keeping first-occurrence order. O(n) expected time, O(n) space.
pub fn dedup_preserve_order(xs: &[i32]) -> Vec<i32> {
    todo!()
}

/// Maximum of every window of width `k`, via a monotonic `VecDeque` of indices.
/// Amortised O(n): each index is pushed once and popped at most once.
pub fn sliding_max(xs: &[i32], k: usize) -> Vec<i32> {
    todo!()
}

/// The `k` largest values, descending. Uses a size-`k` min-heap: O(n log k) time, O(k) space.
pub fn k_largest(xs: &[i32], k: usize) -> Vec<i32> {
    todo!()
}

/// The `k` smallest values, ascending, using `BinaryHeap`'s native max-heap order.
pub fn k_smallest(xs: &[i32], k: usize) -> Vec<i32> {
    todo!()
}

/// Sorted, de-duplicated. `BTreeSet` gives the ordering for free: O(n log n).
pub fn sorted_unique(xs: &[i32]) -> Vec<i32> {
    todo!()
}

/// Sum of the values whose keys lie in the half-open range `[lo, hi)`.
/// O(log n + m) for m hits — impossible on a `HashMap`.
pub fn range_sum(map: &BTreeMap<i32, i32>, lo: i32, hi: i32) -> i32 {
    todo!()
}

/// Rotate a deque left by `k`, one O(1) pop/push per step.
pub fn rotate_left(dq: &mut VecDeque<i32>, k: usize) {
    todo!()
}

/// Group words by first character, sorted by that character.
pub fn group_by_first_char(words: &[&str]) -> BTreeMap<char, Vec<String>> {
    todo!()
}

/// Byte offsets at which a `char` starts. `s.is_char_boundary(i)` is true exactly here.
pub fn char_boundaries(s: &str) -> Vec<usize> {
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn strings_are_bytes_not_chars() {
        assert_eq!(byte_len_vs_char_len("abc"), (3, 3));
        assert_eq!(byte_len_vs_char_len("héllo"), (6, 5));
        assert_eq!(byte_len_vs_char_len("日本語"), (9, 3));
        assert_eq!(char_count("naïve"), 5);
        assert_eq!(nth_char("日本語", 1), Some('本'));
        assert_eq!(nth_char("ab", 5), None);
        assert_eq!(reverse_chars("héllo"), "olléh");
        assert_eq!(char_boundaries("aé日"), vec![0, 1, 3]);
    }

    #[test]
    fn maps_and_sets() {
        let f = word_frequencies("the cat The hat the");
        assert_eq!(f.get("the"), Some(&3));
        assert_eq!(f.get("cat"), Some(&1));
        assert_eq!(f.get("dog"), None);
        assert_eq!(first_duplicate(&[3, 1, 4, 1, 5]), Some(1));
        assert_eq!(first_duplicate(&[3, 1, 4]), None);
        assert_eq!(dedup_preserve_order(&[3, 1, 3, 2, 1]), vec![3, 1, 2]);
    }

    #[test]
    fn deque() {
        assert_eq!(sliding_max(&[1, 3, -1, -3, 5, 3, 6, 7], 3), vec![3, 3, 5, 5, 6, 7]);
        assert_eq!(sliding_max(&[9], 1), vec![9]);
        assert_eq!(sliding_max(&[1, 2], 5), Vec::<i32>::new());
        let mut dq: VecDeque<i32> = (1..=5).collect();
        rotate_left(&mut dq, 2);
        assert_eq!(dq.into_iter().collect::<Vec<_>>(), vec![3, 4, 5, 1, 2]);
    }

    #[test]
    fn heaps() {
        assert_eq!(k_largest(&[5, 1, 9, 3, 7], 3), vec![9, 7, 5]);
        assert_eq!(k_largest(&[5, 1], 0), Vec::<i32>::new());
        assert_eq!(k_smallest(&[5, 1, 9, 3, 7], 2), vec![1, 3]);
    }

    #[test]
    fn btrees() {
        assert_eq!(sorted_unique(&[3, 1, 3, 2]), vec![1, 2, 3]);
        let m: BTreeMap<i32, i32> = (0..10).map(|k| (k, k * k)).collect();
        assert_eq!(range_sum(&m, 2, 5), 4 + 9 + 16);
        assert_eq!(range_sum(&m, 100, 200), 0);
        let g = group_by_first_char(&["ant", "bee", "ape"]);
        assert_eq!(g[&'a'], vec!["ant".to_string(), "ape".to_string()]);
        assert_eq!(g.keys().copied().collect::<Vec<_>>(), vec!['a', 'b']);
    }
}
