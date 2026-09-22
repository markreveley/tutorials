ExUnit.start()

defmodule Tail do
  @moduledoc """
  Lesson 05: accumulators and tail calls.

  Every function here must run in constant stack. Write a private helper
  that carries the accumulator and keep the public function a thin wrapper.
  """

  @doc "Sum of a list of numbers. Accumulator starts at 0."
  # Lemma: do_sum(xs, a) ≡ sum(xs) + a, so do_sum(xs, 0) ≡ sum(xs).
  def sum(xs), do: do_sum(xs, 0)

  defp do_sum([], acc), do: acc
  defp do_sum([h | t], acc), do: do_sum(t, acc + h)

  @doc "Reverse a list by consing onto an accumulator. O(n)."
  # Lemma: do_rev(xs, a) ≡ rev(xs) ++ a, so do_rev(xs, []) ≡ rev(xs).
  def reverse(xs), do: do_rev(xs, [])

  defp do_rev([], acc), do: acc
  defp do_rev([h | t], acc), do: do_rev(t, [h | acc])

  @doc "Length of a list, without using Kernel.length/1."
  def count(xs), do: do_count(xs, 0)

  defp do_count([], acc), do: acc
  defp do_count([_h | t], acc), do: do_count(t, acc + 1)

  @doc "Apply f to every element, preserving order."
  def map(xs, f), do: do_map(xs, f, [])

  defp do_map([], _f, acc), do: reverse(acc)
  defp do_map([h | t], f, acc), do: do_map(t, f, [f.(h) | acc])

  @doc "The list [a, a+1, ..., b], or [] when a > b."
  # Counting *down* means the accumulator is already in ascending order:
  # no final reverse is needed. The accumulator's direction is a choice.
  def range(a, b), do: do_range(a, b, [])

  defp do_range(a, b, acc) when b < a, do: acc
  defp do_range(a, b, acc), do: do_range(a, b - 1, [b | acc])

  @doc "Nth Fibonacci number with two accumulators. fib(0) == 0, fib(1) == 1."
  # Invariant: do_fib(n, fib(k), fib(k+1)) ≡ fib(k + n); at k = 0, do_fib(n, 0, 1).
  def fib(n) when n >= 0, do: do_fib(n, 0, 1)

  defp do_fib(0, a, _b), do: a
  defp do_fib(n, a, b), do: do_fib(n - 1, b, a + b)

  @doc "Prefix sums: [1, 2, 3, 4] -> [1, 3, 6, 10]."
  def running_sum(xs), do: do_running(xs, 0, [])

  defp do_running([], _total, acc), do: reverse(acc)
  defp do_running([h | t], total, acc), do: do_running(t, total + h, [total + h | acc])
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
