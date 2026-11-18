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
  def max_depth(nil), do: 0
  def max_depth({:node, _v, l, r}), do: 1 + max(max_depth(l), max_depth(r))

  @doc """
  Inorder traversal: left, node, right. Written with an accumulator so the
  result is built by consing — `++` per node would make it O(n²).
  Cost: O(n) time, O(h) stack.
  """
  def inorder(t), do: inorder(t, [])

  defp inorder(nil, acc), do: acc
  defp inorder({:node, v, l, r}, acc), do: inorder(l, [v | inorder(r, acc)])

  @doc """
  Binary Tree Level Order Traversal: a list of levels, top to bottom.
  BFS done as a fold over levels — the frontier *is* the queue.
  Cost: O(n) time, O(w) space (w = maximum level width).
  """
  def level_order(nil), do: []
  def level_order(root), do: levels([root], [])

  defp levels([], acc), do: Enum.reverse(acc)

  defp levels(frontier, acc) do
    values = Enum.map(frontier, fn {:node, v, _l, _r} -> v end)

    next =
      Enum.flat_map(frontier, fn {:node, _v, l, r} ->
        Enum.reject([l, r], &is_nil/1)
      end)

    levels(next, [values | acc])
  end

  @doc """
  Number of Islands. The grid is a list of binaries of `?1`/`?0`; land cells
  become a MapSet of `{row, col}`. Flood fill by DFS with the visited set
  threaded through the recursion.
  Cost: O(n log n) time, O(n) space (n = number of cells).
  """
  def num_islands(rows) do
    land =
      for {row, r} <- Enum.with_index(rows),
          {ch, c} <- Enum.with_index(String.to_charlist(row)),
          ch == ?1,
          into: MapSet.new(),
          do: {r, c}

    {count, _seen} =
      Enum.reduce(land, {0, MapSet.new()}, fn cell, {count, seen} ->
        if MapSet.member?(seen, cell),
          do: {count, seen},
          else: {count + 1, flood(cell, land, seen)}
      end)

    count
  end

  defp flood(cell, land, seen) do
    if MapSet.member?(seen, cell) or not MapSet.member?(land, cell) do
      seen
    else
      {r, c} = cell
      seen = MapSet.put(seen, cell)

      Enum.reduce([{r - 1, c}, {r + 1, c}, {r, c - 1}, {r, c + 1}], seen, fn n, seen ->
        flood(n, land, seen)
      end)
    end
  end

  @doc """
  Course Schedule: can all `n` courses be finished, given `[[a, b]]` meaning
  "b before a"? Kahn's topological sort; the answer is "every vertex was
  emitted", i.e. the graph is acyclic.
  Cost: O(n + e) up to map-lookup logs.
  """
  def can_finish(n, prereqs) do
    adj = Enum.reduce(prereqs, %{}, fn [a, b], m -> Map.update(m, b, [a], &[a | &1]) end)
    zero = Map.new(0..(n - 1)//1, &{&1, 0})
    indeg = Enum.reduce(prereqs, zero, fn [a, _b], m -> Map.update!(m, a, &(&1 + 1)) end)
    ready = for {v, 0} <- indeg, do: v
    kahn(ready, adj, indeg, 0) == n
  end

  defp kahn([], _adj, _indeg, done), do: done

  defp kahn([v | rest], adj, indeg, done) do
    {ready, indeg} =
      Enum.reduce(Map.get(adj, v, []), {rest, indeg}, fn w, {q, d} ->
        d = Map.update!(d, w, &(&1 - 1))
        if d[w] == 0, do: {[w | q], d}, else: {q, d}
      end)

    kahn(ready, adj, indeg, done + 1)
  end

  @doc """
  Coin Change: fewest coins summing to `amount`, or -1. Memoised recursion —
  the memo is threaded in and out, so `{value, memo}` is the return shape.
  Cost: O(amount × |coins|) time, O(amount) space.
  """
  def coin_change(coins, amount) do
    {best, _memo} = cc(amount, coins, %{})

    case best do
      :inf -> -1
      n -> n
    end
  end

  defp cc(0, _coins, memo), do: {0, memo}
  defp cc(a, _coins, memo) when a < 0, do: {:inf, memo}

  defp cc(a, coins, memo) do
    case Map.fetch(memo, a) do
      {:ok, v} ->
        {v, memo}

      :error ->
        {best, memo} =
          Enum.reduce(coins, {:inf, memo}, fn c, {best, memo} ->
            {sub, memo} = cc(a - c, coins, memo)
            {min_inf(best, succ(sub)), memo}
          end)

        {best, Map.put(memo, a, best)}
    end
  end

  defp succ(:inf), do: :inf
  defp succ(n), do: n + 1
  defp min_inf(:inf, b), do: b
  defp min_inf(a, :inf), do: a
  defp min_inf(a, b), do: min(a, b)

  @doc """
  Climbing Stairs: f(0) = f(1) = 1, f(n) = f(n-1) + f(n-2). Bottom-up as a
  fold carrying the window `{f(k), f(k+1)}`.
  Cost: O(n) time, O(1) space.
  """
  def climb_stairs(n) when n >= 0 do
    {f, _next} = Enum.reduce(1..n//1, {1, 1}, fn _k, {a, b} -> {b, a + b} end)
    f
  end

  @doc """
  Top K Frequent Elements. Count with `Enum.frequencies/1`, then keep a
  bounded min-heap (`:gb_sets` of `{count, value}`) of size k.
  Cost: O(n log k) time, O(n) space. Result is ordered most frequent first.
  """
  def top_k_frequent(nums, k) do
    nums
    |> Enum.frequencies()
    |> Enum.reduce(:gb_sets.new(), fn {v, c}, heap ->
      heap = :gb_sets.add({c, v}, heap)

      if :gb_sets.size(heap) > k do
        {_smallest, heap} = :gb_sets.take_smallest(heap)
        heap
      else
        heap
      end
    end)
    |> :gb_sets.to_list()
    |> Enum.reverse()
    |> Enum.map(fn {_c, v} -> v end)
  end
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
