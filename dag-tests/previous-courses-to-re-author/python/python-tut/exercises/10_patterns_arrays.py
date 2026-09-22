"""Lesson 10 — LeetCode patterns I: arrays.

Run: python3 -m pytest exercises/10_patterns_arrays.py
"""

import random


def two_sum_sorted(a, target):
    """Return (i, j) with i < j and a[i] + a[j] == target, or None.

    Precondition: a is sorted non-decreasing.
    Postcondition: if a pair exists, some valid pair is returned (0-indexed);
    otherwise None. Θ(n) time, Θ(1) auxiliary space — no dict, no nested loop.
    Invariant: if a solution exists at all, one exists inside a[lo..hi].
    """
    raise NotImplementedError


def container_with_most_water(heights):
    """Return max over i < j of (j - i) * min(heights[i], heights[j]).

    Precondition: heights is a list of non-negative ints; len < 2 gives 0.
    Postcondition: the exact maximum. Θ(n) time, Θ(1) space.
    Invariant: `best` covers every pair already discarded, and every pair not
    yet accounted for lies inside [lo, hi]; the shorter side may be discarded
    because it can never beat its current partner.
    """
    raise NotImplementedError


def longest_substring_without_repeating(s):
    """Return the length of the longest substring of s with no repeated char.

    Precondition: s is a str.
    Postcondition: the exact maximum length (0 for ""). Θ(n) time — each index
    enters and leaves the window at most once.
    Invariant: at the end of step hi, s[lo..hi] has all-distinct characters and
    no valid window ending at hi starts before lo.
    """
    raise NotImplementedError


def min_subarray_len(target, nums):
    """Return the length of the shortest contiguous subarray summing >= target.

    Precondition: nums is a list of positive ints (positivity is what makes the
    window monotone); target > 0.
    Postcondition: the minimal length, or 0 if no such subarray exists. Θ(n)
    time, Θ(1) space.
    Invariant: `s == sum(nums[lo..hi])`, and every window ending at hi that is
    shorter than hi - lo + 1 sums to < target.
    """
    raise NotImplementedError


def product_except_self(nums):
    """Return out where out[i] == product of every nums[j] with j != i.

    Precondition: len(nums) >= 1; the values may include zeros and negatives.
    Postcondition: out has the same length as nums. Θ(n) time and Θ(1)
    auxiliary space (the output does not count). Division is forbidden — use a
    forward prefix pass and a backward suffix pass.
    """
    raise NotImplementedError


def move_zeroes(nums):
    """Move every 0 in nums to the end, keeping the non-zeros in order.

    Precondition: nums is a list of ints.
    Postcondition: mutates nums in place and returns None; the non-zero values
    keep their relative order and all zeros follow them. Θ(n) time, Θ(1) space.
    Invariant: nums[0..w) holds the non-zeros of the original nums[0..i) in
    order, and nums[w..i) is all zeros.
    """
    raise NotImplementedError


def max_subarray(nums):
    """Return the largest sum of a non-empty contiguous subarray (Kadane).

    Precondition: nums is a non-empty list of ints (possibly all negative).
    Postcondition: the exact maximum. Θ(n) time, Θ(1) space.
    Invariant: after processing index i, `cur` is the largest sum of a subarray
    ending exactly at i, and `best` is the largest such value over all t <= i.
    """
    raise NotImplementedError


def subarray_sum_equals_k(nums, k):
    """Return how many contiguous subarrays of nums sum to exactly k.

    Precondition: nums is a list of ints, which MAY be negative or zero — so a
    sliding window is unsound here; use prefix sums.
    Postcondition: the exact count. Θ(n) expected time, Θ(n) space.
    Invariant: sweeping j, `seen[v]` == #{ i <= j : prefix[i] == v }, and
    sum(nums[i..j)) == k  ⇔  prefix[i] == prefix[j] - k.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- tests

def _brute_pair(a, target):
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] + a[j] == target:
                return True
    return False


def _brute_container(h):
    return max(
        (j - i) * min(h[i], h[j])
        for i in range(len(h))
        for j in range(i + 1, len(h))
    ) if len(h) >= 2 else 0


def _brute_longest_distinct(s):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            window = s[i:j + 1]
            if len(set(window)) == len(window):
                best = max(best, len(window))
    return best


def _brute_min_len(target, nums):
    best = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= target:
                length = j - i + 1
                best = length if best == 0 else min(best, length)
                break
    return best


def _brute_count_k(nums, k):
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                count += 1
    return count


def test_two_sum_sorted():
    assert two_sum_sorted([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum_sorted([1, 1, 3], 2) == (0, 1)
    assert two_sum_sorted([-3, 0, 4, 9], 7) is None
    assert two_sum_sorted([], 0) is None
    assert two_sum_sorted([5], 5) is None
    rng = random.Random(0)
    for _ in range(200):
        a = sorted(rng.randrange(-20, 20) for _ in range(rng.randrange(0, 9)))
        t = rng.randrange(-30, 30)
        got = two_sum_sorted(a, t)
        if got is None:
            assert not _brute_pair(a, t), (a, t)
        else:
            i, j = got
            assert i < j and a[i] + a[j] == t, (a, t, got)


def test_container_with_most_water():
    assert container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert container_with_most_water([1, 1]) == 1
    assert container_with_most_water([4]) == 0
    assert container_with_most_water([]) == 0
    rng = random.Random(1)
    for _ in range(200):
        h = [rng.randrange(0, 15) for _ in range(rng.randrange(2, 10))]
        assert container_with_most_water(h) == _brute_container(h), h


def test_longest_substring_without_repeating():
    assert longest_substring_without_repeating("abcabcbb") == 3
    assert longest_substring_without_repeating("bbbbb") == 1
    assert longest_substring_without_repeating("pwwkew") == 3
    assert longest_substring_without_repeating("") == 0
    assert longest_substring_without_repeating("dvdf") == 3
    rng = random.Random(2)
    for _ in range(200):
        s = "".join(rng.choice("abcd") for _ in range(rng.randrange(0, 12)))
        assert longest_substring_without_repeating(s) == _brute_longest_distinct(s), s


def test_min_subarray_len():
    assert min_subarray_len(7, [2, 3, 1, 2, 4, 3]) == 2
    assert min_subarray_len(4, [1, 4, 4]) == 1
    assert min_subarray_len(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0
    assert min_subarray_len(5, []) == 0
    rng = random.Random(3)
    for _ in range(200):
        nums = [rng.randrange(1, 10) for _ in range(rng.randrange(0, 12))]
        t = rng.randrange(1, 30)
        assert min_subarray_len(t, nums) == _brute_min_len(t, nums), (t, nums)


def test_product_except_self():
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert product_except_self([0, 0]) == [0, 0]
    assert product_except_self([7]) == [1]
    rng = random.Random(4)
    for _ in range(200):
        nums = [rng.randrange(-4, 5) for _ in range(rng.randrange(1, 8))]
        expect = []
        for i in range(len(nums)):
            p = 1
            for j, v in enumerate(nums):
                if j != i:
                    p *= v
            expect.append(p)
        assert product_except_self(nums) == expect, nums


def test_move_zeroes():
    nums = [0, 1, 0, 3, 12]
    assert move_zeroes(nums) is None          # mutates, returns nothing
    assert nums == [1, 3, 12, 0, 0]
    nums = [0]
    move_zeroes(nums)
    assert nums == [0]
    nums = [1, 2, 3]
    move_zeroes(nums)
    assert nums == [1, 2, 3]
    rng = random.Random(5)
    for _ in range(200):
        nums = [rng.choice([0, 0, 1, 2, 3]) for _ in range(rng.randrange(0, 12))]
        expect = [v for v in nums if v != 0] + [0] * nums.count(0)
        move_zeroes(nums)
        assert nums == expect


def test_max_subarray():
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray([1]) == 1
    assert max_subarray([-3, -1, -2]) == -1
    assert max_subarray([5, 4, -1, 7, 8]) == 23
    rng = random.Random(6)
    for _ in range(200):
        nums = [rng.randrange(-9, 10) for _ in range(rng.randrange(1, 12))]
        expect = max(
            sum(nums[i:j])
            for i in range(len(nums))
            for j in range(i + 1, len(nums) + 1)
        )
        assert max_subarray(nums) == expect, nums


def test_subarray_sum_equals_k():
    assert subarray_sum_equals_k([1, 1, 1], 2) == 2
    assert subarray_sum_equals_k([1, 2, 3], 3) == 2
    assert subarray_sum_equals_k([1, -1, 0], 0) == 3
    assert subarray_sum_equals_k([], 0) == 0
    rng = random.Random(7)
    for _ in range(200):
        nums = [rng.randrange(-4, 5) for _ in range(rng.randrange(0, 12))]
        k = rng.randrange(-6, 7)
        assert subarray_sum_equals_k(nums, k) == _brute_count_k(nums, k), (nums, k)
