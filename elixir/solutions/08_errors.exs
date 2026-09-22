ExUnit.start()

defmodule Errors do
  @moduledoc "Lesson 08: pipes, `with`, and errors as sum types."

  @doc """
  Lowercase, trim, and squash every run of non-alphanumeric characters
  into a single "-", with no leading or trailing "-".
  """
  def slugify(s) do
    s
    |> String.downcase()
    |> String.trim()
    |> String.replace(~r/[^a-z0-9]+/, "-")
    |> String.trim("-")
  end

  @doc """
  Parse a whole string as an integer.
  {:ok, n} if the string is exactly an integer, else
  {:error, :not_an_integer}.
  """
  def parse_int(s) do
    case Integer.parse(s) do
      {n, ""} -> {:ok, n}
      {_n, _rest} -> {:error, :not_an_integer}
      :error -> {:error, :not_an_integer}
    end
  end

  @doc "Integer division: {:ok, div(a, b)} or {:error, :division_by_zero}."
  def safe_div(_a, 0), do: {:error, :division_by_zero}
  def safe_div(a, b), do: {:ok, div(a, b)}

  @doc "Map lookup as a sum type: {:ok, v} or {:error, {:missing, key}}."
  def fetch(map, key) do
    case Map.fetch(map, key) do
      {:ok, v} -> {:ok, v}
      :error -> {:error, {:missing, key}}
    end
  end

  @doc """
  Given a map with :total and :count, return {:ok, total div count}.
  The first failing step wins: a missing key beats a later division by
  zero, and no later step runs.
  """
  def unit_cost(order) do
    with {:ok, total} <- fetch(order, :total),
         {:ok, count} <- fetch(order, :count),
         {:ok, cost} <- safe_div(total, count) do
      {:ok, cost}
    end
  end

  @doc "Return v from {:ok, v}; raise ArgumentError on {:error, e}."
  def unwrap!({:ok, v}), do: v

  def unwrap!({:error, e}) do
    raise ArgumentError, "unwrap! on error: #{inspect(e)}"
  end

  @doc """
  Turn a list of results into a result of a list:
  {:ok, values} if every element is {:ok, v}, else the FIRST {:error, e}.
  Stops at the first error.
  """
  def traverse(results) do
    Enum.reduce_while(results, {:ok, []}, fn
      {:ok, v}, {:ok, acc} -> {:cont, {:ok, [v | acc]}}
      {:error, e}, _acc -> {:halt, {:error, e}}
    end)
    |> case do
      {:ok, acc} -> {:ok, Enum.reverse(acc)}
      {:error, e} -> {:error, e}
    end
  end
end

defmodule ErrorsTest do
  use ExUnit.Case

  test "slugify" do
    assert Errors.slugify("  Hello, World!  ") == "hello-world"
    assert Errors.slugify("Elixir   is   FUN") == "elixir-is-fun"
    assert Errors.slugify("---a---") == "a"
  end

  test "parse_int" do
    assert Errors.parse_int("42") == {:ok, 42}
    assert Errors.parse_int("-7") == {:ok, -7}
    assert Errors.parse_int("12abc") == {:error, :not_an_integer}
    assert Errors.parse_int("abc") == {:error, :not_an_integer}
  end

  test "safe_div" do
    assert Errors.safe_div(7, 2) == {:ok, 3}
    assert Errors.safe_div(7, 0) == {:error, :division_by_zero}
  end

  test "fetch" do
    assert Errors.fetch(%{a: 1}, :a) == {:ok, 1}
    assert Errors.fetch(%{a: 1}, :b) == {:error, {:missing, :b}}
  end

  test "unit_cost succeeds" do
    assert Errors.unit_cost(%{total: 100, count: 4}) == {:ok, 25}
  end

  test "unit_cost: the first error wins and later steps do not run" do
    # :count is missing AND would be zero-divided; the missing key wins.
    assert Errors.unit_cost(%{total: 100}) == {:error, {:missing, :count}}
    assert Errors.unit_cost(%{count: 0}) == {:error, {:missing, :total}}
    assert Errors.unit_cost(%{total: 1, count: 0}) == {:error, :division_by_zero}
  end

  test "unwrap!" do
    assert Errors.unwrap!({:ok, 5}) == 5

    assert_raise ArgumentError, fn -> Errors.unwrap!({:error, :nope}) end
  end

  test "traverse" do
    assert Errors.traverse([{:ok, 1}, {:ok, 2}, {:ok, 3}]) == {:ok, [1, 2, 3]}
    assert Errors.traverse([]) == {:ok, []}
    assert Errors.traverse([{:ok, 1}, {:error, :a}, {:error, :b}]) == {:error, :a}
  end
end
