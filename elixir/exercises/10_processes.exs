ExUnit.start()

defmodule Processes do
  @moduledoc "Lesson 10: processes, messages, actors, GenServer."

  @doc """
  Spawn a process, send it a term, and wait for it to send the term back.
  Returns {:pong, term}, or :timeout if no reply arrives within 1000 ms.
  """
  def ping(_term), do: raise("not implemented")

  @doc """
  Send every element of msgs to self() tagged {:drain, m}, then receive
  exactly that many messages back. The result equals msgs: per sender /
  receiver pair, message order is preserved.
  """
  def drain(_msgs), do: raise("not implemented")

  @doc """
  Map fun over xs in parallel, preserving order. Spawn all tasks first,
  then await them all.
  """
  def parallel_map(_xs, _fun), do: raise("not implemented")

  @doc "Sum a list by folding updates into an Agent, then reading it."
  def sum_with_agent(_xs), do: raise("not implemented")

  @doc """
  Run fun in a monitored process and return the reason it terminated
  (:normal for a clean exit). :timeout if nothing arrives within 1000 ms.
  """
  def down_reason(_fun), do: raise("not implemented")

  defmodule Counter do
    @moduledoc "A minimal GenServer: synchronous read, asynchronous write."
    use GenServer

    @doc "Start a counter holding n. Returns {:ok, pid}."
    def start_link(_n), do: raise("not implemented")

    @doc "Read the counter synchronously."
    def value(_pid), do: raise("not implemented")

    @doc "Add k to the counter asynchronously. Returns :ok immediately."
    def bump(_pid, _k), do: raise("not implemented")

    @doc "Server callback: the initial state."
    @impl true
    def init(_n), do: raise("not implemented")

    @doc "Server callback: reply with the state, keep it unchanged."
    @impl true
    def handle_call(_msg, _from, _n), do: raise("not implemented")

    @doc "Server callback: no reply, new state n + k."
    @impl true
    def handle_cast(_msg, _n), do: raise("not implemented")
  end
end

defmodule ProcessesTest do
  use ExUnit.Case

  test "ping" do
    assert Processes.ping(:hello) == {:pong, :hello}
    assert Processes.ping({1, 2}) == {:pong, {1, 2}}
  end

  test "drain preserves per-pair order" do
    assert Processes.drain([1, 2, 3]) == [1, 2, 3]
    assert Processes.drain([:a, :b]) == [:a, :b]
    assert Processes.drain([]) == []
  end

  test "parallel_map" do
    assert Processes.parallel_map([1, 2, 3], &(&1 * &1)) == [1, 4, 9]
    assert Processes.parallel_map([], &(&1 * 2)) == []
    # order is by input, not by completion
    assert Processes.parallel_map([3, 1, 2], & &1) == [3, 1, 2]
  end

  test "sum_with_agent" do
    assert Processes.sum_with_agent([1, 2, 3, 4]) == 10
    assert Processes.sum_with_agent([]) == 0
    assert Processes.sum_with_agent([-1, 1]) == 0
  end

  test "down_reason" do
    assert Processes.down_reason(fn -> :ok end) == :normal
    assert Processes.down_reason(fn -> exit(:boom) end) == :boom
  end

  test "Counter: call reads state" do
    {:ok, c} = Processes.Counter.start_link(7)
    assert Processes.Counter.value(c) == 7
  end

  test "Counter: a cast then a call from the same process is ordered" do
    {:ok, c} = Processes.Counter.start_link(0)
    assert Processes.Counter.bump(c, 3) == :ok
    assert Processes.Counter.bump(c, 4) == :ok
    # same sender, same receiver: both casts are queued before this call
    assert Processes.Counter.value(c) == 7
  end
end
