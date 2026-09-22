//! Lesson 11 — LeetCode patterns I: two pointers, sliding windows, prefix sums,
//! hashing, and binary search. Every function states an invariant and a cost.

use std::collections::HashMap;

/// LC 1. Indices `(i, j)`, `i < j`, with `nums[i] + nums[j] == target`.
/// Invariant: `seen` maps every value in `nums[0..j]` to one of its indices.
/// O(n) expected time, O(n) space.
pub fn two_sum(nums: &[i32], target: i32) -> Option<(usize, usize)> {
    todo!()
}

/// LC 125. Palindrome ignoring case and non-alphanumeric characters.
/// Invariant: `cs[0..lo)` and `cs(hi..]` have already been matched pairwise.
/// O(n) time, O(n) space for the scalar vector.
pub fn is_palindrome(s: &str) -> bool {
    todo!()
}

/// LC 11. Container With Most Water. Opposite-end two pointers.
/// Invariant: the optimum uses some pair inside `[lo, hi]`. Moving the shorter
/// wall discards only pairs whose area cannot beat the current best. O(n).
pub fn max_area(height: &[i32]) -> i32 {
    todo!()
}

/// LC 3. Longest substring with all-distinct characters, measured in `char`s.
/// Invariant: `cs[lo..hi]` contains no repeat; `last[c]` is c's newest index.
/// Amortised O(n): `lo` only ever increases.
pub fn longest_substring_without_repeat(s: &str) -> usize {
    todo!()
}

/// LC 209. Shortest subarray with sum ≥ `target`; 0 if none. Requires non-negative values.
/// Invariant: `sum == Σ nums[lo..hi]` and no window ending before `hi` and starting
/// before `lo` is feasible. Each index enters and leaves once ⇒ O(n).
pub fn min_subarray_len(target: i32, nums: &[i32]) -> usize {
    todo!()
}

/// Maximum sum over every fixed window of width `k`; `None` if `k` is 0 or too large.
/// Invariant: `sum` equals the sum of the k values ending at `i`. O(n).
pub fn max_sum_subarray_k(nums: &[i32], k: usize) -> Option<i64> {
    todo!()
}

/// `p[i] = Σ xs[0..i]`, length n+1. Then `Σ xs[l..r] == p[r] - p[l]` for all `l ≤ r`.
pub fn prefix_sums(xs: &[i32]) -> Vec<i64> {
    todo!()
}

/// Sum over the half-open range `[l, r)` in O(1) after O(n) preprocessing.
pub fn range_sum(prefix: &[i64], l: usize, r: usize) -> i64 {
    todo!()
}

/// LC 560. Count subarrays summing to `k`.
/// From `p[r] - p[l] == k` ⇔ `p[l] == p[r] - k`: hash the prefix sums seen so far.
/// O(n) expected.
pub fn subarray_sum_equals_k(nums: &[i32], k: i32) -> i32 {
    todo!()
}

/// LC 238. `out[i] = Π_{j ≠ i} nums[j]`, no division, O(n) time, O(1) extra space.
pub fn product_except_self(nums: &[i32]) -> Vec<i32> {
    todo!()
}

/// First index `i` in the sorted slice with `xs[i] >= target` (n if none).
/// Half-open invariant: the answer lies in `[lo, hi)` ∪ {hi}; `hi - lo` strictly
/// shrinks each round ⇒ termination in ⌈log₂(n+1)⌉ steps.
pub fn binary_search_lower_bound(xs: &[i32], target: i32) -> usize {
    todo!()
}

/// First index `i` with `xs[i] > target` (n if none). `upper - lower` is the multiplicity.
pub fn binary_search_upper_bound(xs: &[i32], target: i32) -> usize {
    todo!()
}

/// LC 287. The repeated value in `nums`, where values are in `1..=n` and n+1 entries
/// exist. Floyd fast/slow on the functional graph `i -> nums[i]`. O(n) time, O(1) space.
pub fn find_duplicate(nums: &[i32]) -> i32 {
    todo!()
}

/// LC 283. Move zeroes to the back, keeping the order of the rest.
/// Invariant: `nums[0..w]` holds every non-zero seen so far, in order. O(n).
pub fn move_zeroes(nums: &mut [i32]) {
    todo!()
}

/// LC 49. Group anagrams; groups and their contents are sorted so the result is canonical.
/// O(Σ mᵢ log mᵢ) with a sorted-letters key.
pub fn group_anagrams(strs: &[&str]) -> Vec<Vec<String>> {
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hashing() {
        assert_eq!(two_sum(&[2, 7, 11, 15], 9), Some((0, 1)));
        assert_eq!(two_sum(&[3, 2, 4], 6), Some((1, 2)));
        assert_eq!(two_sum(&[1, 2], 100), None);
        assert_eq!(subarray_sum_equals_k(&[1, 1, 1], 2), 2);
        assert_eq!(subarray_sum_equals_k(&[1, 2, 3], 3), 2);
        assert_eq!(subarray_sum_equals_k(&[], 0), 0);
        assert_eq!(
            group_anagrams(&["eat", "tea", "tan", "ate", "nat", "bat"]),
            vec![
                vec!["ate".to_string(), "eat".to_string(), "tea".to_string()],
                vec!["bat".to_string()],
                vec!["nat".to_string(), "tan".to_string()],
            ]
        );
    }

    #[test]
    fn two_pointers() {
        assert!(is_palindrome("A man, a plan, a canal: Panama"));
        assert!(is_palindrome(""));
        assert!(is_palindrome(".,"));
        assert!(!is_palindrome("race a car"));
        assert_eq!(max_area(&[1, 8, 6, 2, 5, 4, 8, 3, 7]), 49);
        assert_eq!(max_area(&[1, 1]), 1);
        assert_eq!(max_area(&[5]), 0);
        let mut v = vec![0, 1, 0, 3, 12];
        move_zeroes(&mut v);
        assert_eq!(v, vec![1, 3, 12, 0, 0]);
        assert_eq!(find_duplicate(&[1, 3, 4, 2, 2]), 2);
        assert_eq!(find_duplicate(&[3, 1, 3, 4, 2]), 3);
    }

    #[test]
    fn windows() {
        assert_eq!(longest_substring_without_repeat("abcabcbb"), 3);
        assert_eq!(longest_substring_without_repeat("bbbbb"), 1);
        assert_eq!(longest_substring_without_repeat("pwwkew"), 3);
        assert_eq!(longest_substring_without_repeat(""), 0);
        assert_eq!(min_subarray_len(7, &[2, 3, 1, 2, 4, 3]), 2);
        assert_eq!(min_subarray_len(11, &[1, 1, 1, 1]), 0);
        assert_eq!(max_sum_subarray_k(&[1, 12, -5, -6, 50, 3], 4), Some(51));
        assert_eq!(max_sum_subarray_k(&[1, 2], 3), None);
    }

    #[test]
    fn prefixes() {
        let p = prefix_sums(&[2, 4, 6]);
        assert_eq!(p, vec![0, 2, 6, 12]);
        assert_eq!(range_sum(&p, 1, 3), 10);
        assert_eq!(range_sum(&p, 2, 2), 0);
        assert_eq!(product_except_self(&[1, 2, 3, 4]), vec![24, 12, 8, 6]);
        assert_eq!(product_except_self(&[-1, 1, 0, -3, 3]), vec![0, 0, 9, 0, 0]);
    }

    #[test]
    fn binary_search_bounds() {
        let xs = [1, 3, 3, 3, 5, 8];
        assert_eq!(binary_search_lower_bound(&xs, 3), 1);
        assert_eq!(binary_search_upper_bound(&xs, 3), 4);
        assert_eq!(binary_search_upper_bound(&xs, 3) - binary_search_lower_bound(&xs, 3), 3);
        assert_eq!(binary_search_lower_bound(&xs, 0), 0);
        assert_eq!(binary_search_lower_bound(&xs, 9), 6);
        assert_eq!(binary_search_lower_bound(&xs, 4), 4);
        assert_eq!(binary_search_lower_bound(&[], 1), 0);
        // Exhaustive check against a linear scan.
        let ys = [0, 0, 2, 2, 2, 7, 9, 9];
        for t in -1..=10 {
            let lb = ys.iter().position(|&y| y >= t).unwrap_or(ys.len());
            let ub = ys.iter().position(|&y| y > t).unwrap_or(ys.len());
            assert_eq!(binary_search_lower_bound(&ys, t), lb, "lb at {t}");
            assert_eq!(binary_search_upper_bound(&ys, t), ub, "ub at {t}");
        }
    }
}
