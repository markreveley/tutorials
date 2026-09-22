"""Lesson 12 — Dynamic programming, heaps, graphs.

Run: python3 -m pytest exercises/12_patterns_dp.py
"""

import heapq
from bisect import bisect_left
from collections import Counter, deque


def climb_stairs(n):
    """Return the number of ways to climb n stairs taking 1 or 2 steps at a time.

    Precondition: n is an int with n >= 0.
    Postcondition: result == f(n) where f(0) = f(1) = 1 and
    f(k) = f(k-1) + f(k-2), because the first move is 1 or 2 and the two
    cases are disjoint and exhaustive.
    O(n) time, O(1) space.
    """
    prev, cur = 1, 1                    # f(0), f(1)
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
    return cur if n >= 1 else 1


def coin_change(coins, amount):
    """Return the fewest coins summing to `amount`, or -1 if impossible.

    Precondition: coins is a list of positive ints, amount is an int >= 0;
    each coin may be used any number of times.
    Postcondition: result is min |S| over multisets S of coins with sum
    amount, or -1 when no such S exists.
    Recurrence: best(0) = 0, best(a) = 1 + min over c <= a of best(a - c).
    O(amount * len(coins)) time, O(amount) space.
    """
    INF = float("inf")
    best = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return -1 if best[amount] == INF else best[amount]


def length_of_lis(nums):
    """Return the length of the longest strictly increasing subsequence.

    Precondition: nums is a list of mutually comparable values.
    Postcondition: result is max k such that some i_1 < ... < i_k has
    nums[i_1] < ... < nums[i_k]; 0 for the empty list.
    Patience method: tails[j] is the smallest possible last element of an
    increasing subsequence of length j+1, and tails stays sorted.
    O(n log n) time, O(n) space.
    """
    tails = []
    for x in nums:
        j = bisect_left(tails, x)       # first tail >= x
        if j == len(tails):
            tails.append(x)
        else:
            tails[j] = x
    return len(tails)


def edit_distance(word1, word2):
    """Return the minimum insert/delete/replace edits turning word1 into word2.

    Precondition: word1 and word2 are strings.
    Postcondition: result is the Levenshtein distance; it is 0 iff the
    strings are equal, and is symmetric.
    Recurrence on prefixes: d(i, 0) = i, d(0, j) = j, and for i, j > 0,
    d(i, j) = d(i-1, j-1) if the last characters match, else
    1 + min(d(i-1, j), d(i, j-1), d(i-1, j-1)).
    O(m * n) time, O(min(m, n)) space using one rolling row.
    """
    if len(word1) < len(word2):         # keep the row short
        word1, word2 = word2, word1
    n = len(word2)
    row = list(range(n + 1))            # d(0, j) = j
    for i, a in enumerate(word1, start=1):
        prev_diag = row[0]              # d(i-1, 0)
        row[0] = i                      # d(i, 0) = i
        for j, b in enumerate(word2, start=1):
            up_left = prev_diag
            prev_diag = row[j]          # d(i-1, j), before overwriting
            if a == b:
                row[j] = up_left
            else:
                row[j] = 1 + min(row[j], row[j - 1], up_left)
    return row[n]


def k_largest(nums, k):
    """Return the k largest values of nums in descending order.

    Precondition: nums is a list of comparable values, 0 <= k <= len(nums).
    Postcondition: result is sorted descending and is a sub-multiset of nums
    such that every excluded element is <= min(result).
    O(n log k) time, O(k) space: keep a min-heap of the best k seen so far.
    """
    if k == 0:
        return []
    heap = nums[:k]
    heapq.heapify(heap)                 # heap[0] is the smallest kept
    for x in nums[k:]:
        if x > heap[0]:
            heapq.heapreplace(heap, x)
    return sorted(heap, reverse=True)


def top_k_frequent(nums, k):
    """Return the k most frequent elements of nums.

    Precondition: nums is a list of hashable values; 1 <= k <= number of
    distinct values in nums.
    Postcondition: the result has k distinct elements, and every element not
    returned has count <= the smallest returned count. Ties broken
    arbitrarily; output order is unspecified.
    O(n log k) time, O(n) space.
    """
    counts = Counter(nums)
    return [v for v, _ in heapq.nlargest(k, counts.items(), key=lambda p: p[1])]


def num_islands(grid):
    """Count connected groups of '1' cells in a grid, moving 4-directionally.

    Precondition: grid is a list of equal-length lists (or strings) of the
    characters '1' (land) and '0' (water).
    Postcondition: result is the number of connected components of the graph
    whose vertices are the '1' cells and whose edges join orthogonal
    neighbours. `grid` is not modified.
    O(rows * cols) time and space.
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = set()
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or (r, c) in seen:
                continue
            count += 1
            stack = [(r, c)]            # iterative DFS: no recursion limit
            seen.add((r, c))
            while stack:
                i, j = stack.pop()
                for ni, nj in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if (0 <= ni < rows and 0 <= nj < cols
                            and grid[ni][nj] == "1" and (ni, nj) not in seen):
                        seen.add((ni, nj))
                        stack.append((ni, nj))
    return count


def can_finish(num_courses, prerequisites):
    """Return True iff all courses can be taken respecting the prerequisites.

    Precondition: num_courses >= 0; prerequisites is a list of pairs [a, b]
    meaning b must be taken before a. Labels are ints in [0, num_courses).
    Postcondition: True iff the directed graph b -> a is acyclic, i.e. a
    topological order exists.
    Kahn's algorithm: repeatedly remove a vertex of in-degree 0.
    O(V + E) time and space.
    """
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    queue = deque(v for v in range(num_courses) if indeg[v] == 0)
    placed = 0
    while queue:
        v = queue.popleft()
        placed += 1
        for w in adj[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                queue.append(w)
    return placed == num_courses


# ---------------------------------------------------------------- tests

def test_climb_stairs():
    assert climb_stairs(0) == 1
    assert climb_stairs(1) == 1
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(5) == 8
    assert climb_stairs(45) == 1836311903


def test_coin_change():
    assert coin_change([1, 2, 5], 11) == 3          # 5 + 5 + 1
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
    assert coin_change([], 0) == 0
    assert coin_change([], 7) == -1
    assert coin_change([186, 419, 83, 408], 6249) == 20


def test_length_of_lis():
    assert length_of_lis([]) == 0
    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
    assert length_of_lis([7, 7, 7, 7]) == 1         # strictly increasing
    assert length_of_lis([1, 2, 3, 4, 5]) == 5


def test_edit_distance():
    assert edit_distance("", "") == 0
    assert edit_distance("abc", "abc") == 0
    assert edit_distance("", "abc") == 3
    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5
    assert edit_distance("ros", "horse") == 3       # symmetric


def test_k_largest():
    assert k_largest([3, 2, 1, 5, 6, 4], 2) == [6, 5]
    assert k_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == [6, 5, 5, 4]
    assert k_largest([1], 1) == [1]
    assert k_largest([9, 8], 0) == []


def test_top_k_frequent():
    assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert top_k_frequent([1], 1) == [1]
    assert sorted(top_k_frequent(["a", "a", "b", "b", "c"], 2)) == ["a", "b"]
    assert sorted(top_k_frequent([4, 4, 4, 3, 3, 2, 2, 1], 3)) == [2, 3, 4]


def test_num_islands():
    grid = [
        list("11110"),
        list("11010"),
        list("11000"),
        list("00000"),
    ]
    assert num_islands(grid) == 1
    assert grid[0][0] == "1"                        # input untouched
    assert num_islands([
        list("11000"),
        list("11000"),
        list("00100"),
        list("00011"),
    ]) == 3
    assert num_islands([]) == 0
    assert num_islands([list("000")]) == 0
    assert num_islands([list("1")]) == 1


def test_can_finish():
    assert can_finish(2, [[1, 0]]) is True
    assert can_finish(2, [[1, 0], [0, 1]]) is False
    assert can_finish(0, []) is True
    assert can_finish(4, [[1, 0], [2, 1], [3, 2]]) is True
    assert can_finish(3, [[0, 1], [1, 2], [2, 0]]) is False
    assert can_finish(5, []) is True
