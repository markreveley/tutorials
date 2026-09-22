"""Lesson 06 — Dicts, sets, and hashing.

Run: python3 -m pytest exercises/06_dicts_sets.py
"""


def is_hashable(x):
    """Return True iff x can be used as a dict key or set element.

    Decide by the protocol (does hash(x) succeed?), not by a list of types:
    a tuple is hashable only when all of its items are.
    """
    try:
        hash(x)
    except TypeError:
        return False
    return True


def two_sum(nums, target):
    """Return (i, j) with i < j and nums[i] + nums[j] == target, else None.

    Precondition: nums is a list of ints.
    Postcondition: the pair whose SECOND index is smallest is returned.
    Cost: O(n) expected — one pass, one dict. Invariant: before index i,
    `seen` maps each value in nums[0..i) to an index where it occurs.
    """
    seen = {}
    for i, x in enumerate(nums):
        want = target - x
        if want in seen:
            return (seen[want], i)
        if x not in seen:
            seen[x] = i
    return None


def char_count(s):
    """Return {character: occurrences} for the characters present in s.

    Precondition: s is a str of any characters (not just a..z).
    Postcondition: no zero entries; sum(result.values()) == len(s).
    Do it with a plain dict — no Counter.
    """
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


def first_unique_char(s):
    """Return the index of the first character occurring exactly once, or -1.

    Postcondition: O(n) time — count in one pass, then scan in index order.
    """
    counts = char_count(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


def group_anagrams(words):
    """Group words that are anagrams of one another.

    Precondition: words is a list of str.
    Postcondition: a list of groups; groups appear in order of first
    occurrence and each group keeps input order. Keys must be hashable, so
    canonicalise a word as a str or tuple, never a list.
    """
    groups = {}
    for word in words:
        key = "".join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())


def top_k_frequent(nums, k):
    """Return the k most frequent values in nums.

    Precondition: 0 <= k <= number of distinct values in nums.
    Postcondition: sorted by descending count; ties broken by ascending
    value, so the result is deterministic.
    """
    counts = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    ordered = sorted(counts, key=lambda v: (-counts[v], v))
    return ordered[:k]


def has_close_duplicate(nums, k):
    """Return True iff some value repeats within a window of width k.

    Precondition: k >= 0.
    Postcondition: True iff there exist i < j with nums[i] == nums[j] and
    j - i <= k. Cost: O(n) expected, O(min(n, k)) space — keep a set holding
    exactly the last k values, which is the loop invariant.
    """
    if k <= 0:
        return False
    window = set()
    for i, x in enumerate(nums):
        if i > k:
            window.discard(nums[i - k - 1])
        if x in window:
            return True
        window.add(x)
    return False


def jaccard(a, b):
    """Return |A ∩ B| / |A ∪ B| for the sets of elements of a and b.

    Precondition: a and b are iterables of hashable items.
    Postcondition: a float in [0.0, 1.0]; 1.0 when both are empty (two
    empty sets are identical), 0.0 when they are disjoint and not both empty.
    """
    sa, sb = set(a), set(b)
    union = sa | sb
    if not union:
        return 1.0
    return len(sa & sb) / len(union)


# ---------------------------------------------------------------- tests

def test_is_hashable():
    assert is_hashable(1)
    assert is_hashable("a")
    assert is_hashable((1, 2))
    assert is_hashable(frozenset([1]))
    assert is_hashable(None)
    assert not is_hashable([1])
    assert not is_hashable({1: 2})
    assert not is_hashable({1, 2})
    assert not is_hashable((1, [2]))       # tuple of a mutable is not hashable


def test_two_sum():
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([3, 2, 4], 6) == (1, 2)
    assert two_sum([3, 3], 6) == (0, 1)
    assert two_sum([0, 0], 0) == (0, 1)
    assert two_sum([1, 2, 3], 100) is None
    assert two_sum([], 0) is None


def test_char_count():
    assert char_count("mississippi") == {"m": 1, "i": 4, "s": 4, "p": 2}
    assert char_count("") == {}
    assert char_count("aA") == {"a": 1, "A": 1}
    assert sum(char_count("hello world").values()) == 11


def test_first_unique_char():
    assert first_unique_char("leetcode") == 0
    assert first_unique_char("loveleetcode") == 2
    assert first_unique_char("aabb") == -1
    assert first_unique_char("") == -1


def test_group_anagrams():
    got = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert got == [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    assert group_anagrams([]) == []
    assert group_anagrams([""]) == [[""]]


def test_top_k_frequent():
    assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
    assert top_k_frequent([1], 1) == [1]
    assert top_k_frequent([3, 1, 2], 3) == [1, 2, 3]      # tie: ascending
    assert top_k_frequent([1, 2], 0) == []


def test_has_close_duplicate():
    assert has_close_duplicate([1, 2, 3, 1], 3)
    assert has_close_duplicate([1, 0, 1, 1], 1)
    assert not has_close_duplicate([1, 2, 3, 1, 2, 3], 2)
    assert not has_close_duplicate([1, 2, 3, 1], 0)
    assert not has_close_duplicate([], 5)
    assert has_close_duplicate([1, 1], 100)


def test_jaccard():
    assert jaccard([1, 2, 3], [2, 3, 4]) == 0.5
    assert jaccard([], []) == 1.0
    assert jaccard([1], []) == 0.0
    assert jaccard([1, 1, 2], [2, 1]) == 1.0              # sets, not multisets
    assert jaccard("abc", "b") == 1 / 3
