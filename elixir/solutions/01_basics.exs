ExUnit.start()

defmodule Basics do
  @moduledoc "Lesson 01: values, atoms, tuples, the match operator."

  def swap({a, b}), do: {b, a}

  def classify(term) do
    cond do
      is_integer(term) -> :integer
      is_float(term) -> :float
      is_atom(term) -> :atom
      is_tuple(term) -> :tuple
      is_list(term) -> :list
      is_binary(term) -> :binary
      true -> :other
    end
  end

  def unwrap_ok(term) do
    case term do
      {:ok, v} -> v
      _ -> :error
    end
  end

  def point_add({x1, y1}, {x2, y2}), do: {x1 + x2, y1 + y2}

  def manhattan({x1, y1}, {x2, y2}), do: abs(x1 - x2) + abs(y1 - y2)

  def safe_div(_a, 0), do: {:error, :division_by_zero}
  def safe_div(a, b), do: {:ok, div(a, b)}

  def to_gray({:rgb, r, g, b}), do: {:gray, div(r + g + b, 3)}
  def to_gray({:gray, _} = c), do: c
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
