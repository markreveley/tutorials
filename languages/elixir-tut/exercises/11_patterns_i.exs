ExUnit.start()

defmodule PatternsI do
  @moduledoc """
  Lesson 11: two pointers, sliding window, prefix sums, hashing, binary search.

  Representation rule for this file: a *list* is a one-way cursor, so a
  "pointer" into a list is a suffix of that list. When an algorithm needs
  random access (binary search, meet-in-the-middle on both ends) the input
  is converted to a tuple first, because `elem/2` is O(1) and `Enum.at/2`
  is O(n).
  """

  @doc """
  Two Sum. Return `{i, j}` with i < j and `nums[i] + nums[j] == target`,
  or `nil`. One pass, hashing seen values to their index.
  Cost: O(n) time, O(n) space (n = length of nums).
  """
  def two_sum(_nums, _target), do: raise("not implemented")

  @doc """
  Valid Palindrome: ignore non-alphanumerics, ignore case.
  Two pointers implemented as two simultaneous list cursors — one over the
  cleaned charlist, one over its reverse — walking ⌊n/2⌋ steps.
  Cost: O(n) time, O(n) space.
  """
  def is_palindrome(_s), do: raise("not implemented")

  @doc """
  Container With Most Water. Converging two pointers over a *tuple*, so each
  step is O(1); over a list the same code would be O(n) per step.
  Invariant: the optimum uses some pair inside `[lo, hi]`.
  Cost: O(n) time after an O(n) conversion, O(n) space.
  """
  def max_area(_heights), do: raise("not implemented")

  @doc """
  Longest Substring Without Repeating Characters. Sliding window carried as
  fold state: the last index of every character plus the window start.
  Cost: O(n) time, O(k) space (k = alphabet size seen).
  """
  def longest_unique_substring(_s), do: raise("not implemented")

  @doc """
  Minimum Size Subarray Sum: shortest contiguous run of positive numbers
  summing to at least `target`; 0 if none. The window is the gap between two
  list cursors — `lo` is a suffix of nums, `hi` is a further suffix.
  Cost: O(n) time (each cursor advances at most n times), O(1) extra space.
  """
  def min_subarray_len(_target, _nums), do: raise("not implemented")

  @doc """
  Binary search over a *sorted tuple*. Returns `{:ok, index}` or `:error`.
  Half-open formulation: the answer, if any, lies in `[lo, hi)`.
  Cost: O(log n) time, O(1) space. Requires a tuple: on a list the O(1)
  index access is lost and the whole method degenerates to O(n).
  """
  def binary_search(_t, _target), do: raise("not implemented")

  @doc """
  Running Sum: inclusive prefix sums, `p[i] = xs[0] + … + xs[i]`.
  `Enum.scan/2` is a fold that keeps every intermediate accumulator.
  Cost: O(n) time, O(n) space.
  """
  def prefix_sums(_xs), do: raise("not implemented")
end

defmodule PatternsITest do
  use ExUnit.Case

  test "two_sum" do
    assert PatternsI.two_sum([2, 7, 11, 15], 9) == {0, 1}
    assert PatternsI.two_sum([3, 2, 4], 6) == {1, 2}
    assert PatternsI.two_sum([3, 3], 6) == {0, 1}
    assert PatternsI.two_sum([1, 2, 3], 100) == nil
    assert PatternsI.two_sum([], 0) == nil
  end

  test "is_palindrome" do
    assert PatternsI.is_palindrome("A man, a plan, a canal: Panama")
    assert PatternsI.is_palindrome("")
    assert PatternsI.is_palindrome(".,")
    assert PatternsI.is_palindrome("aba")
    refute PatternsI.is_palindrome("race a car")
    refute PatternsI.is_palindrome("ab")
  end

  test "max_area" do
    assert PatternsI.max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert PatternsI.max_area([1, 1]) == 1
    assert PatternsI.max_area([4]) == 0
    assert PatternsI.max_area([]) == 0
  end

  test "longest_unique_substring" do
    assert PatternsI.longest_unique_substring("abcabcbb") == 3
    assert PatternsI.longest_unique_substring("bbbbb") == 1
    assert PatternsI.longest_unique_substring("pwwkew") == 3
    assert PatternsI.longest_unique_substring("") == 0
    assert PatternsI.longest_unique_substring("dvdf") == 3
  end

  test "min_subarray_len" do
    assert PatternsI.min_subarray_len(7, [2, 3, 1, 2, 4, 3]) == 2
    assert PatternsI.min_subarray_len(4, [1, 4, 4]) == 1
    assert PatternsI.min_subarray_len(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0
    assert PatternsI.min_subarray_len(15, [1, 2, 3, 4, 5]) == 5
    assert PatternsI.min_subarray_len(1, []) == 0
  end

  test "binary_search" do
    t = {-1, 0, 3, 5, 9, 12}
    assert PatternsI.binary_search(t, 9) == {:ok, 4}
    assert PatternsI.binary_search(t, -1) == {:ok, 0}
    assert PatternsI.binary_search(t, 12) == {:ok, 5}
    assert PatternsI.binary_search(t, 2) == :error
    assert PatternsI.binary_search({}, 1) == :error

    # every element of a sorted tuple is found at its own index
    big = 0..200 |> Enum.map(&(&1 * 3)) |> List.to_tuple()

    for i <- 0..200 do
      assert PatternsI.binary_search(big, i * 3) == {:ok, i}
      assert PatternsI.binary_search(big, i * 3 + 1) == :error
    end
  end

  test "prefix_sums" do
    assert PatternsI.prefix_sums([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert PatternsI.prefix_sums([1, 1, 1, 1, 1]) == [1, 2, 3, 4, 5]
    assert PatternsI.prefix_sums([3, 1, 2, 10, 1]) == [3, 4, 6, 16, 17]
    assert PatternsI.prefix_sums([]) == []
  end
end
