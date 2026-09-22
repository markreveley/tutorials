ExUnit.start()

defmodule Lists do
  @moduledoc """
  Lesson 04: lists as an inductive type, recursion, structural induction.
  Write every function with two clauses: one for [], one for [h | t].
  Do not use Enum or the List module.
  """

  @doc "Number of elements. (Named len/1 so it does not clash with Kernel.length/1.)"
  def len(_xs), do: raise("not implemented")

  @doc "Sum of a list of numbers; the empty list sums to 0."
  def sum(_xs), do: raise("not implemented")

  @doc "Append ys to xs, by recursion on xs. This is your own ++."
  def append(_xs, _ys), do: raise("not implemented")

  @doc "Reverse a list, using append/2. Naive and O(n^2) — that is fine here."
  def reverse(_xs), do: raise("not implemented")

  @doc "True when x occurs in xs."
  def member?(_xs, _x), do: raise("not implemented")

  @doc "Return {:ok, last_element} or :error for the empty list."
  def last(_xs), do: raise("not implemented")

  @doc "The first n elements of xs (all of xs when n >= len(xs), [] when n <= 0)."
  def take(_xs, _n), do: raise("not implemented")
end

defmodule ListsTest do
  use ExUnit.Case

  test "len" do
    assert Lists.len([]) == 0
    assert Lists.len([:a]) == 1
    assert Lists.len([1, 2, 3, 4]) == 4
  end

  test "sum" do
    assert Lists.sum([]) == 0
    assert Lists.sum([1, 2, 3]) == 6
    assert Lists.sum([-1, 1]) == 0
  end

  test "append" do
    assert Lists.append([], []) == []
    assert Lists.append([], [1, 2]) == [1, 2]
    assert Lists.append([1, 2], []) == [1, 2]
    assert Lists.append([1, 2], [3, 4]) == [1, 2, 3, 4]
  end

  test "append is associative and [] is its identity" do
    xs = [1, 2]
    ys = [3]
    zs = [4, 5]
    assert Lists.append(Lists.append(xs, ys), zs) == Lists.append(xs, Lists.append(ys, zs))
    assert Lists.append([], xs) == xs
    assert Lists.append(xs, []) == xs
  end

  test "len distributes over append" do
    xs = [1, 2, 3]
    ys = [4, 5]
    assert Lists.len(Lists.append(xs, ys)) == Lists.len(xs) + Lists.len(ys)
  end

  test "reverse" do
    assert Lists.reverse([]) == []
    assert Lists.reverse([1]) == [1]
    assert Lists.reverse([1, 2, 3]) == [3, 2, 1]
  end

  test "reverse is an involution" do
    for xs <- [[], [1], [1, 2], [1, 2, 3, 4, 5]] do
      assert Lists.reverse(Lists.reverse(xs)) == xs
    end
  end

  test "reverse of an append" do
    xs = [1, 2]
    ys = [3, 4]

    assert Lists.reverse(Lists.append(xs, ys)) ==
             Lists.append(Lists.reverse(ys), Lists.reverse(xs))
  end

  test "member?" do
    refute Lists.member?([], :a)
    assert Lists.member?([1, 2, 3], 2)
    refute Lists.member?([1, 2, 3], 9)
    assert Lists.member?([:a, :b], :b)
  end

  test "last" do
    assert Lists.last([]) == :error
    assert Lists.last([1]) == {:ok, 1}
    assert Lists.last([1, 2, 3]) == {:ok, 3}
  end

  test "take" do
    assert Lists.take([1, 2, 3], 0) == []
    assert Lists.take([1, 2, 3], 2) == [1, 2]
    assert Lists.take([1, 2, 3], 9) == [1, 2, 3]
    assert Lists.take([], 3) == []
    assert Lists.take([1, 2, 3], -1) == []
  end
end
