ExUnit.start()

defmodule Patterns do
  @moduledoc "Lesson 02: patterns, guards, multi-clause functions."

  @doc "Return the head of a list; return the default for the empty list."
  def head_or([h | _], _default), do: h
  def head_or([], default), do: default

  @doc """
  Name the shape of a term:
  :empty_list, :one_element_list, :longer_list,
  :empty_tuple, :ok_tuple, :error_tuple, :other_tuple,
  :empty_map, :map, or :other.
  """
  def describe([]), do: :empty_list
  def describe([_]), do: :one_element_list
  def describe([_ | _]), do: :longer_list
  def describe({}), do: :empty_tuple
  def describe({:ok, _}), do: :ok_tuple
  def describe({:error, _}), do: :error_tuple
  def describe(t) when is_tuple(t), do: :other_tuple
  def describe(m) when is_map(m) and map_size(m) == 0, do: :empty_map
  def describe(m) when is_map(m), do: :map
  def describe(_), do: :other

  @doc "Return :negative, :zero or :positive for a number."
  def sign(n) when n < 0, do: :negative
  def sign(n) when n == 0, do: :zero
  def sign(n) when is_number(n), do: :positive

  @doc "True when `value` matches `target` exactly. Use the pin operator."
  def pinned?(value, target) do
    case value do
      ^target -> true
      _ -> false
    end
  end

  @doc """
  Build a display name from a map with optional :first and :last keys.
  Both -> "first last"; one -> that one; neither -> "anonymous".
  """
  def full_name(%{first: f, last: l}), do: f <> " " <> l
  def full_name(%{first: f}), do: f
  def full_name(%{last: l}), do: l
  def full_name(_), do: "anonymous"

  @doc "Return {:ok, first_byte} of a binary, or :error when it is empty."
  def first_byte(<<b, _::binary>>), do: {:ok, b}
  def first_byte(<<>>), do: :error

  @doc """
  Split a request line: "GET /a" -> {:get, "/a"}, "POST /a" -> {:post, "/a"},
  anything else -> :unknown.
  """
  def method_and_path(<<"GET ", path::binary>>), do: {:get, path}
  def method_and_path(<<"POST ", path::binary>>), do: {:post, path}
  def method_and_path(_), do: :unknown
end

defmodule PatternsTest do
  use ExUnit.Case

  test "head_or" do
    assert Patterns.head_or([1, 2, 3], :none) == 1
    assert Patterns.head_or([], :none) == :none
    assert Patterns.head_or([:only], 0) == :only
  end

  test "describe lists" do
    assert Patterns.describe([]) == :empty_list
    assert Patterns.describe([1]) == :one_element_list
    assert Patterns.describe([1, 2]) == :longer_list
  end

  test "describe tuples" do
    assert Patterns.describe({}) == :empty_tuple
    assert Patterns.describe({:ok, 1}) == :ok_tuple
    assert Patterns.describe({:error, :bad}) == :error_tuple
    assert Patterns.describe({1, 2, 3}) == :other_tuple
  end

  test "describe maps and everything else" do
    assert Patterns.describe(%{}) == :empty_map
    assert Patterns.describe(%{a: 1}) == :map
    assert Patterns.describe(42) == :other
    assert Patterns.describe(:atom) == :other
  end

  test "sign" do
    assert Patterns.sign(-3) == :negative
    assert Patterns.sign(0) == :zero
    assert Patterns.sign(2.5) == :positive
  end

  test "pinned?" do
    assert Patterns.pinned?(3, 3)
    refute Patterns.pinned?(3, 4)
    assert Patterns.pinned?({:ok, [1]}, {:ok, [1]})
    refute Patterns.pinned?({:ok, [1]}, {:ok, [2]})
  end

  test "full_name" do
    assert Patterns.full_name(%{first: "ada", last: "lovelace"}) == "ada lovelace"
    assert Patterns.full_name(%{first: "ada"}) == "ada"
    assert Patterns.full_name(%{last: "lovelace"}) == "lovelace"
    assert Patterns.full_name(%{age: 36}) == "anonymous"
  end

  test "first_byte" do
    assert Patterns.first_byte("abc") == {:ok, ?a}
    assert Patterns.first_byte(<<7, 8>>) == {:ok, 7}
    assert Patterns.first_byte("") == :error
  end

  test "method_and_path" do
    assert Patterns.method_and_path("GET /index") == {:get, "/index"}
    assert Patterns.method_and_path("POST /form") == {:post, "/form"}
    assert Patterns.method_and_path("DELETE /x") == :unknown
  end
end
