//! Lesson 10 — iterators, adapters, consumers, and closures.

/// Square every even element, in order. `filter` then `map`, one pass, no intermediate Vec.
pub fn squares_of_evens(xs: &[i32]) -> Vec<i32> {
    todo!()
}

/// Total byte length of all words. `fold` written as `map` + `sum`.
pub fn sum_of_lengths(words: &[&str]) -> usize {
    todo!()
}

/// Inclusive prefix sums: out[i] = Σ xs[0..=i]. `scan` threads mutable state through a chain.
pub fn running_totals(xs: &[i32]) -> Vec<i32> {
    todo!()
}

/// The longest strictly increasing *prefix* of `xs`. `enumerate` + `take_while`.
pub fn take_while_increasing(xs: &[i32]) -> Vec<i32> {
    todo!()
}

/// Elementwise sum, truncated to the shorter input — `zip` stops at the first `None`.
pub fn zip_sum(a: &[i32], b: &[i32]) -> Vec<i32> {
    todo!()
}

/// Index of the first element satisfying `pred`. `position` short-circuits.
pub fn index_of_first(xs: &[i32], pred: impl Fn(i32) -> bool) -> Option<usize> {
    todo!()
}

/// `all` on an empty slice is `true` (vacuous truth), matching ∀ over the empty set.
pub fn all_positive(xs: &[i32]) -> bool {
    todo!()
}

/// Does any adjacent pair repeat? `windows(2)` + `any`.
pub fn any_adjacent_equal(xs: &[i32]) -> bool {
    todo!()
}

/// Concatenate the inner vectors. `flat_map` = `map` then `flatten`.
pub fn flatten_nested(v: &[Vec<i32>]) -> Vec<i32> {
    todo!()
}

/// Longest word; ties go to the last maximum, per `max_by_key`'s documented rule.
pub fn longest_word<'a>(words: &[&'a str]) -> Option<&'a str> {
    todo!()
}

/// Split into (matching, non-matching). `partition` is a consumer, not an adapter.
pub fn partition_parity(xs: &[i32]) -> (Vec<i32>, Vec<i32>) {
    todo!()
}

/// Sum of each contiguous chunk of `k` (the final chunk may be short). `k == 0` gives `[]`.
pub fn chunk_sums(xs: &[i32], k: usize) -> Vec<i32> {
    todo!()
}

/// `a` reversed, followed by `b`. `rev` needs a `DoubleEndedIterator`; slice iters are one.
pub fn rev_chain(a: &[i32], b: &[i32]) -> Vec<i32> {
    todo!()
}

/// Product via `fold`, showing the accumulator explicitly.
pub fn product_fold(xs: &[i32]) -> i64 {
    todo!()
}

/// `Fn`: the closure only reads its captures, so it can be called many times.
pub fn apply_twice<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 {
    todo!()
}

/// A closure that captures `n` by value (`move`) and outlives the call that built it.
/// Boxed so the return type is nameable; `-> impl Fn(i32) -> i32` is the zero-cost form.
pub fn make_adder(n: i32) -> Box<dyn Fn(i32) -> i32> {
    todo!()
}

/// `FnMut`: mutable captured state. Returns 1, 2, 3, ... on successive calls.
/// Calling it needs a `mut` binding — that is what distinguishes `FnMut` from `Fn`.
pub fn counter() -> Box<dyn FnMut() -> u32> {
    todo!()
}

/// `FnOnce`: the closure consumes a capture, so it may be called at most once.
pub fn consume_once<F: FnOnce() -> String>(f: F) -> String {
    todo!()
}

/// A hand-written iterator. Implementing `next` is the whole contract; every
/// adapter and consumer comes free from the `Iterator` blanket methods.
pub struct Fib {
    a: u64,
    b: u64,
}

impl Iterator for Fib {
    type Item = u64;
    fn next(&mut self) -> Option<u64> {
        todo!()
    }
}

/// 0, 1, 1, 2, 3, 5, ... — infinite; `take` makes it finite.
pub fn fib() -> Fib {
    todo!()
}

/// First `n` Fibonacci numbers. Proof that laziness is load-bearing: `fib()` never ends.
pub fn first_n_fib(n: usize) -> Vec<u64> {
    todo!()
}

/// Sum of squares of the first `n` odd numbers, built from a lazy range.
pub fn odd_squares_sum(n: u64) -> u64 {
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adapters() {
        assert_eq!(squares_of_evens(&[1, 2, 3, 4]), vec![4, 16]);
        assert_eq!(sum_of_lengths(&["ab", "cde"]), 5);
        assert_eq!(running_totals(&[1, 2, 3]), vec![1, 3, 6]);
        assert_eq!(running_totals(&[]), Vec::<i32>::new());
        assert_eq!(take_while_increasing(&[1, 3, 5, 4, 9]), vec![1, 3, 5]);
        assert_eq!(take_while_increasing(&[5, 5]), vec![5]);
        assert_eq!(zip_sum(&[1, 2, 3], &[10, 20]), vec![11, 22]);
        assert_eq!(flatten_nested(&[vec![1, 2], vec![], vec![3]]), vec![1, 2, 3]);
        assert_eq!(rev_chain(&[1, 2, 3], &[9]), vec![3, 2, 1, 9]);
        assert_eq!(chunk_sums(&[1, 2, 3, 4, 5], 2), vec![3, 7, 5]);
        assert_eq!(chunk_sums(&[1], 0), Vec::<i32>::new());
    }

    #[test]
    fn consumers() {
        assert_eq!(index_of_first(&[1, 3, 4, 5], |x| x % 2 == 0), Some(2));
        assert_eq!(index_of_first(&[1, 3], |x| x % 2 == 0), None);
        assert!(all_positive(&[1, 2]));
        assert!(all_positive(&[]));
        assert!(!all_positive(&[1, -1]));
        assert!(any_adjacent_equal(&[1, 2, 2, 3]));
        assert!(!any_adjacent_equal(&[1, 2, 3]));
        assert_eq!(longest_word(&["a", "abc", "ab"]), Some("abc"));
        assert_eq!(longest_word(&[]), None);
        assert_eq!(partition_parity(&[1, 2, 3, 4]), (vec![2, 4], vec![1, 3]));
        assert_eq!(product_fold(&[2, 3, 4]), 24);
        assert_eq!(product_fold(&[]), 1);
    }

    #[test]
    fn closures() {
        assert_eq!(apply_twice(|x| x * 3, 2), 18);
        let add5 = make_adder(5);
        assert_eq!(add5(1), 6);
        assert_eq!(add5(2), 7);
        let mut c = counter();
        assert_eq!((c(), c(), c()), (1, 2, 3));
        let owned = String::from("gone");
        assert_eq!(consume_once(move || owned), "gone");
    }

    #[test]
    fn custom_iterator_is_lazy() {
        assert_eq!(first_n_fib(8), vec![0, 1, 1, 2, 3, 5, 8, 13]);
        assert_eq!(first_n_fib(0), Vec::<u64>::new());
        assert_eq!(fib().take_while(|&x| x < 100).filter(|x| x % 2 == 0).sum::<u64>(), 44);
        assert_eq!(odd_squares_sum(3), 1 + 9 + 25);
    }
}
