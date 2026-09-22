ExUnit.start()

defmodule Folds do
  @moduledoc """
  Lesson 06: Enum, Stream, higher-order functions, folds.

  Rule for this file: reduce is the only list primitive you may assume.
  Do not call Enum.map/2, Enum.filter/2 or Enum.sum/1 — build them.
  """

  @doc "Sum of a list, via Enum.reduce/3."
  def sum(xs), do: Enum.reduce(xs, 0, &+/2)

  @doc "map, built from Enum.reduce/3 (plus one Enum.reverse/1)."
  # map(f, ·) is the fold fn h, acc -> [f.(h) | acc] end over []; done as a
  # left fold it builds the result backwards, hence the single reverse.
  def map(xs, f) do
    xs
    |> Enum.reduce([], fn x, acc -> [f.(x) | acc] end)
    |> Enum.reverse()
  end

  @doc "filter, built from Enum.reduce/3 (plus one Enum.reverse/1)."
  def filter(xs, p) do
    xs
    |> Enum.reduce([], fn x, acc -> if p.(x), do: [x | acc], else: acc end)
    |> Enum.reverse()
  end

  @doc """
  Right fold: foldr(f, z, [a, b, c]) == f.(a, f.(b, f.(c, z))).
  Note the argument order of f: element first, accumulator second.
  """
  # Body recursion is the definition itself, and foldr cannot be made tail
  # recursive without reversing first: f is applied on the way back out.
  def foldr(_f, z, []), do: z
  def foldr(f, z, [h | t]), do: f.(h, foldr(f, z, t))

  @doc "Function composition: compose(f, g).(x) == f.(g.(x))."
  def compose(f, g), do: fn x -> f.(g.(x)) end

  @doc "Squares of the even elements, in order. One comprehension, no Enum."
  def evens_squared(xs), do: for(x <- xs, rem(x, 2) == 0, do: x * x)

  @doc """
  All index pairs {i, j} with i < j and xs[i] + xs[j] == target,
  in ascending order. Brute-force two-sum via a comprehension.
  """
  # A tuple gives O(1) indexing; //1 keeps the ranges empty (not descending)
  # when the list is empty or i is the last index.
  def pairs_summing_to(xs, target) do
    arr = List.to_tuple(xs)
    n = tuple_size(arr)

    for i <- 0..(n - 1)//1,
        j <- (i + 1)..(n - 1)//1,
        elem(arr, i) + elem(arr, j) == target,
        do: {i, j}
  end

  @doc """
  The first n integers >= start satisfying p, using a lazy Stream over an
  infinite source. Must terminate: no eager Enum stage before the take.
  """
  # Stream.iterate is infinite; Enum.take/2 halts the pipeline after n hits,
  # so peak extra memory is O(n), not O(size of the source).
  def first_n_matching(start, p, n) do
    start
    |> Stream.iterate(&(&1 + 1))
    |> Stream.filter(p)
    |> Enum.take(n)
  end
end

defmodule FoldsTest do
  use ExUnit.Case

  test "sum" do
    assert Folds.sum([]) == 0
    assert Folds.sum([1, 2, 3, 4]) == 10
    assert Folds.sum(1..100) == 5050
  end

  test "map" do
    assert Folds.map([], &(&1 * 2)) == []
    assert Folds.map([1, 2, 3], &(&1 * &1)) == [1, 4, 9]
    assert Folds.map(["a", "bb"], &String.length/1) == [1, 2]
  end

  test "filter" do
    assert Folds.filter([], &(&1 > 0)) == []
    assert Folds.filter([1, 2, 3, 4], &(rem(&1, 2) == 0)) == [2, 4]
    assert Folds.filter([1, 2, 3], fn _ -> false end) == []
  end

  test "foldr" do
    assert Folds.foldr(&+/2, 0, [1, 2, 3]) == 6
    assert Folds.foldr(&[&1 | &2], [], [1, 2, 3]) == [1, 2, 3]
    assert Folds.foldr(&(&1 <> &2), "", ["a", "b", "c"]) == "abc"
    # foldr is right-associated: 1 - (2 - (3 - 0)) == 2
    assert Folds.foldr(&-/2, 0, [1, 2, 3]) == 2
  end

  test "compose" do
    inc = &(&1 + 1)
    dbl = &(&1 * 2)
    assert Folds.compose(inc, dbl).(5) == 11
    assert Folds.compose(dbl, inc).(5) == 12
    # fusion law: map f ∘ map g ≡ map (f ∘ g)
    xs = [1, 2, 3]
    assert Folds.map(Folds.map(xs, dbl), inc) == Folds.map(xs, Folds.compose(inc, dbl))
  end

  test "evens_squared" do
    assert Folds.evens_squared([]) == []
    assert Folds.evens_squared([1, 2, 3, 4, 5, 6]) == [4, 16, 36]
    assert Folds.evens_squared([1, 3, 5]) == []
  end

  test "pairs_summing_to" do
    assert Folds.pairs_summing_to([], 9) == []
    assert Folds.pairs_summing_to([2, 7, 11, 15], 9) == [{0, 1}]
    assert Folds.pairs_summing_to([3, 3, 3], 6) == [{0, 1}, {0, 2}, {1, 2}]
    assert Folds.pairs_summing_to([1, 2, 3], 100) == []
  end

  test "first_n_matching" do
    assert Folds.first_n_matching(1, &(rem(&1, 7) == 0), 3) == [7, 14, 21]
    assert Folds.first_n_matching(10, &(&1 > 0), 2) == [10, 11]
    assert Folds.first_n_matching(1, &(&1 * &1 > 1_000_000), 1) == [1001]
    assert Folds.first_n_matching(1, &(&1 > 0), 0) == []
  end
end
