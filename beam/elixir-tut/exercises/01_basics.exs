ExUnit.start()

defmodule Basics do
  @moduledoc "Lesson 01: values, atoms, tuples, the match operator."

  @doc "Swap the two elements of a pair: {a, b} -> {b, a}."
  def swap(_pair), do: raise("not implemented")

  @doc """
  Return an atom naming the kind of term: :integer, :float, :atom,
  :tuple, :list, :binary, or :other.
  """
  def classify(_term), do: raise("not implemented")

  @doc "Return v from {:ok, v}; return :error for anything else."
  def unwrap_ok(_term), do: raise("not implemented")

  @doc "Componentwise sum of two {x, y} points."
  def point_add(_p, _q), do: raise("not implemented")

  @doc "Manhattan distance |x1-x2| + |y1-y2| between two {x, y} points."
  def manhattan(_p, _q), do: raise("not implemented")

  @doc "Integer division wrapped: {:ok, div(a, b)} or {:error, :division_by_zero}."
  def safe_div(_a, _b), do: raise("not implemented")

  @doc """
  Given {:rgb, r, g, b} return {:gray, (r+g+b) div 3}.
  Given {:gray, v} return it unchanged.
  """
  def to_gray(_color), do: raise("not implemented")
end

defmodule BasicsTest do
  use ExUnit.Case

  test "swap" do
    assert Basics.swap({1, 2}) == {2, 1}
    assert Basics.swap({:a, "b"}) == {"b", :a}
  end

  test "classify" do
    assert Basics.classify(1) == :integer
    assert Basics.classify(1.5) == :float
    assert Basics.classify(:x) == :atom
    assert Basics.classify({1}) == :tuple
    assert Basics.classify([1]) == :list
    assert Basics.classify("s") == :binary
    assert Basics.classify(%{}) == :other
  end

  test "unwrap_ok" do
    assert Basics.unwrap_ok({:ok, 5}) == 5
    assert Basics.unwrap_ok({:error, :bad}) == :error
    assert Basics.unwrap_ok(:ok) == :error
  end

  test "point_add" do
    assert Basics.point_add({1, 2}, {3, 4}) == {4, 6}
    assert Basics.point_add({-1, 0}, {1, 0}) == {0, 0}
  end

  test "manhattan" do
    assert Basics.manhattan({0, 0}, {3, 4}) == 7
    assert Basics.manhattan({-2, 5}, {1, 1}) == 7
  end

  test "safe_div" do
    assert Basics.safe_div(7, 2) == {:ok, 3}
    assert Basics.safe_div(7, 0) == {:error, :division_by_zero}
  end

  test "to_gray" do
    assert Basics.to_gray({:rgb, 30, 60, 90}) == {:gray, 60}
    assert Basics.to_gray({:gray, 7}) == {:gray, 7}
  end
end
