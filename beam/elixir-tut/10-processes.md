# 10 — Processes, messages, actors, GenServer

## Concept

An Elixir **process** is not an OS process and not a thread. It is a
BEAM-scheduled unit with its own heap and its own mailbox, costing a few
hundred bytes to start. A million of them on a laptop is unremarkable.

Three facts define everything else: a process's memory is **private**, so
no other process can read or write it; the only way to affect another
process is to **send it a message**, which copies the term into that
process's mailbox; and sending is **asynchronous** and never blocks, while
receiving blocks.

### spawn, send, receive, self

```elixir
iex> self()
#PID<0.110.0>

iex> pid = spawn(fn -> IO.puts("hi from #{inspect(self())}") end)
hi from #PID<0.115.0>
#PID<0.115.0>

iex> send(self(), {:hello, 42})
iex> receive do
...>   {:hello, n} -> n
...> end
42
```

`send/2` returns immediately, whether or not the target exists or ever
reads the message. `receive` scans the mailbox **in order** for the first
message matching any of its patterns, removes it, and runs that branch;
non-matching messages stay put. This is *selective receive*.

Always give `receive` an `after`:

```elixir
receive do
  {:result, v} -> v
after
  1_000 -> :timeout
end
```

Without it, a message that never arrives hangs the process forever. In a
test, a missing `after` is the difference between a red build and a hung
one.

The request/reply idiom sends your own pid so the other side can answer:

```elixir
parent = self()
pid = spawn(fn ->
  receive do
    {:square, from, n} -> send(from, {:squared, n * n})
  end
end)
send(pid, {:square, parent, 7})
receive do: ({:squared, v} -> v)      # 49
```

Note `parent = self()` *outside* the `fn`: inside the spawned function
`self()` is the new process. This is the single most common beginner bug.

### Links and monitors

```elixir
spawn_link(fn -> exit(:boom) end)     # my process dies too
{pid, ref} = spawn_monitor(fn -> exit(:boom) end)
receive do
  {:DOWN, ^ref, :process, ^pid, reason} -> reason     # :boom
end
```

A **link** is bidirectional: if either end dies abnormally, the other is
sent an exit signal and dies too (unless it traps exits). Links are how
supervision trees propagate failure — this is the mechanism behind "let it
crash" from lesson 8.

A **monitor** is unidirectional and non-invasive: you get a `{:DOWN, ref,
:process, pid, reason}` message and carry on. Links for parts of one
logical unit that should live and die together; monitors when you merely
want to *know*.

### Task — a process that computes one value

```elixir
iex> t = Task.async(fn -> Enum.sum(1..1_000_000) end)
iex> Task.await(t, 5_000)
500000500000

iex> 1..10 |> Task.async_stream(&(&1 * &1), max_concurrency: 4)
...>       |> Enum.map(fn {:ok, v} -> v end)
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

`Task.async/1` spawns a linked, monitored process; `Task.await/2` blocks
for its result and re-raises if it crashed. `Task.async_stream/3` is the
parallel `Enum.map`, and **preserves input order** regardless of
completion order.

### Agent — a process that holds one value

```elixir
iex> {:ok, pid} = Agent.start_link(fn -> 0 end)
iex> Agent.update(pid, &(&1 + 5))
:ok
iex> Agent.get(pid, & &1)
5
iex> Agent.stop(pid)
```

An Agent is state plus two operations with the process boilerplate hidden.
The function you pass runs *inside the agent process* — keep it small and
never let it raise.

### GenServer — the general case

`GenServer` is the standard behaviour for a stateful process: you write the
callbacks, OTP writes the receive loop, timeouts, and shutdown.

```elixir
defmodule Counter do
  use GenServer

  # ---- client API: runs in the CALLER's process ----
  def start_link(n), do: GenServer.start_link(__MODULE__, n)
  def value(pid), do: GenServer.call(pid, :value)          # synchronous
  def bump(pid, k), do: GenServer.cast(pid, {:bump, k})    # fire-and-forget

  # ---- callbacks: run in the SERVER's process ----
  @impl true
  def init(n), do: {:ok, n}

  @impl true
  def handle_call(:value, _from, n), do: {:reply, n, n}

  @impl true
  def handle_cast({:bump, k}, n), do: {:noreply, n + k}
end
```

```elixir
iex> {:ok, c} = Counter.start_link(0)
iex> Counter.bump(c, 3)     # :ok, immediately — may not have run yet
iex> Counter.value(c)       # 3 — see the ordering guarantee below
```

The split matters: `start_link/1`, `value/1`, `bump/2` run in the caller
and only send messages; `init/1`, `handle_call/3`, `handle_cast/2` run in
the server, one message at a time, with state threaded through their
return values. The state is an immutable term; the "mutation" is that the
server loops with a different term next time.

`call` blocks the caller (default timeout 5000 ms) and gives back-pressure;
`cast` gives none. Prefer `call` unless you measured a reason not to.

## Grounding: the actor model

The actor model (Hewitt 1973; Agha 1986) is a formal model of concurrency.
An actor is a triple:

```
actor  =  (state, behaviour, mailbox)
```

and on receiving a message an actor may do exactly three things:

```
1. send a finite number of messages to actors whose addresses it knows
2. create a finite number of new actors
3. designate the behaviour (and state) for the next message
```

Elixir implements this literally: (1) is `send/2`, (2) is `spawn/1`, (3) is
the return value of `handle_call`/`handle_cast`. Nothing else is available
— there is no shared variable to reach for.

### Data races are impossible by construction

**Definition.** A data race is two concurrent accesses to the same memory
location, at least one a write, with no ordering between them.

**Claim.** No Elixir program has a data race.

**Proof.** A location is either (a) inside some process's heap, or (b)
inside a message in transit. For (a): the only operations that touch
process P's heap are executed by P itself, and P executes its own
instructions sequentially, so any two accesses are ordered by program
order — no race. For (b): `send` copies the term into the receiver's
mailbox, so the sender's copy and the receiver's copy are distinct
locations; no location is accessed by both. In neither case do two
processes access one location. ∎

(The one exception is large binaries, which are reference-counted and
shared rather than copied — but they are immutable, so no access is a
write, and the definition is not met.)

This is a *structural* guarantee, not a discipline you maintain. Contrast
shared memory with locks, where correctness is a property of every call
site: forget one `lock()` and you get a race that appears once a month;
take two locks in different orders in two files and you get a deadlock that
neither file is wrong on its own. Those failure modes are non-local, so no
single function can be checked in isolation. Actor failures are local — a
message you did not handle, or a reply you did not wait for, is visible in
the process that made the mistake.

The price is honest: copying on send costs O(size of message), and
"isolated state" means read-mostly shared data has to be replicated,
routed through an owning process, or put in ETS. Message passing buys
safety, not free lunch.

### The ordering guarantee, exactly

The BEAM guarantees:

> If process A sends M1 to B and later sends M2 to B, then M1 arrives in
> B's mailbox before M2.

That is: **per sender–receiver pair, order is preserved (FIFO)**. This is
what makes `Counter.bump(c, 3)` then `Counter.value(c)` deterministic even
though `bump` is asynchronous — same sender, same receiver, so the cast
message is queued before the call message, and the server processes its
mailbox in order.

The BEAM does **not** guarantee:

- **Global ordering.** If A sends M1 to C and B sends M2 to C, C may see
  them in either order, no matter what wall-clock time they were sent at.
  There is no global clock and no total order on events; only the
  happens-before partial order exists.
- **Transitive ordering.** A sends M1 to C, then A sends M2 to B, then B
  sends M3 to C. M1 arrives before M2 (same pair), but M3 may reach C
  before M1 does — the path through B is a different pair.
- **Delivery.** `send` to a dead or unreachable pid is silently a no-op.
  If you need to know, use a monitor or a `call` with a timeout.

Every one of these is a real source of bugs, and every one of them is
resolved the same way: if you need an ordering, create a causal chain that
forces it (reply-then-send), or funnel the events through a single process
so that "arrival order at that process" *is* the order.

### What this buys you for leetcode: mostly nothing

Be honest about this. Leetcode problems are single-threaded algorithmic
puzzles with a sequential cost model. Processes give you:

- **No asymptotic improvement.** A parallel solution to an O(n²) problem is
  still O(n²) work; you have divided the wall clock by the core count at
  best, and Amdahl's law caps even that.
- **A real slowdown at small n.** Spawning and message-copying costs more
  than the work in almost every leetcode-sized input.
- **Nondeterminism you have to design away**, which is pure cost when the
  problem is deterministic.

Where they genuinely help:

- **Embarrassingly parallel maps** over independent subproblems — scoring
  each of many candidate answers, running a solver on each of many
  independent test inputs, brute-forcing a search space split by starting
  point. `Task.async_stream/3` with `max_concurrency` and `ordered: true`
  is the entire API you need.
- **Memoisation with a shared table** (an Agent or ETS) when several
  workers explore an overlapping DP space — though for one problem
  instance a map threaded through a fold is simpler and faster (lesson 12).
- **Abandoning a search on a timeout** — `Task.async` with `Task.yield/2`
  and `Task.shutdown/2`.

Learn this chapter because it is the point of Elixir and what "let it
crash" (lesson 8) rests on — not as a leetcode technique. Do not reach for
it in an interview unless concurrency is asked for by name.

## Worked examples

```elixir
# a process that keeps state by tail recursion — what GenServer wraps
defmodule Loop do
  def start(n), do: spawn(fn -> loop(n) end)

  defp loop(n) do
    receive do
      {:add, k} -> loop(n + k)
      {:get, from} -> send(from, {:value, n}); loop(n)
      :stop -> :ok
    end
  end
end

iex> p = Loop.start(0)
iex> send(p, {:add, 5}); send(p, {:get, self()})
iex> receive do: ({:value, v} -> v)
5
```

The state lives as an argument to a tail-recursive loop (lesson 5). There
is no mutable cell anywhere; "the counter changed" means "the next
iteration was called with a different term".

```elixir
# parallel map over independent subproblems, order preserved
iex> [[1,2,3], [4,5], [6]] |> Task.async_stream(&Enum.sum/1) |> Enum.map(fn {:ok, v} -> v end)
[6, 9, 6]

# draining your own mailbox demonstrates per-pair FIFO
iex> Enum.each([1, 2, 3], &send(self(), {:m, &1}))
iex> Enum.map(1..3, fn _ -> receive do: ({:m, v} -> v) end)
[1, 2, 3]
```

## Exercises

`exercises/10_processes.exs`. Every test must be deterministic: use an
explicit `receive ... after` or `Task.await/2`, never `Process.sleep/1`.
Hints:

- `ping/1`: bind `parent = self()` before `spawn`, have the child
  `receive` a `{:ping, from, term}` and reply `{:pong, term}`.
- `drain/1`: `send` each message to `self()` tagged, then `Enum.map` over
  the same list doing one `receive` per element. The result equals the
  input — that is the FIFO guarantee, observed.
- `parallel_map/2`: `Enum.map` to `Task.async`, then `Enum.map` to
  `Task.await`. Two passes, not one — one pass would await each task
  before starting the next and buy you nothing.
- `sum_with_agent/1`: `Agent.start_link`, fold `Agent.update`, read with
  `Agent.get`, then `Agent.stop`.
- `down_reason/1`: `spawn_monitor/1`, then `receive` the `{:DOWN, ref,
  :process, pid, reason}` message. Pin `ref` so you cannot match a stray
  DOWN from something else.
- `Processes.Counter`: three client functions and three callbacks, exactly
  as in the `Counter` example above.

## Leetcode at this stage

Nothing here changes what you can solve; see the honest assessment above.
If you want to exercise it anyway, take a problem you have already solved
and parallelise the *outer* loop:

- 200 Number of Islands — flood-fill each candidate start in parallel and
  merge, once you have the sequential version from lesson 12.
- Any brute-force problem — split the search space by first element and
  `Task.async_stream` the pieces.

Questions before moving on:

1. Why does `parent = self()` have to be outside the `spawn` closure?
2. A casts to a server then calls it. Why is the call guaranteed to see
   the cast's effect? Which guarantee is doing the work, and what breaks
   if a *different* process sends the cast?
3. State the data-race proof in your own words. Where exactly does the
   "large binaries are shared" caveat fail to break it?
