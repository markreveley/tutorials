# 03. Functions, Scope, Recursion

## Concept

`def` binds a name to a function object. `return` hands back a value;
falling off the end returns `None`.

```python
def area(w, h):
    return w * h

area(3, 4)          # positional
area(w=3, h=4)      # keyword — order-independent
area(3, h=4)        # mixed; positionals must come first
```

Parameter kinds, in the order they may appear:

```python
def f(pos, /, normal, kw_default=0, *args, kw_only, **kwargs):
    ...
```

- before `/`: positional-only (callers may not use the name)
- normal: positional or keyword
- `kw_default=0`: a default, used when the argument is omitted
- `*args`: a **tuple** of the surplus positional arguments
- after `*args` (or a bare `*`): keyword-only
- `**kwargs`: a **dict** of the surplus keyword arguments

The same stars unpack at the call site: `f(*seq)` spreads a sequence into
positional arguments, `f(**d)` spreads a dict into keyword arguments.

Functions are ordinary objects: assign them, pass them, return them, store
them in lists and dicts. `lambda params: expr` is an anonymous function
limited to a single expression — use it for a `key=` argument, not as a
way to avoid `def`.

```python
ops = {"+": lambda a, b: a + b, "*": lambda a, b: a * b}
ops["*"](3, 4)                       # 12
sorted(words, key=len)               # a function as data
```

A **closure** is a function that refers to a name from an enclosing
function that has already returned:

```python
def make_counter(start=0):
    n = start
    def tick():
        nonlocal n       # rebind the enclosing n, don't create a local
        n += 1
        return n
    return tick
```

## Why

### LEGB, and why assignment decides scope statically

A name is resolved by searching, in order:

    Local → Enclosing function(s) → Global (module) → Builtins

The rule that surprises people: **whether a name is local is decided at
compile time by whether the function body ever assigns to it**, not by
what has run.

```python
x = 1
def f():
    print(x)      # UnboundLocalError, not 1
    x = 2
```

`x = 2` anywhere in the body makes `x` local for the *whole* body, so the
`print` reads an unbound local. Why insist on this? Because the alternative
— decide at run time whether `x` means the global or a fresh local —
would make the meaning of a name depend on the execution path, so the same
line could denote different variables on different calls. Static scoping is
what lets you read a function and know, without running it, which binding
each name refers to. `global x` and `nonlocal x` are the explicit opt-outs;
they exist precisely because the default had to be unambiguous.

Note the asymmetry: *mutation* is not assignment. `lst.append(1)` needs no
declaration because it never rebinds `lst`; it mutates the object `lst`
already names (lesson 01's model, made concrete in lesson 04).

### Closures capture variables, not values

The inner function holds a reference to the enclosing *binding*, so it sees
later changes to it. Hence the classic bug:

```python
fs = []
for i in range(3):
    fs.append(lambda: i)
[f() for f in fs]          # [2, 2, 2] — one i, read after the loop
```

Fix by binding the value at definition time, via a default argument
(evaluated once, at `def` time): `lambda i=i: i` gives `[0, 1, 2]`.

### Recursion is induction

To prove `∀ n ∈ ℕ. P(n)` by induction you prove P(0), and P(k) ⇒ P(k+1).
To write a recursive function you write the base case, and the step that
builds the answer for n from the answer for k < n. **These are the same
act.** The recursive call *is* the appeal to the induction hypothesis:
inside the body you are permitted to assume the function already works on
smaller inputs, because that is exactly what the induction hypothesis
grants. Nothing else about the recursion has to be simulated in your head.

Three obligations, mirroring lesson 02's four:

1. **Base case correct** — the proof's base case.
2. **Step correct assuming the recursive calls are** — the induction step.
3. **Every call is on a strictly smaller input, under a well-founded
   order** — the termination argument, matching the loop's variant.

Omit (1) and there is no base for the induction and no bottom to the
recursion; the two failures are the same failure.

#### Proof A — factorial, simple induction

    def factorial(n):                 # precondition: n ≥ 0
        if n == 0:
            return 1
        return n * factorial(n - 1)

Claim: ∀ n ≥ 0, `factorial(n)` terminates and returns n!.

Base: n = 0 returns 1 = 0! by definition. ✓
Step: let n > 0 and assume `factorial(n-1)` returns (n−1)! (hypothesis;
legitimate because n−1 ≥ 0). The body returns n · (n−1)! = n!. ✓
Termination: the measure n is a natural number and strictly decreases (n →
n−1) at each call, so by well-ordering the chain of calls is finite. ∎

#### Proof B — sum of a list, structural induction

    def sum_list(xs):
        if not xs:
            return 0
        return xs[0] + sum_list(xs[1:])

Structural induction follows the *shape of the data*: a list is either
empty, or an element followed by a shorter list. One case per constructor.

Base: `xs == []` returns 0 = Σ over the empty list. ✓
Step: xs = [x₀] + rest. Assume the call on `rest` returns Σ rest
(legitimate: len(rest) = len(xs) − 1). The body returns x₀ + Σ rest =
Σ xs. ✓
Termination: the measure len(xs) strictly decreases. ∎

Correctness does not mean efficiency: `xs[1:]` copies, so this costs Θ(n²)
time and Θ(n) stack. Passing an index instead of slicing gives Θ(n).

#### Proof C — Fibonacci, strong induction

    def fib(n):                       # precondition: n ≥ 0
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

Here the step needs the hypothesis at *two* smaller points, one of which is
not n−1. Simple induction gives you only P(n−1); **strong** induction gives
you P(k) for all k < n, which is what this shape requires.

Base: n = 0 → 0 = F₀, n = 1 → 1 = F₁. ✓ (Two base cases, because the step
reaches back two steps; a proof needs a base for every position the step
cannot reach.)
Step: n ≥ 2, assume ∀ k < n. `fib(k)` = F_k. Then the body returns
F_{n−1} + F_{n−2} = F_n by the definition of the sequence. ✓
Termination: measure n, both calls strictly decrease it, and n ≥ 0 is
maintained since n ≥ 2 ⇒ n−2 ≥ 0. ∎

Cost: let T(n) be the number of calls. T(n) = T(n−1) + T(n−2) + 1, so
T(n) + 1 obeys the Fibonacci recurrence and T(n) = Θ(φⁿ) with
φ = (1+√5)/2. Exponential — because the same subproblem is recomputed. A
memo dict makes each n compute once, giving Θ(n) (lesson 12 names this
dynamic programming).

#### Proof D — binary recursion over a nested structure

    def flatten(xs):
        out = []
        for x in xs:
            if isinstance(x, list):
                out.extend(flatten(x))
            else:
                out.append(x)
        return out

The recursion branches, so induct on a measure that shrinks along every
branch: let s(xs) be the total number of list objects reachable from xs.
Each recursive call is on an element of xs, so s(x) < s(xs) strictly.

Claim: `flatten(xs)` returns the non-list leaves of xs in left-to-right
order. Induct strongly on s(xs).
Base: s = 1 (no nested lists) — the loop appends every element, in order. ✓
Step: assume the claim for all structures of smaller measure. The loop
maintains the invariant "`out` = the leaves of `xs[0..i)` in order": a
non-list element contributes itself; a list element x contributes
`flatten(x)`, which by the hypothesis is the leaves of x in order.
Concatenation of the per-element leaf sequences, in index order, is the
leaf sequence of xs. ✓ ∎

Note the two disciplines used together: induction across the recursion,
an invariant across the loop inside one call.

### Recursion depth is a resource limit, not a semantic one

Each call allocates a frame; CPython caps the chain at
`sys.getrecursionlimit()` (1000 by default) and raises `RecursionError`
past it. This guard exists because Python frames also consume the C stack,
and overflowing that would crash the interpreter rather than raise.

Python does **not** eliminate tail calls: `return f(...)` still grows the
stack. So a proof of termination does not imply the program runs — a
correct recursion of depth n needs Θ(n) stack. For n up to a few hundred,
recurse; for depth proportional to input size (a linked list of 10⁵ nodes,
say), convert to a loop with an explicit stack, which is what lesson 11
does for trees. Raising the limit is a last resort, not a fix.

## Worked examples

```python
>>> def f(a, b=2, *args, **kwargs):
...     return a, b, args, kwargs
>>> f(1)
(1, 2, (), {})
>>> f(1, 3, 4, 5, x=9)
(1, 3, (4, 5), {'x': 9})
>>> args = (1, 3); kw = {'x': 9}
>>> f(*args, **kw)
(1, 3, (), {'x': 9})
```

Defaults are evaluated once, at definition time — the same rule that
creates the mutable-default bug (lesson 04) makes `lambda i=i: i` work:

```python
>>> fs = [lambda i=i: i for i in range(3)]
>>> [f() for f in fs]
[0, 1, 2]
```

Closures as state, without a class:

```python
>>> tick = make_counter(10)
>>> tick(), tick(), tick()
(11, 12, 13)
>>> make_counter(10)()          # a fresh, independent cell
11
```

Functions returning functions:

```python
>>> def compose(f, g):
...     return lambda x: f(g(x))
>>> inc = lambda x: x + 1
>>> compose(inc, inc)(0)
2
```

Recursion depth, empirically:

```python
>>> import sys; sys.getrecursionlimit()
1000
>>> def depth(n): return 0 if n == 0 else 1 + depth(n - 1)
>>> depth(10000)
RecursionError: maximum recursion depth exceeded
```

## Exercises

Open `exercises/03_functions.py`; run `python3 -m pytest exercises/03_functions.py`.

- `apply_n(f, x, n)` — iterate a function n times; induction on n.
- `make_counter(start)` — a closure with `nonlocal` state.
- `compose(*funcs)` — variadic composition, identity when empty.
- `with_defaults(func, **defaults)` — fill in missing keyword arguments.
- `factorial(n)` — Proof A.
- `sum_list(items)` — Proof B, structural recursion.
- `fib(n, memo=None)` — Proof C, plus the mutable-default trap avoided.
- `flatten(nested)` — Proof D, branching recursion.

## LeetCode

- 509 Fibonacci Number — naive vs memoized; state the recurrence's cost.
- 70 Climbing Stairs — the same recurrence with different base cases.
- 50 Pow(x, n) — recursive fast power; strong induction on |n|.
- 344 Reverse String — recursion on a shrinking range, in place.
- 206 Reverse Linked List — write it recursively, then iteratively.
- 21 Merge Two Sorted Lists — structural induction on the two lists.
- 231 Power of Two — one-line recursion or a bit trick.
- 1137 N-th Tribonacci Number — three base cases; say why three.

## Next

Lesson 4 returns to data: lists and tuples, aliasing, and the mutation
rules that the "names bind to objects" model predicts.
