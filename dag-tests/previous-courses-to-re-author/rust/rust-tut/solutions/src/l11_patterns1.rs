//! Lesson 11 — LeetCode patterns I: two pointers, sliding windows, prefix sums,
//! hashing, and binary search. Every function states an invariant and a cost.

use std::collections::HashMap;

/// LC 1. Indices `(i, j)`, `i < j`, with `nums[i] + nums[j] == target`.
/// Invariant: `seen` maps every value in `nums[0..j]` to one of its indices.
/// O(n) expected time, O(n) space.
pub fn two_sum(nums: &[i32], target: i32) -> Option<(usize, usize)> {
    let mut seen: HashMap<i32, usize> = HashMap::new();
    for (j, &x) in nums.iter().enumerate() {
        if let Some(&i) = seen.get(&(target - x)) {
            return Some((i, j));
        }
        seen.entry(x).or_insert(j);
    }
    None
}

/// LC 125. Palindrome ignoring case and non-alphanumeric characters.
/// Invariant: `cs[0..lo)` and `cs(hi..]` have already been matched pairwise.
/// O(n) time, O(n) space for the scalar vector.
pub fn is_palindrome(s: &str) -> bool {
    let cs: Vec<char> = s
        .chars()
        .filter(|c| c.is_alphanumeric())
        .map(|c| c.to_ascii_lowercase())
        .collect();
    if cs.is_empty() {
        return true;
    }
    let (mut lo, mut hi) = (0usize, cs.len() - 1);
    while lo < hi {
        if cs[lo] != cs[hi] {
            return false;
        }
        lo += 1;
        hi -= 1;
    }
    true
}

/// LC 11. Container With Most Water. Opposite-end two pointers.
/// Invariant: the optimum uses some pair inside `[lo, hi]`. Moving the shorter
/// wall discards only pairs whose area cannot beat the current best. O(n).
pub fn max_area(height: &[i32]) -> i32 {
    if height.len() < 2 {
        return 0;
    }
    let (mut lo, mut hi) = (0usize, height.len() - 1);
    let mut best = 0;
    while lo < hi {
        let h = height[lo].min(height[hi]);
        best = best.max(h * (hi - lo) as i32);
        if height[lo] <= height[hi] {
            lo += 1;
        } else {
            hi -= 1;
        }
    }
    best
}

/// LC 3. Longest substring with all-distinct characters, measured in `char`s.
/// Invariant: `cs[lo..hi]` contains no repeat; `last[c]` is c's newest index.
/// Amortised O(n): `lo` only ever increases.
pub fn longest_substring_without_repeat(s: &str) -> usize {
    let cs: Vec<char> = s.chars().collect();
    let mut last: HashMap<char, usize> = HashMap::new();
    let mut lo = 0usize;
    let mut best = 0usize;
    for hi in 0..cs.len() {
        if let Some(&prev) = last.get(&cs[hi]) {
            if prev >= lo {
                lo = prev + 1;
            }
        }
        last.insert(cs[hi], hi);
        best = best.max(hi - lo + 1);
    }
    best
}

/// LC 209. Shortest subarray with sum ≥ `target`; 0 if none. Requires non-negative values.
/// Invariant: `sum == Σ nums[lo..hi]` and no window ending before `hi` and starting
/// before `lo` is feasible. Each index enters and leaves once ⇒ O(n).
pub fn min_subarray_len(target: i32, nums: &[i32]) -> usize {
    let mut lo = 0usize;
    let mut sum: i64 = 0;
    let mut best = usize::MAX;
    for hi in 0..nums.len() {
        sum += nums[hi] as i64;
        while sum >= target as i64 {
            best = best.min(hi - lo + 1);
            sum -= nums[lo] as i64;
            lo += 1;
        }
    }
    if best == usize::MAX { 0 } else { best }
}

/// Maximum sum over every fixed window of width `k`; `None` if `k` is 0 or too large.
/// Invariant: `sum` equals the sum of the k values ending at `i`. O(n).
pub fn max_sum_subarray_k(nums: &[i32], k: usize) -> Option<i64> {
    if k == 0 || nums.len() < k {
        return None;
    }
    let mut sum: i64 = nums[..k].iter().map(|&x| x as i64).sum();
    let mut best = sum;
    for i in k..nums.len() {
        sum += nums[i] as i64 - nums[i - k] as i64;
        best = best.max(sum);
    }
    Some(best)
}

/// `p[i] = Σ xs[0..i]`, length n+1. Then `Σ xs[l..r] == p[r] - p[l]` for all `l ≤ r`.
pub fn prefix_sums(xs: &[i32]) -> Vec<i64> {
    let mut p = Vec::with_capacity(xs.len() + 1);
    p.push(0i64);
    for &x in xs {
        p.push(p[p.len() - 1] + x as i64);
    }
    p
}

/// Sum over the half-open range `[l, r)` in O(1) after O(n) preprocessing.
pub fn range_sum(prefix: &[i64], l: usize, r: usize) -> i64 {
    prefix[r] - prefix[l]
}

/// LC 560. Count subarrays summing to `k`.
/// From `p[r] - p[l] == k` ⇔ `p[l] == p[r] - k`: hash the prefix sums seen so far.
/// O(n) expected.
pub fn subarray_sum_equals_k(nums: &[i32], k: i32) -> i32 {
    let mut counts: HashMap<i64, i32> = HashMap::new();
    counts.insert(0, 1);
    let mut running: i64 = 0;
    let mut total = 0;
    for &x in nums {
        running += x as i64;
        if let Some(&c) = counts.get(&(running - k as i64)) {
            total += c;
        }
        *counts.entry(running).or_insert(0) += 1;
    }
    total
}

/// LC 238. `out[i] = Π_{j ≠ i} nums[j]`, no division, O(n) time, O(1) extra space.
pub fn product_except_self(nums: &[i32]) -> Vec<i32> {
    let n = nums.len();
    let mut out = vec![1i32; n];
    let mut left = 1i32;
    for i in 0..n {
        out[i] = left;
        left *= nums[i];
    }
    let mut right = 1i32;
    for i in (0..n).rev() {
        out[i] *= right;
        right *= nums[i];
    }
    out
}

/// First index `i` in the sorted slice with `xs[i] >= target` (n if none).
/// Half-open invariant: the answer lies in `[lo, hi)` ∪ {hi}; `hi - lo` strictly
/// shrinks each round ⇒ termination in ⌈log₂(n+1)⌉ steps.
pub fn binary_search_lower_bound(xs: &[i32], target: i32) -> usize {
    let (mut lo, mut hi) = (0usize, xs.len());
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if xs[mid] < target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo
}

/// First index `i` with `xs[i] > target` (n if none). `upper - lower` is the multiplicity.
pub fn binary_search_upper_bound(xs: &[i32], target: i32) -> usize {
    let (mut lo, mut hi) = (0usize, xs.len());
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if xs[mid] <= target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo
}

/// LC 287. The repeated value in `nums`, where values are in `1..=n` and n+1 entries
/// exist. Floyd fast/slow on the functional graph `i -> nums[i]`. O(n) time, O(1) space.
pub fn find_duplicate(nums: &[i32]) -> i32 {
    let (mut slow, mut fast) = (nums[0], nums[nums[0] as usize]);
    while slow != fast {
        slow = nums[slow as usize];
        fast = nums[nums[fast as usize] as usize];
    }
    let mut a = 0i32;
    while a != slow {
        a = nums[a as usize];
        slow = nums[slow as usize];
    }
    a
}

/// LC 283. Move zeroes to the back, keeping the order of the rest.
/// Invariant: `nums[0..w]` holds every non-zero seen so far, in order. O(n).
pub fn move_zeroes(nums: &mut [i32]) {
    let mut w = 0usize;
    for r in 0..nums.len() {
        if nums[r] != 0 {
            nums.swap(w, r);
            w += 1;
        }
    }
}

/// LC 49. Group anagrams; groups and their contents are sorted so the result is canonical.
/// O(Σ mᵢ log mᵢ) with a sorted-letters key.
pub fn group_anagrams(strs: &[&str]) -> Vec<Vec<String>> {
    let mut groups: HashMap<Vec<char>, Vec<String>> = HashMap::new();
    for s in strs {
        let mut key: Vec<char> = s.chars().collect();
        key.sort_unstable();
        groups.entry(key).or_default().push((*s).to_string());
    }
    let mut out: Vec<Vec<String>> = groups
        .into_values()
        .map(|mut g| {
            g.sort();
            g
        })
        .collect();
    out.sort();
    out
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
