ExUnit.start()

defmodule Tail do
  @moduledoc """
  Lesson 05: accumulators and tail calls.

  Every function here must run in constant stack. Write a private helper
  that carries the accumulator and keep the public function a thin wrapper.
  """

  @doc "Sum of a list of numbers. Accumulator starts at 0."
  def sum(_xs), do: raise("not implemented")

  @doc "Reverse a list by consing onto an accumulator. O(n)."
  def reverse(_xs), do: raise("not implemented")

  @doc "Length of a list, without using Kernel.length/1."
  def count(_xs), do: raise("not implemented")

  @doc "Apply f to every element, preserving order."
  def map(_xs, _f), do: raise("not implemented")

  @doc "The list [a, a+1, ..., b], or [] when a > b."
  def range(_a, _b), do: raise("not implemented")

  @doc "Nth Fibonacci number with two accumulators. fib(0) == 0, fib(1) == 1."
  def fib(_n), do: raise("not implemented")

  @doc "Prefix sums: [1, 2, 3, 4] -> [1, 3, 6, 10]."
  def running_sum(_xs), do: raise("not implemented")
end

defmodule TailTest do
  use ExUnit.Case

  test "sum" do
    assert Tail.sum([]) == 0
    assert Tail.sum([1, 2, 3, 4]) == 10
    assert Tail.sum(Enum.to_list(1..100_000)) == 5_000_050_000
  end

  test "reverse" do
    assert Tail.reverse([]) == []
    assert Tail.reverse([1, 2, 3]) == [3, 2, 1]
    assert Tail.reverse(Tail.reverse([1, 2, 3])) == [1, 2, 3]
  end

  test "count" do
    assert Tail.count([]) == 0
    assert Tail.count([:a, :b, :c]) == 3
    assert Tail.count(Enum.to_list(1..100_000)) == 100_000
  end

  test "map" do
    assert Tail.map([], &(&1 * 2)) == []
    assert Tail.map([1, 2, 3], &(&1 * &1)) == [1, 4, 9]
    assert Tail.map([1, 2, 3], &Integer.to_string/1) == ["1", "2", "3"]
  end

  test "range" do
    assert Tail.range(1, 5) == [1, 2, 3, 4, 5]
    assert Tail.range(3, 3) == [3]
    assert Tail.range(5, 1) == []
    assert Tail.count(Tail.range(1, 50_000)) == 50_000
  end

  test "fib" do
    assert Tail.fib(0) == 0
    assert Tail.fib(1) == 1
    assert Tail.fib(10) == 55
    assert Tail.fib(90) == 2_880_067_194_370_816_120
  end

  test "running_sum" do
    assert Tail.running_sum([]) == []
    assert Tail.running_sum([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert Tail.running_sum([3, 1, 2, 10, 1]) == [3, 4, 6, 16, 17]
  end
end
