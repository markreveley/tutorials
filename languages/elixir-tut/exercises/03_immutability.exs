ExUnit.start()

defmodule Immutability do
  @moduledoc "Lesson 03: immutability, rebinding, referential transparency."

  @doc """
  Bind y = n, then rebind y twice: y = y + 1, then y = y * 2.
  Return {n, y}. The parameter n must be unaffected.
  """
  def rebind(_n), do: raise("not implemented")

  @doc """
  Capture n in a zero-arity closure, then rebind n to n + 100.
  Return {closure_result, n}. The closure sees the value it captured.
  """
  def closure_sees_old_value(_n), do: raise("not implemented")

  @doc "Return {put_elem(t, i, v), t} — the new tuple and the untouched original."
  def put_elem_pure(_t, _i, _v), do: raise("not implemented")

  @doc "Return {Map.put(m, k, v), m} — the new map and the untouched original."
  def map_put_pure(_m, _k, _v), do: raise("not implemented")

  @doc """
  Cons x onto xs and report whether the tail of the result is the *same*
  memory as xs (not merely equal). Return {[x | xs], shared?}.
  Use `:erts_debug.same/2`.
  """
  def cons_shares_tail(_x, _xs), do: raise("not implemented")

  @doc """
  Compute (n + 1) * (n + 1) by binding the common subexpression once.
  Equational reasoning says the two forms are interchangeable.
  """
  def square_of_succ(_n), do: raise("not implemented")

  @doc "Swap a pair twice. swap ∘ swap ≡ id, so this returns the input."
  def swap_twice(_pair), do: raise("not implemented")
end

defmodule ImmutabilityTest do
  use ExUnit.Case

  test "rebind does not touch n" do
    assert Immutability.rebind(3) == {3, 8}
    assert Immutability.rebind(0) == {0, 2}
  end

  test "a closure captures the value, not the name" do
    assert Immutability.closure_sees_old_value(5) == {5, 105}
  end

  test "put_elem returns a new tuple and leaves the old one alone" do
    assert Immutability.put_elem_pure({1, 2, 3}, 0, :x) == {{:x, 2, 3}, {1, 2, 3}}
  end

  test "Map.put returns a new map and leaves the old one alone" do
    assert Immutability.map_put_pure(%{a: 1}, :b, 2) == {%{a: 1, b: 2}, %{a: 1}}
    assert Immutability.map_put_pure(%{a: 1}, :a, 9) == {%{a: 9}, %{a: 1}}
  end

  test "cons shares the tail rather than copying it" do
    xs = [1, 2, 3]
    assert {[0, 1, 2, 3], true} = Immutability.cons_shares_tail(0, xs)
    assert {[:a], true} = Immutability.cons_shares_tail(:a, [])
  end

  test "square_of_succ" do
    assert Immutability.square_of_succ(4) == 25
    assert Immutability.square_of_succ(-1) == 0
    assert Immutability.square_of_succ(0) == 1
  end

  test "swap twice is the identity" do
    assert Immutability.swap_twice({1, :two}) == {1, :two}
    assert Immutability.swap_twice({[], "s"}) == {[], "s"}
  end
end
