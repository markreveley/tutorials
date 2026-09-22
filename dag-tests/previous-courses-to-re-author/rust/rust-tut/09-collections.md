# 09. Collections

## Concept

Six containers cover essentially every LeetCode problem. All live in
`std::collections` except `Vec` and `String`, which are in the prelude.

```rust
use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque};

let mut v: Vec<i32>        = vec![3, 1, 2];   // growable array
let mut s: String          = String::from("hi");
let mut m: HashMap<&str, i32> = HashMap::new();
let mut hs: HashSet<i32>   = HashSet::new();
let mut dq: VecDeque<i32>  = VecDeque::new(); // ring buffer, O(1) both ends
let mut h: BinaryHeap<i32> = BinaryHeap::new(); // MAX-heap
let mut bt: BTreeMap<i32, &str> = BTreeMap::new(); // sorted, range queries
let mut bs: BTreeSet<i32>  = BTreeSet::new();
```

`Vec<T>` is a triple (pointer, length, capacity). Push amortises to O(1) by
doubling capacity; `v[i]` is a bounds-checked O(1) offset.

```rust
v.push(9); v.pop();            // Some(9)
v.sort_unstable();             // O(n log n), no allocation
v.binary_search(&2);           // Ok(idx) | Err(insertion_point)
&v[1..3];                      // slice: a (pointer, length) view, no copy
v.swap(0, 2); v.retain(|x| *x > 0); v.dedup();
```

`String` owns a `Vec<u8>` guaranteed to hold valid UTF-8. `&str` is a borrowed
slice of such bytes. Neither is indexable by an integer.

```rust
let s = "héllo";
s.len();                       // 6  — BYTES, not chars
s.chars().count();             // 5  — O(n) walk
s.chars().nth(1);              // Some('é')
&s[0..1];                      // "h"   — byte range, checked
// &s[0..2];                   // PANIC: byte index 2 is not a char boundary
s.as_bytes()[0];               // 104  — u8, O(1)
let cs: Vec<char> = s.chars().collect();  // O(n) once, then O(1) indexing
```

`HashMap` uses SipHash-1-3 by default (DoS-resistant, slightly slow) with open
addressing. The **Entry API** is the only way to do "look up, then insert or
modify" in one hash and one probe:

```rust
*m.entry("a").or_insert(0) += 1;          // count
m.entry("b").or_insert_with(Vec::new);    // lazy default
m.entry("c").and_modify(|v| *v += 1).or_insert(1);
groups.entry(k).or_default().push(x);     // needs V: Default
```

`BinaryHeap<T: Ord>` is a max-heap: `pop` yields the greatest element.
`std::cmp::Reverse` is a zero-cost newtype whose `Ord` is flipped, so one type
serves both directions:

```rust
use std::cmp::Reverse;
let mut min_heap = BinaryHeap::new();
min_heap.push(Reverse(5));
let Reverse(smallest) = min_heap.pop().unwrap();   // 5
```

`BTreeMap`/`BTreeSet` keep keys in sorted order in a B-tree (branching factor
~11, so cache-friendly). They buy you what hashing cannot give: `range`,
`first_key_value`, and ordered iteration.

```rust
bt.range(3..7);            // half-open, O(log n + hits)
bt.first_key_value();      // Option<(&K, &V)>
```

## Why

### Why `String` is not indexable by an integer

You want `s[i]` to be the i-th character in O(1). Two requirements collide.

**(A) The bytes are contiguous UTF-8.** A `char` occupies 1–4 bytes depending
on its value. So the byte offset of character i is

    off(i) = Σ_{j < i} width(s.chars[j])

which depends on the *data*, not on i.

**(B) O(1) random access needs an address computable from i alone.** For a
fixed-width element type that is `base + i·size`. Under (A) there is no such
formula: to know `off(i)` you must have read every earlier character.

So an implementation must pick one:

1. **Scan** — `off(i)` costs O(i). Then `s[i]` is not O(1). This is what
   `s.chars().nth(i)` does, and Rust makes the cost visible by refusing to
   spell it `s[i]`.
2. **Side index** — store `off(0..n)` alongside. O(n) extra space, and every
   insertion invalidates the suffix of the index, so mutation becomes O(n).
3. **Fixed-width encoding** (UTF-32) — 4 bytes per character, so ASCII text
   costs 4× the memory, and every read/write to the outside world (files,
   sockets, JSON, C APIs — all UTF-8) needs transcoding.

Rust chooses (1) and *renames the operation*: `s[a..b]` is a **byte** range,
O(1), and panics if `a` or `b` is not a char boundary (`s.is_char_boundary`).
Integer indexing is simply not implemented, because there is no definition of
it that is both O(1) and meaningful. Compare Python, which picks (3)-ish
internally (PEP 393 picks 1, 2, or 4 bytes per string) and pays with a
per-string mode flag.

Corollary for LeetCode: if a problem indexes into a string repeatedly, pay the
O(n) once — `let cs: Vec<char> = s.chars().collect();` — and index `cs`.
If it is guaranteed ASCII, `s.as_bytes()` is even cheaper and `b'a'` gives you
byte literals.

One more caveat: `char` is a **Unicode scalar value**, not a user-perceived
character. `"é"` may be one scalar (U+00E9) or two (`e` + U+0301). `chars()`
counts scalars. Grapheme clusters need a crate, which we do not have.

### Why the Entry API exists

The natural code

```rust
if !m.contains_key(&k) { m.insert(k, 0); }   // hash #1, hash #2
*m.get_mut(&k).unwrap() += 1;                // hash #3
```

hashes three times and probes three times. Worse, in Rust the borrow checker
would reject the tempting one-liner form: `m.get_mut(&k)` holds a `&mut m` for
as long as the returned reference lives, so you cannot call `m.insert` inside
that scope. `entry(k)` returns an `Entry` that *owns* the position it found —
one hash, one probe, and a single mutable borrow that ends when you are done.
It is both the fast and the only borrow-legal shape.

### Why `BinaryHeap` is a max-heap and `Reverse` is free

A binary heap only needs `Ord`. Providing both `MinHeap` and `MaxHeap` types
doubles the API for no gain, since `Reverse<T>` is a `#[repr(transparent)]`
newtype with

    Reverse(a) < Reverse(b)  ⇔  b < a

Monomorphisation compiles `BinaryHeap<Reverse<i32>>` to the same machine code
as a hypothetical `MinHeap<i32>`: same layout, same comparisons, opposite sense.
The wrapper is erased at compile time. This is the same argument as lesson 10's
zero-cost iterators.

### Cost, as a proof obligation

A solution is not finished until you can state its time and space bound and say
*why*. The reason column is the part that matters.

| Operation | Vec | reason |
| --- | --- | --- |
| `v[i]` | O(1) | address = base + i·size |
| `push` | amortised O(1) | capacity doubles; Σ copies over n pushes < 2n |
| `insert(0, x)` / `remove(0)` | O(n) | every later element shifts |
| `contains` | O(n) | unordered linear scan |
| `sort_unstable` | O(n log n) | pattern-defeating quicksort, in place |
| `binary_search` | O(log n) | halving; requires sorted input |

| Operation | VecDeque | reason |
| --- | --- | --- |
| `push_front/back`, `pop_front/back` | amortised O(1) | ring buffer: move an index, no shifting |
| `dq[i]` | O(1) | offset from head, modulo capacity |
| contiguous slice | not guaranteed | the ring may wrap; use `make_contiguous` |

| Operation | HashMap / HashSet | reason |
| --- | --- | --- |
| `insert`, `get`, `remove` | O(1) expected | hash to a bucket; load factor kept < 7/8 |
| worst case | O(n) | adversarial collisions (SipHash makes this hard) |
| iteration order | unspecified | bucket order, and it changes between runs |

| Operation | BTreeMap / BTreeSet | reason |
| --- | --- | --- |
| `insert`, `get`, `remove` | O(log n) | height is Θ(log n) with branching factor B |
| `range(a..b)` | O(log n + k) | descend once, then walk k hits in order |
| iteration | O(n), sorted | in-order traversal |

| Operation | BinaryHeap | reason |
| --- | --- | --- |
| `push` | O(log n) | sift up one path of a complete tree |
| `pop` | O(log n) | swap root with last, sift down one path |
| `peek` | O(1) | the root is index 0 |
| build from Vec | O(n) | Σ over levels of (nodes × height) telescopes to < 2n |

Two derived facts worth memorising:

- **Top-k of n items: O(n log k), not O(n log n).** Keep a size-k *min*-heap;
  every element does one push and at most one pop on a heap of size ≤ k.
- **`k_smallest` uses a max-heap and `k_largest` uses a min-heap.** The heap
  holds the current answer set, and you evict the *worst* member of it, which
  is the opposite extreme from what you are selecting.

## Worked examples

```rust
// Counting with entry
let mut c: HashMap<char, usize> = HashMap::new();
for ch in "mississippi".chars() { *c.entry(ch).or_insert(0) += 1; }
assert_eq!(c[&'s'], 4);

// Set membership in one pass
let mut seen = HashSet::new();
let first_dup = [3, 1, 4, 1].iter().find(|&&x| !seen.insert(x));
assert_eq!(first_dup, Some(&1));           // insert returns false if present

// Monotonic deque: sliding window maximum in amortised O(n)
// dq holds indices, values strictly decreasing. Each index is pushed once
// and popped at most once ⇒ ≤ 2n deque operations total.

// Min-heap via Reverse
let mut h = BinaryHeap::new();
for x in [5, 1, 9] { h.push(Reverse(x)); }
assert_eq!(h.pop(), Some(Reverse(1)));

// Ordered range query — a HashMap cannot do this at all
let bt: BTreeMap<i32, i32> = (0..10).map(|k| (k, k * k)).collect();
let s: i32 = bt.range(2..5).map(|(_, v)| v).sum();   // 4 + 9 + 16
assert_eq!(s, 29);

// Byte vs char, made explicit
let s = "日本語";
assert_eq!(s.len(), 9);
assert_eq!(s.chars().count(), 3);
assert_eq!(s.char_indices().map(|(i, _)| i).collect::<Vec<_>>(), vec![0, 3, 6]);
assert!(s.is_char_boundary(3));
assert!(!s.is_char_boundary(1));
```

## Exercises

Open `exercises/src/l09_collections.rs`; run `cargo test -p exercises l09`.

- `char_count`, `nth_char`, `byte_len_vs_char_len`, `reverse_chars`,
  `char_boundaries` — UTF-8 in practice; state the cost of each.
- `word_frequencies` — the Entry API, one hash per word.
- `first_duplicate`, `dedup_preserve_order` — `HashSet::insert`'s return value.
- `sliding_max` — monotonic `VecDeque`; argue the amortised O(n).
- `k_largest`, `k_smallest` — size-k heaps; get the direction right.
- `sorted_unique`, `range_sum`, `group_by_first_char` — when order buys you
  something hashing cannot.
- `rotate_left` — O(1) rotation on a ring buffer.

## LeetCode

- 1 Two Sum — `HashMap`.
- 20 Valid Parentheses — `Vec` as a stack.
- 49 Group Anagrams — `HashMap` with a sorted-letters key.
- 217 Contains Duplicate — `HashSet`.
- 242 Valid Anagram — counting map, or a `[u32; 26]`.
- 347 Top K Frequent Elements — counting map plus a size-k heap.
- 239 Sliding Window Maximum — monotonic `VecDeque`.
- 703 Kth Largest Element in a Stream — `BinaryHeap<Reverse<i32>>`.
- 692 Top K Frequent Words — heap ordering with a tie-break.
- 128 Longest Consecutive Sequence — `HashSet` with an O(n) argument.
