//! Lesson 02 — control flow, loops, loop invariants, ranges.

/// Sum of 1..=n. Use a `for` over a range. Invariant: after processing i, acc = i(i+1)/2.
pub fn sum_to(n: u64) -> u64 {
    todo!()
}

/// Collatz step count: how many steps until n reaches 1. `collatz_steps(1) == 0`.
/// Use `while` (or `loop` with `break`).
pub fn collatz_steps(n: u64) -> u32 {
    todo!()
}

/// Return the smallest k >= 0 such that 2^k >= n. `loop` with `break value`.
pub fn ceil_log2(n: u64) -> u32 {
    todo!()
}

/// FizzBuzz for one number. Use `match` on a tuple `(n % 3, n % 5)`.
pub fn fizzbuzz(n: u32) -> String {
    todo!()
}

/// Index of the first element equal to `target`, or `None`.
/// Invariant: all elements at indices < i differ from target.
pub fn linear_search(xs: &[i32], target: i32) -> Option<usize> {
    todo!()
}

/// Integer square root: largest r with r*r <= n. Use a loop, no floats.
/// Invariant: r*r <= n.
pub fn isqrt(n: u64) -> u64 {
    todo!()
}

/// Count primes < n using trial division. Nested loops; use a labeled `continue`.
pub fn count_primes(n: u32) -> u32 {
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sums() {
        assert_eq!(sum_to(0), 0);
        assert_eq!(sum_to(1), 1);
        assert_eq!(sum_to(100), 5050);
    }

    #[test]
    fn collatz() {
        assert_eq!(collatz_steps(1), 0);
        assert_eq!(collatz_steps(2), 1);
        assert_eq!(collatz_steps(6), 8);
        assert_eq!(collatz_steps(27), 111);
    }

    #[test]
    fn log2() {
        assert_eq!(ceil_log2(1), 0);
        assert_eq!(ceil_log2(2), 1);
        assert_eq!(ceil_log2(3), 2);
        assert_eq!(ceil_log2(1024), 10);
        assert_eq!(ceil_log2(1025), 11);
    }

    #[test]
    fn fb() {
        assert_eq!(fizzbuzz(3), "Fizz");
        assert_eq!(fizzbuzz(10), "Buzz");
        assert_eq!(fizzbuzz(15), "FizzBuzz");
        assert_eq!(fizzbuzz(7), "7");
    }

    #[test]
    fn search() {
        assert_eq!(linear_search(&[4, 2, 9], 9), Some(2));
        assert_eq!(linear_search(&[4, 2, 9], 5), None);
        assert_eq!(linear_search(&[], 5), None);
        assert_eq!(linear_search(&[1, 1], 1), Some(0));
    }

    #[test]
    fn sqrt() {
        assert_eq!(isqrt(0), 0);
        assert_eq!(isqrt(1), 1);
        assert_eq!(isqrt(15), 3);
        assert_eq!(isqrt(16), 4);
        assert_eq!(isqrt(99), 9);
    }

    #[test]
    fn primes() {
        assert_eq!(count_primes(2), 0);
        assert_eq!(count_primes(10), 4);
        assert_eq!(count_primes(100), 25);
    }
}
