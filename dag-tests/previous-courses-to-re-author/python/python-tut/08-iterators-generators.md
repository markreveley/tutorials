# 08. Iterators, Generators, and Laziness

## Concept

### The iterator protocol

Two methods and one exception define the whole thing.

```python
it = iter(obj)     # calls obj.__iter__(); returns an iterator
next(it)           # calls it.__next__(); returns the next item
                   # raises StopIteration when there are none left
```

An **iterable** is any object with `__iter__`. An **iterator** is an object
with `__next__` *and* an `__iter__` that returns `self`. Lists, strings,
dicts, sets, and files are iterables; the objects `iter()` hands back are
iterators. The distinction matters: an iterable can be walked many times,
an iterator exactly once.

```python
xs = [1, 2, 3]
iter(xs) is iter(xs)        # False — a fresh iterator each time
it = iter(xs)
iter(it) is it              # True  — an iterator is its own iterable
list(it), list(it)          # ([1, 2, 3], []) — exhausted after one pass
```

### The for loop, desugared

```python
for x in obj:
    body
else:
    tail
```

is exactly

```python
_it = iter(obj)
while True:
    try:
        x = next(_it)
    except StopIteration:
        tail            # the else-clause runs only on normal exhaustion
        break
    body                # a break here skips the else-clause
```

Everything that "works in a for loop" works because it supplies `__iter__`.
`sum`, `max`, `list`, `in`, tuple unpacking, `zip` — all of them do exactly
the above.

### Generators

A function containing `yield` is a **generator function**. Calling it runs
no code; it builds a generator object.

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

g = countdown(3)      # nothing has run yet
next(g)               # 3   — runs up to the first yield, then suspends
next(g)               # 2   — resumes after the yield with n still bound
next(g), next(g)      # 1, then StopIteration
```

`yield` suspends: it saves the instruction pointer and the local frame and
returns a value to the caller. `next` resumes from that point. Falling off
the end (or `return`) raises `StopIteration`. `yield from sub` delegates:
it yields every item `sub` produces.

### Generator expressions and comprehensions

```python
[x * x for x in range(5)]              # list        [0, 1, 4, 9, 16]
{x * x for x in range(5)}              # set
{x: x * x for x in range(5)}           # dict
(x * x for x in range(5))              # generator — nothing computed yet
sum(x * x for x in range(5))           # bare genexp as a sole argument
```

Filters and nesting read left to right, in the same order as the loops they
replace:

```python
[(i, j) for i in range(3) for j in range(i) if (i + j) % 2 == 0]
```

The loop variable lives in the comprehension's own scope; it does not leak.

### Infinite sequences

Laziness makes unbounded producers ordinary values.

```python
def naturals(start=0):
    n = start
    while True:
        yield n
        n += 1

from itertools import islice
list(islice(naturals(), 5))        # [0, 1, 2, 3, 4]
```

### itertools essentials

    count(start, step)      infinite arithmetic sequence
    cycle(iterable)         repeat forever (buffers a copy)
    repeat(x, n)            x, n times (forever if n omitted)
    islice(it, stop)        slice an iterator; islice(it, start, stop, step)
    chain(a, b, ...)        concatenate; chain.from_iterable(iters)
    accumulate(it, f)       running fold — prefix sums by default
    pairwise(it)            (a0,a1), (a1,a2), ...          (3.10+)
    groupby(it, key)        runs of equal keys — sort first if you want groups
    product/permutations/combinations   the obvious enumerations
    zip(a, b)               parallel walk, stops at the shortest

## Why

### Laziness is call-by-need, at the granularity of elements

Three evaluation disciplines for an argument:

- **Call-by-value**: evaluate once, before the call. A list comprehension.
- **Call-by-name**: re-evaluate at each use. A zero-argument function.
- **Call-by-need**: evaluate at first use, then reuse the result.

A generator is call-by-need over a *sequence*: element k is computed when
it is first demanded, and never recomputed, because the consumer holds the
value it received. Consequences:

1. Elements never demanded are never computed. `next(x for x in xs if p(x))`
   stops at the first hit.
2. The producer need not terminate; only the consumer must.
3. A generator is single-pass. Unlike a lazy list in Haskell, it memoizes
   nothing — the spine is consumed as it is produced. Need two passes?
   Materialize a list, or use `itertools.tee`.

### A generator is a suspended computation

Formally: a generator object is a triple (code, frame, state) where the
frame holds the locals and the instruction pointer, and state ∈ {created,
suspended, running, closed}. `next(g)` transitions suspended → running,
executes until the next `yield` (back to suspended, emitting a value) or
until the code returns (→ closed, raising `StopIteration`). This is a
first-class *continuation of a restricted shape*: it can be resumed, but
only once and only from where it stopped.

That is why the frame's locals are the generator's entire state, and why
the state is O(size of the frame) — a constant determined by the source
text, not by how many items it will produce.

### A pipeline runs in O(1) space; the eager version needs Θ(n)

Compare, for input `range(n)`:

```python
# eager
squares = [x * x for x in range(n)]
evens   = [y for y in squares if y % 2 == 0]
total   = sum(evens)

# lazy
squares = (x * x for x in range(n))
evens   = (y for y in squares if y % 2 == 0)
total   = sum(evens)
```

**Claim.** The lazy version uses O(1) auxiliary space; the eager version
uses Θ(n).

*Eager.* After statement 1, `squares` holds n int objects simultaneously —
every one is reachable from the list until `squares` dies. So peak live
memory ≥ n words, and it is Θ(n).

*Lazy.* Let the pipeline have k stages (here k = 3, fixed by the program
text, independent of n). Model the state after any `next` call on the last
stage: each stage i is a generator whose frame contains a bounded number of
locals — its loop variable, its reference to stage i−1, and O(1) temporaries
— say at most c words. No stage holds a container. At most one value is in
flight per stage, since a stage yields a value only after consuming one and
retains no history.

By induction on i: stage 1 (`range`) stores start/stop/step, O(1). If
stages 1..i−1 occupy O(1) together, stage i adds at most c words and drops
each consumed value before requesting the next, so stages 1..i occupy O(1).
The consumer `sum` keeps one accumulator. Total ≤ k·c + O(1) = O(1). ∎

The catch: this holds only if no stage buffers. `sorted`, `list`, `len`,
`reversed`, and `random.shuffle` all force the whole sequence and restore
the Θ(n). Laziness is a property of a *chain*, and one eager link breaks it.

### When a comprehension beats a loop

Use a comprehension when the loop body is a single expression appended to
one new container and has no side effects. It is clearer, it does not leak
the loop variable, and CPython emits a specialized append that skips the
attribute lookup a manual `result.append(...)` performs.

Use a loop when you need early exit (`break`), several outputs, statements
with side effects, or a body long enough that reading it left to right
stops being a help. Never write a comprehension for its side effects and
throw the list away — that allocates n items to produce nothing.

Use a *generator* expression, not a list comprehension, whenever the result
feeds straight into `sum`, `min`, `max`, `any`, `all`, `join`, or a `for`.
`any(p(x) for x in xs)` short-circuits; `any([p(x) for x in xs])` evaluates
p on every element first.

## Worked examples

```python
>>> def logged(n, log):
...     for i in range(n):
...         log.append(i)
...         yield i
...
>>> log = []
>>> next(x for x in logged(1000, log) if x > 2)   # stops at the first hit
3
>>> log                                            # only 4 items produced
[0, 1, 2, 3]
```

A hand-written iterator class, and the same thing as a generator:

```python
class Countdown:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return self                 # this object IS the iterator
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

def countdown(n):                   # 4 lines instead of 9, and restartable
    while n > 0:                    # per call
        yield n
        n -= 1
```

Prefix sums, lazily, and a sliding window over a stream:

```python
>>> from itertools import accumulate, islice, tee
>>> list(accumulate([3, 1, 4, 1, 5]))
[3, 4, 8, 9, 14]

>>> def windows(it, k):
...     from collections import deque
...     w = deque(maxlen=k)
...     for x in it:
...         w.append(x)
...         if len(w) == k:
...             yield tuple(w)
...
>>> list(windows(range(5), 3))
[(0, 1, 2), (1, 2, 3), (2, 3, 4)]
```

Space: `windows` holds k items, never n — the deque's `maxlen` evicts.

The exhaustion trap, which costs people whole debugging sessions:

```python
>>> g = (x for x in range(3))
>>> 1 in g, 1 in g            # the first `in` consumed 0 and 1
(True, False)
>>> total, biggest = sum(g), max(g)   # ValueError: max() arg is empty
```

## Exercises

Open `exercises/08_iterators.py`; run `python3 -m pytest exercises/08_iterators.py`.

- `manual_iterate(iterable)` — the for loop, written out with `iter`/`next`/`StopIteration`.
- `Countdown` — a class implementing the iterator protocol directly.
- `take(iterable, k)` — first k items, consuming exactly k; must work on infinite iterators.
- `evens()` — an infinite generator.
- `running_max(iterable)` — lazy prefix maxima, one pass, O(1) state.
- `unique_everseen(iterable)` — first occurrences, in order, lazily.
- `chunk(iterable, size)` — fixed-size blocks, last one possibly short.
- `sum_of_squares_of_evens(iterable)` — a pipeline in O(1) space.

## LeetCode

- 341 Flatten Nested List Iterator — `__next__`/`hasNext` over a stack; `yield from` writes it in four lines.
- 284 Peeking Iterator — one item of lookahead; the state machine of a suspended generator, by hand.
- 251 Flatten 2D Vector — nested iteration, lazily.
- 173 Binary Search Tree Iterator — in-order traversal as a generator; O(h) space.
- 1286 Iterator for Combination — `itertools.combinations` is the reference; write it yourself.
- 900 RLE Iterator — decode a run-length stream without materializing it.
- 604 Design Compressed String Iterator — same idea, character-wise.
- 1885 Count Pairs in Two Arrays — sort plus two pointers, fed by a genexp (previews lesson 10).

## Next

Lesson 09 turns "this is fast" into an obligation you can discharge: O, Θ,
Ω defined precisely, amortized analysis, and the cost of every CPython
operation you have been using.
