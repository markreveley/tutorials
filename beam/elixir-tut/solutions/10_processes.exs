ExUnit.start()

defmodule Processes do
  @moduledoc "Lesson 10: processes, messages, actors, GenServer."

  @doc """
  Spawn a process, send it a term, and wait for it to send the term back.
  Returns {:pong, term}, or :timeout if no reply arrives within 1000 ms.
  """
  def ping(term) do
    parent = self()

    pid =
      spawn(fn ->
        receive do
          {:ping, from, t} -> send(from, {:pong, t})
        after
          1_000 -> :ok
        end
      end)

    send(pid, {:ping, parent, term})

    receive do
      {:pong, t} -> {:pong, t}
    after
      1_000 -> :timeout
    end
  end

  @doc """
  Send every element of msgs to self() tagged {:drain, m}, then receive
  exactly that many messages back. The result equals msgs: per sender /
  receiver pair, message order is preserved.
  """
  def drain(msgs) do
    Enum.each(msgs, fn m -> send(self(), {:drain, m}) end)

    Enum.map(msgs, fn _ ->
      receive do
        {:drain, m} -> m
      after
        1_000 -> :timeout
      end
    end)
  end

  @doc """
  Map fun over xs in parallel, preserving order. Spawn all tasks first,
  then await them all.
  """
  def parallel_map(xs, fun) do
    xs
    |> Enum.map(fn x -> Task.async(fn -> fun.(x) end) end)
    |> Enum.map(fn t -> Task.await(t, 5_000) end)
  end

  @doc "Sum a list by folding updates into an Agent, then reading it."
  def sum_with_agent(xs) do
    {:ok, pid} = Agent.start_link(fn -> 0 end)
    Enum.each(xs, fn x -> Agent.update(pid, &(&1 + x)) end)
    total = Agent.get(pid, & &1)
    Agent.stop(pid)
    total
  end

  @doc """
  Run fun in a monitored process and return the reason it terminated
  (:normal for a clean exit). :timeout if nothing arrives within 1000 ms.
  """
  def down_reason(fun) do
    {pid, ref} = spawn_monitor(fun)

    receive do
      {:DOWN, ^ref, :process, ^pid, reason} -> reason
    after
      1_000 -> :timeout
    end
  end

  defmodule Counter do
    @moduledoc "A minimal GenServer: synchronous read, asynchronous write."
    use GenServer

    @doc "Start a counter holding n. Returns {:ok, pid}."
    def start_link(n), do: GenServer.start_link(__MODULE__, n)

    @doc "Read the counter synchronously."
    def value(pid), do: GenServer.call(pid, :value)

    @doc "Add k to the counter asynchronously. Returns :ok immediately."
    def bump(pid, k), do: GenServer.cast(pid, {:bump, k})

    @doc "Server callback: the initial state."
    @impl true
    def init(n), do: {:ok, n}

    @doc "Server callback: reply with the state, keep it unchanged."
    @impl true
    def handle_call(:value, _from, n), do: {:reply, n, n}

    @doc "Server callback: no reply, new state n + k."
    @impl true
    def handle_cast({:bump, k}, n), do: {:noreply, n + k}
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
