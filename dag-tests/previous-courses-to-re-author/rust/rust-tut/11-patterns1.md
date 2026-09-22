# 11. Patterns I — Two Pointers, Windows, Prefix Sums, Hashing, Binary Search

## Concept

Five array patterns. Each one is a loop, so each one is a choice of invariant.
The template is always the same three obligations:

1. **Establishment** — the invariant holds before the first iteration.
2. **Preservation** — if it holds at the top of an iteration, it holds at the
   bottom.
3. **Termination + exit** — some measure strictly decreases toward a bound, and
   the invariant together with the exit condition implies the postcondition.

State the invariant before you write the loop body. Then state the cost.

### Two pointers, opposite ends

```rust
let (mut lo, mut hi) = (0usize, xs.len() - 1);
while lo < hi {
    // decide, then move exactly one of lo, hi inward
}
```

Measure: `hi - lo`, strictly decreasing, bounded below by 0 ⇒ ≤ n iterations,
O(n). Used when the array is sorted, or when the objective depends only on
`min(xs[lo], xs[hi])` and the width.

### Two pointers, same direction (read/write, or fast/slow)

```rust
let mut w = 0;                       // write cursor
for r in 0..xs.len() { ... }         // read cursor
```

Invariant: `xs[0..w]` is the answer built from `xs[0..r]`. Since `w ≤ r`, the
write never overtakes the read, so in-place compaction is safe.

Floyd's fast/slow is the same idea on a functional graph `i ↦ next(i)`: the hare
moves two steps per tortoise step, so if a ρ-shape exists they meet.

### Sliding window

```rust
let mut lo = 0;
for hi in 0..n {
    // extend the window with xs[hi]
    while /* window is invalid or improvable */ {
        // shrink from lo
        lo += 1;
    }
    // record the answer for the window xs[lo..=hi]
}
```

Fixed width k: no inner loop, just `sum += xs[hi] - xs[hi - k]`.
Variable width: the inner `while` looks like it makes this O(n²). It does not —
see the amortisation argument below.

### Prefix sums

`p[0] = 0`, `p[i+1] = p[i] + xs[i]`. Then for all `0 ≤ l ≤ r ≤ n`:

    Σ xs[l..r] = p[r] − p[l]

O(n) preprocessing buys O(1) range sums. Immediately gives the hashing trick:
a subarray `[l, r)` sums to k **iff** `p[l] = p[r] − k`, so counting subarrays
with sum k is counting, for each r, how many earlier prefixes equal `p[r] − k`.

### Hashing

`HashMap` converts "have I seen a value that would complete this?" from an O(n)
rescan into an O(1) expected lookup, turning O(n²) pair-hunting into O(n).
Two shapes: complement lookup (Two Sum), and canonical-key grouping (anagrams).

### Binary search on a monotone predicate

Do not memorise index arithmetic. Memorise this: binary search finds the
**boundary** of a monotone Boolean predicate over `0..=n`.

```rust
let (mut lo, mut hi) = (0usize, xs.len());   // half-open [lo, hi)
while lo < hi {
    let mid = lo + (hi - lo) / 2;
    if !p(mid) { lo = mid + 1 } else { hi = mid }
}
lo   // the least i with p(i), or n
```

`p(i) = xs[i] >= target` gives lower bound; `p(i) = xs[i] > target` gives upper
bound; `upper − lower` is the multiplicity of `target`.

## Why

### Why the half-open formulation, and a full proof

Fix a slice `xs` of length n, sorted ascending, and a predicate
`p : {0,…,n−1} → Bool` that is **monotone**: `p(i) ⇒ p(j)` for all `j > i`.
Extend it with `p(n) = true` by convention. Define

    ANS = min { i ∈ [0, n] : p(i) }        (well-defined: p(n) = true)

Claim: the loop above returns ANS.

**Invariant.** I ≡ `0 ≤ lo ≤ hi ≤ n` ∧ `(∀ i < lo. ¬p(i))` ∧ `(p(hi) ∨ hi = n)`.

Read it as: everything strictly left of `lo` is known false, and `hi` is known
true (or is the sentinel). Hence `lo ≤ ANS ≤ hi` at all times.

**Establishment.** `lo = 0`, `hi = n`. The ∀ clause quantifies over the empty
set, so it is vacuously true. The third clause holds because `hi = n`. ∎

**Preservation.** Assume I and `lo < hi`. Let `mid = lo + ⌊(hi − lo)/2⌋`.

First, `lo ≤ mid < hi`. Let `d = hi − lo ≥ 1`. Then `mid = lo + ⌊d/2⌋ ≥ lo`, and
`⌊d/2⌋ ≤ d − 1` whenever `d ≥ 1` (for d = 1, ⌊1/2⌋ = 0 = d − 1; for d ≥ 2,
⌊d/2⌋ ≤ d/2 ≤ d − 1), so `mid ≤ hi − 1 < hi`. In particular `mid` is a legal
index into `xs`, since `mid < hi ≤ n`.

- Case `¬p(mid)`: set `lo' = mid + 1`. Monotonicity contrapositive: `¬p(mid)`
  and `i ≤ mid` ⇒ `¬p(i)` (otherwise `p(i)` with `i ≤ mid` would force
  `p(mid)`). Combined with the old ∀ clause, `∀ i < lo'. ¬p(i)`. And
  `lo' = mid + 1 ≤ hi`, so `lo' ≤ hi'` with `hi' = hi`. I holds.
- Case `p(mid)`: set `hi' = mid`. Then `p(hi')` holds directly, and
  `lo ≤ mid = hi'`. The ∀ clause is untouched. I holds. ∎

**Termination.** The measure is `μ = hi − lo ∈ ℕ`. In case 1,
`μ' = hi − (mid + 1) < hi − mid ≤ hi − lo = μ`. In case 2,
`μ' = mid − lo < hi − lo = μ` because `mid < hi`. So μ strictly decreases and is
bounded below by 0; the loop terminates.

Sharper: `μ' ≤ ⌈μ/2⌉` in both cases. Case 2 gives `μ' = ⌊μ/2⌋ ≤ ⌈μ/2⌉`; case 1
gives `μ' = μ − ⌊μ/2⌋ − 1 = ⌈μ/2⌉ − 1`. Starting from `μ₀ = n`, after k
iterations `μ ≤ ⌈n/2ᵏ⌉`, which reaches 0 at `k = ⌈log₂(n+1)⌉`. So the loop runs
Θ(log n) times, each iteration O(1) ⇒ **O(log n) time, O(1) space**. ∎

**Postcondition.** On exit `lo = hi` (we never overshoot: `lo' ≤ hi` and
`hi' ≥ lo`). I then says `∀ i < lo. ¬p(i)` and `p(lo) ∨ lo = n`. The first
clause says ANS ≥ lo; the second says ANS ≤ lo. Hence `lo = ANS`. ∎

Three things the half-open form buys, and the closed form `[lo, hi]` does not:

- `hi = n` is expressible, so "no element satisfies p" needs no sentinel value
  or special case — the answer is just `n`.
- The loop condition is `lo < hi`, not `lo <= hi`, so there is no off-by-one in
  the exit test and no `hi = mid - 1` underflow when `mid = 0` and `hi: usize`.
  (In Rust that underflow *panics* in debug and wraps to `usize::MAX` in
  release. Both are bugs; the half-open form makes them unreachable.)
- The result is directly an insertion point, which is what `Vec::binary_search`
  returns in its `Err` arm, and what every "count of elements < x" question
  wants.

Also note `mid = lo + (hi − lo) / 2`, never `(lo + hi) / 2`: the latter can
overflow for large indices. In Rust that is a debug panic rather than silent
corruption, but write the safe form anyway.

### Why the variable sliding window is O(n), not O(n²)

The code has a `for` over `hi` containing a `while` that advances `lo`. The
naive bound is O(n) × O(n) = O(n²). The true bound is O(n), by amortisation.

Take the potential Φ = `lo`. Observations:

1. `lo` never decreases — no line in the pattern assigns it a smaller value.
2. `lo ≤ hi + 1 ≤ n` always, so `Φ ∈ [0, n]`.
3. Every execution of the inner loop body increments `lo`, i.e. increases Φ by
   exactly 1.

Let T be the total number of inner-loop body executions over the whole run. By
(3), T equals the total increase of Φ. By (1) and (2), the total increase is at
most `n − 0 = n`. So **T ≤ n**. The outer loop contributes n iterations, each
O(1) outside the inner body. Total O(n) time. ∎

The same argument covers the monotonic deque of lesson 09 (each index is pushed
once and popped at most once ⇒ ≤ 2n deque operations) and the read/write
compaction pointer.

Warning: `min_subarray_len` shrinks while `sum >= target`, which is only a
correct stopping rule when all values are non-negative — otherwise extending
the window can *decrease* the sum and the monotonicity that justifies never
moving `lo` back is lost. State the precondition; it is part of the invariant.

### Why the opposite-ends move is not greedy nonsense (LC 11)

Container With Most Water. Area of the pair `(lo, hi)` is
`(hi − lo) · min(h[lo], h[hi])`. Invariant: **some optimal pair lies within
`[lo, hi]`**.

Establishment: `[0, n−1]` contains every pair.
Preservation: suppose `h[lo] ≤ h[hi]` and we advance `lo`. Any pair
`(lo, j)` with `j < hi` has width `j − lo < hi − lo` and height
`min(h[lo], h[j]) ≤ h[lo] = min(h[lo], h[hi])`, so its area is ≤ the area of
`(lo, hi)`, which we already recorded. Therefore discarding all pairs anchored
at `lo` loses nothing, and an optimum still lies in `[lo+1, hi]`. ∎
Exit: `lo = hi`, the interval holds no pair, and the optimum was recorded at the
moment it was discarded. Cost: each iteration moves one pointer ⇒ O(n) time,
O(1) space.

### Why hashing turns O(n²) into O(n)

Two Sum's brute force asks, for each j, "does some i < j have
`nums[i] = target − nums[j]`?" — an O(j) scan. Maintaining a `HashMap` from
value to index makes that question O(1) expected. The invariant is exactly
"`seen` contains every value in `nums[0..j]`", established empty and preserved
by inserting `nums[j]` at the end of iteration j. Insert *after* the lookup, or
you will match an element with itself. Expected O(n) time, O(n) space — the
space is the price of the speedup, and you must state it.

## Worked examples

```rust
// Prefix sums: one identity, two applications
let p = prefix_sums(&[2, 4, 6]);              // [0, 2, 6, 12]
assert_eq!(range_sum(&p, 1, 3), 10);          // 4 + 6

// Count subarrays summing to k, from p[l] = p[r] - k
assert_eq!(subarray_sum_equals_k(&[1, 1, 1], 2), 2);

// Product except self: two sweeps, no division, O(1) extra space
// out[i] = (Π_{j<i} nums[j]) * (Π_{j>i} nums[j])
assert_eq!(product_except_self(&[1, 2, 3, 4]), vec![24, 12, 8, 6]);

// Boundary search: multiplicity of 3 is upper - lower
let xs = [1, 3, 3, 3, 5, 8];
assert_eq!(binary_search_lower_bound(&xs, 3), 1);
assert_eq!(binary_search_upper_bound(&xs, 3), 4);
assert_eq!(binary_search_lower_bound(&xs, 9), 6);   // n, "not present"

// Variable window: shortest subarray with sum >= 7
assert_eq!(min_subarray_len(7, &[2, 3, 1, 2, 4, 3]), 2);

// Read/write compaction, stable and in place
let mut v = vec![0, 1, 0, 3, 12];
move_zeroes(&mut v);
assert_eq!(v, vec![1, 3, 12, 0, 0]);
```

Rust-specific notes that bite in these problems:

- Index with `usize`. `hi -= 1` when `hi == 0` panics; prefer half-open ranges
  and `while lo < hi`.
- Widen before summing: `sum += nums[i] as i64`. `i32` overflow panics in debug.
- For per-character indexing, `let cs: Vec<char> = s.chars().collect()` once
  (lesson 09), or `s.as_bytes()` if the input is guaranteed ASCII.
- `nums.swap(w, r)` avoids a borrow conflict that `nums[w] = nums[r]` on two
  mutable places would otherwise create.

## Exercises

Open `exercises/src/l11_patterns1.rs`; run `cargo test -p exercises l11`.
For each one, write the invariant as a comment before you write the body.

- `two_sum`, `subarray_sum_equals_k`, `group_anagrams` — hashing.
- `is_palindrome`, `max_area`, `move_zeroes`, `find_duplicate` — two pointers,
  opposite ends, read/write, and Floyd fast/slow respectively.
- `longest_substring_without_repeat`, `min_subarray_len`,
  `max_sum_subarray_k` — variable and fixed windows; give the amortised bound.
- `prefix_sums`, `range_sum`, `product_except_self` — prefix identities.
- `binary_search_lower_bound`, `binary_search_upper_bound` — half-open form;
  the test checks every boundary against a linear scan.

## LeetCode

- 1 Two Sum — hashing.
- 125 Valid Palindrome — two pointers with filtering.
- 167 Two Sum II — sorted input, opposite-end pointers, O(1) space.
- 11 Container With Most Water — the discard argument above.
- 15 3Sum — sort, then a two-pointer scan inside a loop.
- 3 Longest Substring Without Repeating Characters — variable window.
- 209 Minimum Size Subarray Sum — variable window, non-negative precondition.
- 643 Maximum Average Subarray I — fixed window.
- 560 Subarray Sum Equals K — prefix sums plus hashing.
- 238 Product of Array Except Self — two sweeps.
- 283 Move Zeroes — read/write pointers.
- 704 Binary Search — the base case.
- 35 Search Insert Position — lower bound, verbatim.
- 34 Find First and Last Position — lower and upper bound.
- 153 Find Minimum in Rotated Sorted Array — binary search on a non-array
  predicate; write the monotone p and the proof.
- 287 Find the Duplicate Number — Floyd on `i ↦ nums[i]`.
- 49 Group Anagrams — canonical keys.
