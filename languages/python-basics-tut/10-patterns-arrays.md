# 10. LeetCode Patterns I: Arrays

Four patterns cover most array problems: two pointers, sliding window,
prefix sums, and in-place rearrangement. Each one is a loop, so each one is
justified the same way — by an invariant (lesson 02) — and each one carries
a cost obligation (lesson 09). A pattern you can code but cannot justify is
a memorized trick; it fails the moment the problem shifts.

The recipe, every time:

1. Name the state (the pointers, the accumulator).
2. Write the invariant P: what is true of the state before each iteration.
3. Check initialization (P holds before the loop), preservation (the body
   restores P), and termination (a measure strictly decreases, and
   P ∧ exit-condition ⇒ the postcondition).
4. State the bound and why.

## Pattern 1 — Two pointers from opposite ends

**Shape.** `lo = 0; hi = n-1`; each iteration examines `(a[lo], a[hi])` and
moves exactly one pointer inward. Requires a monotone structure — usually a
sorted array — that makes the discarded side provably useless.

### Two Sum on a sorted array

```python
def two_sum_sorted(a, target):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        s = a[lo] + a[hi]
        if s == target:
            return (lo, hi)
        if s < target:
            lo += 1
        else:
            hi -= 1
    return None
```

**Invariant P.** If any pair (i, j) with i < j and a[i] + a[j] = target
exists in the whole array, then one exists with lo ≤ i < j ≤ hi.

*Initialization.* lo = 0, hi = n−1: the range is everything. ✓

*Preservation.* Suppose P holds and a[lo] + a[hi] < target. For every
j ≤ hi, sortedness gives a[j] ≤ a[hi], hence
a[lo] + a[j] ≤ a[lo] + a[hi] < target. So lo pairs with nothing in
[lo+1, hi]; any surviving solution avoids index lo, and P still holds with
lo+1. The case `> target` is symmetric on hi. ✓

*Termination.* hi − lo strictly decreases each iteration and the loop stops
at hi − lo ≤ 0. On exit the range holds fewer than two indices, so by P no
pair exists anywhere — returning None is correct. ✓

**Cost.** Each iteration does O(1) work and decreases hi − lo by 1 from
n−1, so at most n−1 iterations: Θ(n) time, Θ(1) auxiliary space.

### Container With Most Water

Same shape, different discard lemma.

**Lemma.** If h[lo] ≤ h[hi], then for every j with lo < j < hi,
area(lo, j) ≤ area(lo, hi).

*Proof.* area(lo, j) = (j − lo)·min(h[lo], h[j]) ≤ (j − lo)·h[lo]
≤ (hi − lo)·h[lo] = (hi − lo)·min(h[lo], h[hi]) = area(lo, hi). ∎

So once `lo` has been paired with `hi`, no *unexamined* pair involving `lo`
can beat it, and `lo` may be discarded.

**Invariant.** `best` = the maximum area over all pairs already discarded or
examined, and every pair not yet accounted for has both endpoints in
[lo, hi]. At exit the range holds no pairs, so `best` is the global maximum.
Θ(n) time, Θ(1) space.

## Pattern 2 — Fast and slow pointers

Two pointers moving through the *same* sequence at different rates.

- **Middle of a list**: `slow` advances 1, `fast` advances 2. Invariant:
  after k steps, slow is at index k and fast at 2k. When fast runs off the
  end, k = ⌊n/2⌋. One pass, Θ(1) space, no length needed in advance.
- **Cycle detection (Floyd)**: if the sequence enters a cycle of length λ
  after a tail of length μ, then slow and fast meet. *Proof.* Once both are
  inside the cycle (after at most μ + λ steps), the gap fast − slow, taken
  mod λ, increases by exactly 1 per step, so within λ further steps it hits
  0 — a meeting. If there is no cycle, fast reaches the end in ⌈n/2⌉ steps.
  Either way Θ(n) time, Θ(1) space.
- **Write pointer** (a fast/slow pair over an array): the read pointer scans
  and the write pointer trails, compacting in place. See pattern 5.

## Pattern 3 — Sliding window

The window is a contiguous range `a[lo..hi)`. Instead of recomputing a
summary for each of the Θ(n²) ranges, maintain it incrementally: adding
a[hi] and removing a[lo] must each be O(1).

### Fixed size k

```python
def max_sum_window(a, k):
    s = sum(a[:k])
    best = s
    for hi in range(k, len(a)):
        s += a[hi] - a[hi - k]      # add the entrant, remove the leaver
        best = max(best, s)
    return best
```

**Invariant.** At the top of iteration `hi`, `s == sum(a[hi-k .. hi))` and
`best == max over all windows ending at or before hi`. Preservation is one
addition and one subtraction; the algebra `sum(a[i+1..j+1)) =
sum(a[i..j)) + a[j] − a[i]` is the whole proof. Θ(n) time, Θ(1) space.

### Variable size

Grow `hi` unconditionally; shrink `lo` while the window violates (or
over-satisfies) the property. Two templates:

```python
# longest window satisfying P (shrink while invalid)
lo = 0
for hi in range(n):
    add(a[hi])
    while not valid():
        remove(a[lo]); lo += 1
    best = max(best, hi - lo + 1)

# shortest window satisfying P (shrink while still valid)
lo = 0
for hi in range(n):
    add(a[hi])
    while valid():
        best = min(best, hi - lo + 1)
        remove(a[lo]); lo += 1
```

**Invariant (longest form).** At the bottom of iteration hi: the window
a[lo..hi] is valid, and no valid window ending at hi starts before lo —
so `hi − lo + 1` is the longest valid window ending at hi. Since every
window ends *somewhere*, taking the max over hi gives the global answer.
The second claim needs monotonicity of P: **if a[lo..hi] is invalid then so
is a[lo'..hi] for every lo' ≤ lo** (shrinking is the only thing that can
restore validity). Check that this holds for your P before reaching for the
pattern — it is true for "all characters distinct" and "sum ≥ target on
non-negative numbers", and false for "sum ≥ target with negatives", which
is why Shortest Subarray with Sum at Least K needs a deque, not a window.

### Why the variable window is Θ(n), not Θ(n²)

The nested `while` looks quadratic. It is not — the accounting method of
lesson 09 applies.

**Claim.** The body of the inner `while` executes at most n times in total
across the whole run.

*Proof.* `lo` is initialized to 0, never decreases, is incremented exactly
once per inner-loop body, and satisfies lo ≤ n at all times (it never
passes hi + 1 ≤ n). So the number of increments — hence the number of inner
iterations over the entire run — is at most n. ∎

Charge each outer iteration an amortized 2 units: 1 for its own O(1) work,
1 banked to pay for the eventual removal of the element it added. Every
removal is funded by the credit its insertion left behind. Total work
≤ 2n·O(1) = Θ(n). Each element is added exactly once and removed at most
once: **Θ(n) time**, and Θ(1) or Θ(alphabet) space depending on the summary
you maintain.

## Pattern 4 — Prefix sums

Define P[0] = 0 and P[i+1] = P[i] + a[i]. Then

    P[i] = Σ_{t<i} a[t]     and     sum(a[i..j)) = P[j] − P[i]

*Proof.* By induction on i, P[i] = Σ_{t<i} a[t]. Then
P[j] − P[i] = Σ_{t<j} a[t] − Σ_{t<i} a[t] = Σ_{i ≤ t < j} a[t]. ∎

Θ(n) preprocessing buys Θ(1) range-sum queries. Two standard uses:

**Counting subarrays with a given sum.** sum(a[i..j)) = k ⇔ P[j] − P[i] = k
⇔ P[i] = P[j] − k. So sweep j, and maintain a dict `seen` with the
invariant `seen[v] == #{ i ≤ j : P[i] == v }`. At step j add
`seen[P[j] − k]` to the answer — exactly the number of valid starts. One
pass, Θ(n) expected time, Θ(n) space. Note this works with negative
numbers, where the sliding window does not.

**Products instead of sums.** Product-Except-Self replaces + with ×: the
answer is prefix-product × suffix-product. Since × has no inverse over ints
containing 0, you cannot divide the total — you compute both directions.
Writing the prefix into the output array and then sweeping backwards with a
running suffix gives Θ(1) auxiliary space (the output does not count).

**Kadane** is the prefix idea reduced to O(1) state. Let `cur` be the
maximum sum of a subarray ending exactly at i. Then

    cur(i) = max(a[i], cur(i-1) + a[i])

because such a subarray either is just a[i] or extends the best one ending
at i−1 — and extending a *worse* one ending at i−1 could never be better.
Invariant: after processing i, `cur == cur(i)` and `best == max(cur(t) for
t ≤ i)`. Every non-empty subarray ends somewhere, so `best` is the answer.
Θ(n) time, Θ(1) space.

## Pattern 5 — In-place rearrangement

The write-pointer template. Read with `i`, write with `w ≤ i`; because the
write pointer never overtakes the read pointer, no unread element is
clobbered.

```python
def move_zeroes(a):
    w = 0
    for i in range(len(a)):
        if a[i] != 0:
            a[w], a[i] = a[i], a[w]
            w += 1
```

**Invariant.** Before iteration i: `a[0..w)` holds the non-zero elements of
the original `a[0..i)` in their original relative order, and `a[w..i)` holds
only zeros; the multiset a[0..i) is unchanged.

*Preservation.* If a[i] == 0 the zero-block grows by one and w is unchanged.
✓ Otherwise the swap moves a[i] to position w; the value it displaces is
a[w], which by the invariant is 0 (or is a[i] itself when w == i), so it
lands in the zero-block. Both clauses hold with w+1, i+1. ✓

*Termination.* i reaches n; then a[0..w) is every non-zero element in order
and a[w..n) is all zeros. ∎ Θ(n) time, Θ(1) space, and each element is
touched a constant number of times.

Same template: Remove Duplicates from Sorted Array, Remove Element,
Sort Colors (three pointers: `lo`, `i`, `hi`, with the invariant
a[0..lo) = 0s, a[lo..i) = 1s, a[hi..n) = 2s), and reverse-in-place
(swap `a[i]` and `a[n-1-i]` for i < n/2 — note the loop bound: running to n
would undo every swap).

## Choosing a pattern

| Signal in the problem                          | Reach for              |
|------------------------------------------------|------------------------|
| sorted array, find a pair/triple               | two pointers, opposite ends |
| linked list, cycle or midpoint                 | fast/slow              |
| "contiguous subarray/substring", non-negative  | sliding window         |
| "contiguous", may be negative, count or sum    | prefix sums + dict     |
| "in place", "O(1) extra space", partitioning   | write pointer          |
| best subarray sum ending anywhere              | Kadane                 |

If the array is unsorted and the answer is order-insensitive, sorting first
costs Θ(n log n) and often unlocks two pointers — a fine trade when the
alternative is Θ(n²).

## Exercises

Open `exercises/10_patterns_arrays.py`; run `python3 -m pytest exercises/10_patterns_arrays.py`.

- `two_sum_sorted(a, target)` — opposite ends; the discard lemma above.
- `container_with_most_water(heights)` — opposite ends; the area lemma.
- `longest_substring_without_repeating(s)` — variable window, shrink while invalid.
- `min_subarray_len(target, nums)` — variable window, shrink while valid.
- `product_except_self(nums)` — prefix × suffix, Θ(1) auxiliary space.
- `move_zeroes(nums)` — write pointer, in place, returns None.
- `max_subarray(nums)` — Kadane, with the invariant in the docstring.
- `subarray_sum_equals_k(nums, k)` — prefix sums plus a counting dict.

Each docstring states the required bound. A solution that returns the right
answer outside its bound does not count as done.

## LeetCode

- 167 Two Sum II — Input Array Is Sorted — pattern 1, verbatim.
- 11 Container With Most Water — pattern 1 with the area lemma.
- 15 3Sum — sort, fix i, then pattern 1 on the suffix; Θ(n²).
- 141 / 142 Linked List Cycle (II) — Floyd; part II needs the μ, λ algebra.
- 3 Longest Substring Without Repeating Characters — variable window.
- 209 Minimum Size Subarray Sum — variable window, shortest form.
- 424 Longest Repeating Character Replacement — window plus a frequency table.
- 76 Minimum Window Substring — the hardest standard window; two counters.
- 560 Subarray Sum Equals K — prefix sums + dict; negatives allowed.
- 238 Product of Array Except Self — prefix × suffix, no division.
- 53 Maximum Subarray — Kadane.
- 283 Move Zeroes, 26 Remove Duplicates, 75 Sort Colors — write pointers.
- 152 Maximum Product Subarray — Kadane with two accumulators (min and max);
  work out why one is not enough.

## Next

Lesson 11 moves from linear scans to recursive structure: trees, traversal
orders, and correctness by induction rather than by invariant.
