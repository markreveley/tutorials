ExUnit.start()

defmodule Tree do
  @moduledoc """
  A binary tree is `nil` or `{:node, value, left, right}` — an inductive
  type with one base case and one step case, so every function over it is
  written by structural recursion and proved by structural induction.
  """

  @doc "Build a leaf. Cost: O(1)."
  def leaf(v), do: {:node, v, nil, nil}

  @doc "Build an internal node. Cost: O(1)."
  def node(v, l, r), do: {:node, v, l, r}

  @doc """
  Build from a level-order (heap-layout) list: the children of index i are
  at 2i+1 and 2i+2, and `nil` means "no subtree here".
  Cost: O(n).
  """
  def from_list(xs) when is_list(xs), do: build(List.to_tuple(xs), 0)

  defp build(t, i) when i >= tuple_size(t), do: nil

  defp build(t, i) do
    case elem(t, i) do
      nil -> nil
      v -> {:node, v, build(t, 2 * i + 1), build(t, 2 * i + 2)}
    end
  end
end

defmodule Graph do
  @moduledoc "A graph is `%{node => [neighbour]}`. Adjacency lookup is O(log n)."

  @doc "Directed graph from `[{u, v}]` edges, every mentioned vertex present. Cost: O(e log n)."
  def from_edges(edges) do
    Enum.reduce(edges, %{}, fn {u, v}, g ->
      g |> Map.put_new(v, []) |> Map.update(u, [v], &[v | &1])
    end)
  end

  @doc "Undirected graph from `[{u, v}]` edges. Cost: O(e log n)."
  def undirected(edges) do
    from_edges(Enum.flat_map(edges, fn {u, v} -> [{u, v}, {v, u}] end))
  end

  @doc "Neighbours of v, `[]` if v is unknown. Cost: O(log n)."
  def neighbours(g, v), do: Map.get(g, v, [])
end

defmodule PatternsII do
  @moduledoc """
  Lesson 12: trees, graphs, BFS/DFS, DP as memoised recursion, heaps.

  Mutation is replaced by *state threading*: a function that would mutate a
  visited-set or a memo table instead takes it as an argument and returns
  the updated copy alongside its result.
  """

  @doc """
  Maximum Depth of Binary Tree. Structural recursion; proof by structural
  induction on the tree.
  Cost: O(n) time, O(h) stack (n = nodes, h = height).
  """
  def max_depth(_tree), do: raise("not implemented")

  @doc """
  Inorder traversal: left, node, right. Written with an accumulator so the
  result is built by consing — `++` per node would make it O(n²).
  Cost: O(n) time, O(h) stack.
  """
  def inorder(_tree), do: raise("not implemented")

  @doc """
  Binary Tree Level Order Traversal: a list of levels, top to bottom.
  BFS done as a fold over levels — the frontier *is* the queue.
  Cost: O(n) time, O(w) space (w = maximum level width).
  """
  def level_order(_tree), do: raise("not implemented")

  @doc """
  Number of Islands. The grid is a list of binaries of `?1`/`?0`; land cells
  become a MapSet of `{row, col}`. Flood fill by DFS with the visited set
  threaded through the recursion.
  Cost: O(n log n) time, O(n) space (n = number of cells).
  """
  def num_islands(_rows), do: raise("not implemented")

  @doc """
  Course Schedule: can all `n` courses be finished, given `[[a, b]]` meaning
  "b before a"? Kahn's topological sort; the answer is "every vertex was
  emitted", i.e. the graph is acyclic.
  Cost: O(n + e) up to map-lookup logs.
  """
  def can_finish(_n, _prereqs), do: raise("not implemented")

  @doc """
  Coin Change: fewest coins summing to `amount`, or -1. Memoised recursion —
  the memo is threaded in and out, so `{value, memo}` is the return shape.
  Cost: O(amount × |coins|) time, O(amount) space.
  """
  def coin_change(_coins, _amount), do: raise("not implemented")

  @doc """
  Climbing Stairs: f(0) = f(1) = 1, f(n) = f(n-1) + f(n-2). Bottom-up as a
  fold carrying the window `{f(k), f(k+1)}`.
  Cost: O(n) time, O(1) space.
  """
  def climb_stairs(_n), do: raise("not implemented")

  @doc """
  Top K Frequent Elements. Count with `Enum.frequencies/1`, then keep a
  bounded min-heap (`:gb_sets` of `{count, value}`) of size k.
  Cost: O(n log k) time, O(n) space. Result is ordered most frequent first.
  """
  def top_k_frequent(_nums, _k), do: raise("not implemented")
end

defmodule PatternsIITest do
  use ExUnit.Case

  # 3
  # / \
  # 9  20
  #    /  \
  #   15   7
  defp sample, do: Tree.from_list([3, 9, 20, nil, nil, 15, 7])

  test "max_depth" do
    assert PatternsII.max_depth(nil) == 0
    assert PatternsII.max_depth(Tree.leaf(1)) == 1
    assert PatternsII.max_depth(sample()) == 3
    assert PatternsII.max_depth(Tree.node(1, nil, Tree.node(2, nil, Tree.leaf(3)))) == 3
  end

  test "inorder" do
    assert PatternsII.inorder(nil) == []
    assert PatternsII.inorder(Tree.leaf(1)) == [1]
    assert PatternsII.inorder(sample()) == [9, 3, 15, 20, 7]
    bst = Tree.node(2, Tree.leaf(1), Tree.leaf(3))
    assert PatternsII.inorder(bst) == [1, 2, 3]
  end

  test "level_order" do
    assert PatternsII.level_order(nil) == []
    assert PatternsII.level_order(Tree.leaf(1)) == [[1]]
    assert PatternsII.level_order(sample()) == [[3], [9, 20], [15, 7]]
  end

  test "num_islands" do
    assert PatternsII.num_islands([
             "11110",
             "11010",
             "11000",
             "00000"
           ]) == 1

    assert PatternsII.num_islands([
             "11000",
             "11000",
             "00100",
             "00011"
           ]) == 3

    assert PatternsII.num_islands(["000", "000"]) == 0
    assert PatternsII.num_islands([]) == 0
  end

  test "can_finish" do
    assert PatternsII.can_finish(2, [[1, 0]])
    refute PatternsII.can_finish(2, [[1, 0], [0, 1]])
    assert PatternsII.can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    refute PatternsII.can_finish(3, [[0, 1], [1, 2], [2, 0]])
    assert PatternsII.can_finish(3, [])
  end

  test "coin_change" do
    assert PatternsII.coin_change([1, 2, 5], 11) == 3
    assert PatternsII.coin_change([2], 3) == -1
    assert PatternsII.coin_change([1], 0) == 0
    assert PatternsII.coin_change([2, 5, 10], 27) == 4
    assert PatternsII.coin_change([186, 419, 83, 408], 6249) == 20
  end

  test "climb_stairs" do
    assert PatternsII.climb_stairs(0) == 1
    assert PatternsII.climb_stairs(1) == 1
    assert PatternsII.climb_stairs(2) == 2
    assert PatternsII.climb_stairs(3) == 3
    assert PatternsII.climb_stairs(5) == 8
    assert PatternsII.climb_stairs(45) == 1_836_311_903
  end

  test "top_k_frequent" do
    assert PatternsII.top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
    assert PatternsII.top_k_frequent([1], 1) == [1]
    assert PatternsII.top_k_frequent([4, 4, 4, 5, 5, 6], 3) == [4, 5, 6]
    assert PatternsII.top_k_frequent([], 3) == []
  end

  test "graph helpers" do
    g = Graph.undirected([{:a, :b}, {:b, :c}])
    assert Enum.sort(Graph.neighbours(g, :b)) == [:a, :c]
    assert Graph.neighbours(g, :z) == []
  end
end
