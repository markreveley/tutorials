//! Lesson 03 — functions, recursion and induction.

/// n! recursively. Spec: fact(0) = 1, fact(n) = n * fact(n-1).
pub fn fact(n: u64) -> u64 {
    if n == 0 { 1 } else { n * fact(n - 1) }
}

/// Fibonacci, iterative, O(n). fib(0)=0, fib(1)=1.
pub fn fib(n: u32) -> u64 {
    let (mut a, mut b) = (0u64, 1u64);
    for _ in 0..n {
        let next = a + b;
        a = b;
        b = next;
    }
    a
}

/// Fast exponentiation mod m: base^exp mod m in O(log exp). Recursive.
/// Spec: pow_mod(b, 0, m) = 1 mod m; pow_mod(b, e, m) = pow_mod(b, e/2, m)^2 * b^(e%2) mod m.
pub fn pow_mod(base: u64, exp: u64, m: u64) -> u64 {
    if exp == 0 {
        return 1 % m;
    }
    let half = pow_mod(base, exp / 2, m);
    let sq = half * half % m;
    if exp % 2 == 1 { sq * (base % m) % m } else { sq }
}

/// Greatest common divisor by Euclid's algorithm (recursive).
pub fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

/// Sum of a slice, recursively on the slice structure: sum([]) = 0, sum(x:xs) = x + sum(xs).
/// Use slice patterns or `split_first`.
pub fn sum_rec(xs: &[i64]) -> i64 {
    match xs {
        [] => 0,
        [x, rest @ ..] => x + sum_rec(rest),
    }
}

/// Reverse a string, recursively by characters. Hint: `chars()` + `next()` + `as_str()`.
pub fn reverse_rec(s: &str) -> String {
    let mut it = s.chars();
    match it.next() {
        None => String::new(),
        Some(c) => {
            let mut r = reverse_rec(it.as_str());
            r.push(c);
            r
        }
    }
}

/// Tail-recursive style with an accumulator: fact_acc(n, acc) = acc * n!.
/// Rust does not guarantee TCO, but the shape matters for reasoning.
pub fn fact_acc(n: u64, acc: u64) -> u64 {
    if n == 0 { acc } else { fact_acc(n - 1, acc * n) }
}

/// Ackermann. A(0,n)=n+1; A(m,0)=A(m-1,1); A(m,n)=A(m-1, A(m, n-1)).
/// Terminates by lexicographic induction on (m, n).
pub fn ackermann(m: u64, n: u64) -> u64 {
    match (m, n) {
        (0, n) => n + 1,
        (m, 0) => ackermann(m - 1, 1),
        (m, n) => ackermann(m - 1, ackermann(m, n - 1)),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn factorial() {
        assert_eq!(fact(0), 1);
        assert_eq!(fact(5), 120);
        assert_eq!(fact(20), 2432902008176640000);
        assert_eq!(fact_acc(5, 1), 120);
        assert_eq!(fact_acc(0, 7), 7);
    }

    #[test]
    fn fibonacci() {
        assert_eq!(fib(0), 0);
        assert_eq!(fib(1), 1);
        assert_eq!(fib(10), 55);
        assert_eq!(fib(90), 2880067194370816120);
    }

    #[test]
    fn modpow() {
        assert_eq!(pow_mod(2, 10, 1000), 24);
        assert_eq!(pow_mod(3, 0, 7), 1);
        assert_eq!(pow_mod(7, 1_000_000, 1_000_000_007), 880007888);
        assert_eq!(pow_mod(5, 3, 1), 0);
    }

    #[test]
    fn euclid() {
        assert_eq!(gcd(48, 18), 6);
        assert_eq!(gcd(17, 5), 1);
        assert_eq!(gcd(0, 9), 9);
        assert_eq!(gcd(9, 0), 9);
    }

    #[test]
    fn structural() {
        assert_eq!(sum_rec(&[]), 0);
        assert_eq!(sum_rec(&[1, 2, 3, -6]), 0);
        assert_eq!(reverse_rec(""), "");
        assert_eq!(reverse_rec("abc"), "cba");
        assert_eq!(reverse_rec("héllo"), "olléh");
    }

    #[test]
    fn ack() {
        assert_eq!(ackermann(0, 0), 1);
        assert_eq!(ackermann(1, 2), 4);
        assert_eq!(ackermann(2, 3), 9);
        assert_eq!(ackermann(3, 3), 61);
    }
}
