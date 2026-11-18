ExUnit.start()

defmodule Maps.Point do
  @moduledoc "A tagged map with a compile-time-fixed key set."
  defstruct x: 0, y: 0
end

defmodule Maps do
  @moduledoc """
  Lesson 07: maps, keyword lists, MapSet, structs, persistence.

  Nothing here mutates. Every function returns a new term and leaves its
  arguments exactly as they were.
  """

  @doc "Value at key, or default when the key is absent. Note: not `m[k] || default`."
  def get_or(_map, _key, _default), do: raise("not implemented")

  @doc "Increment the counter at key, starting from 1 when it is absent."
  def bump(_map, _key), do: raise("not implemented")

  @doc "Count occurrences: [:a, :b, :a] -> %{a: 2, b: 1}. Build it with bump/2."
  def frequencies(_xs), do: raise("not implemented")

  @doc "Merge two maps, adding the values of keys present in both."
  def merge_sums(_m1, _m2), do: raise("not implemented")

  @doc "Distinct elements as a sorted list, via MapSet."
  def unique(_xs), do: raise("not implemented")

  @doc """
  Names of the maps whose :status is :active, in order.
  One comprehension; the generator pattern does the filtering.
  """
  def active_names(_users), do: raise("not implemented")

  @doc "Translate a %Maps.Point{} by {dx, dy}, returning a new point."
  def move(_point, _dx, _dy), do: raise("not implemented")

  @doc """
  put_in/3 over a path list: deep_put(data, [:a, :b], 1).
  Only the nodes on that path are copied; everything else is shared.
  """
  def deep_put(_data, _path, _value), do: raise("not implemented")
end

defmodule MapsTest do
  use ExUnit.Case

  alias Maps.Point

  test "get_or" do
    assert Maps.get_or(%{a: 1}, :a, 0) == 1
    assert Maps.get_or(%{a: 1}, :z, 0) == 0
    # the trap: a stored false must not be replaced by the default
    assert Maps.get_or(%{a: false}, :a, :missing) == false
    assert Maps.get_or(%{a: nil}, :a, :missing) == nil
  end

  test "bump" do
    assert Maps.bump(%{}, :a) == %{a: 1}
    assert Maps.bump(%{a: 1}, :a) == %{a: 2}
    assert Maps.bump(%{a: 1, b: 9}, :b) == %{a: 1, b: 10}
  end

  test "frequencies" do
    assert Maps.frequencies([]) == %{}
    assert Maps.frequencies([:a, :b, :a]) == %{a: 2, b: 1}
    assert Maps.frequencies(~w(x y x x)) == %{"x" => 3, "y" => 1}
  end

  test "merge_sums" do
    assert Maps.merge_sums(%{}, %{a: 1}) == %{a: 1}
    assert Maps.merge_sums(%{a: 1, b: 2}, %{b: 10, c: 5}) == %{a: 1, b: 12, c: 5}
  end

  test "unique" do
    assert Maps.unique([]) == []
    assert Maps.unique([3, 1, 3, 2, 1]) == [1, 2, 3]
    assert Maps.unique([:b, :a, :b]) == [:a, :b]
  end

  test "active_names" do
    users = [
      %{name: "ann", status: :active},
      %{name: "bo", status: :banned},
      %{name: "cy", status: :active, extra: 1}
    ]

    assert Maps.active_names(users) == ["ann", "cy"]
    assert Maps.active_names([]) == []
  end

  test "move" do
    p = %Point{x: 1, y: 2}
    q = Maps.move(p, 10, -2)
    assert q == %Point{x: 11, y: 0}
    # persistence: the original is untouched
    assert p == %Point{x: 1, y: 2}
    assert is_struct(q, Point)
  end

  test "deep_put" do
    data = %{user: %{name: "ann", scores: %{math: 90}}}
    updated = Maps.deep_put(data, [:user, :scores, :math], 95)
    assert updated == %{user: %{name: "ann", scores: %{math: 95}}}
    assert data == %{user: %{name: "ann", scores: %{math: 90}}}
  end
end
