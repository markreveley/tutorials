//! Lesson 01 — values, types, expressions, shadowing, integer overflow.

/// Return the area of a rectangle. Both sides fit in u32; the product may not.
/// Use a wider type so the result is exact.
pub fn area(w: u32, h: u32) -> u64 {
    w as u64 * h as u64
}

/// Celsius to Fahrenheit. `f = c * 9/5 + 32`. Note float arithmetic.
pub fn c_to_f(c: f64) -> f64 {
    c * 9.0 / 5.0 + 32.0
}

/// Return `true` iff `n` is even. Use an expression, not `if ... return`.
pub fn is_even(n: i64) -> bool {
    n % 2 == 0
}

/// Wrapping add: (a + b) mod 2^32, never panics.
pub fn wrapping_sum(a: u32, b: u32) -> u32 {
    a.wrapping_add(b)
}

/// Checked add: `Some(a+b)` if representable in i32, else `None`.
pub fn checked_sum(a: i32, b: i32) -> Option<i32> {
    a.checked_add(b)
}

/// Saturating subtract for unsigned: max(a - b, 0).
pub fn sat_sub(a: u8, b: u8) -> u8 {
    a.saturating_sub(b)
}

/// Digit sum of a non-negative integer written in base 10.
/// 0 -> 0, 1234 -> 10. Use a `while` loop; it's fine to shadow.
pub fn digit_sum(n: u64) -> u32 {
    let mut n = n;
    let mut s = 0;
    while n > 0 {
        s += (n % 10) as u32;
        n /= 10;
    }
    s
}

/// Return the larger of two values using an `if` *expression* (no `return`).
pub fn max_expr(a: i32, b: i32) -> i32 {
    if a > b { a } else { b }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn area_is_exact_for_large_inputs() {
        assert_eq!(area(3, 4), 12);
        assert_eq!(area(u32::MAX, u32::MAX), (u32::MAX as u64) * (u32::MAX as u64));
    }

    #[test]
    fn temperature() {
        assert_eq!(c_to_f(0.0), 32.0);
        assert!((c_to_f(100.0) - 212.0).abs() < 1e-9);
        assert!((c_to_f(-40.0) - (-40.0)).abs() < 1e-9);
    }

    #[test]
    fn evenness() {
        assert!(is_even(0));
        assert!(is_even(-4));
        assert!(!is_even(7));
    }

    #[test]
    fn overflow_modes() {
        assert_eq!(wrapping_sum(u32::MAX, 1), 0);
        assert_eq!(wrapping_sum(5, 6), 11);
        assert_eq!(checked_sum(i32::MAX, 1), None);
        assert_eq!(checked_sum(2, 3), Some(5));
        assert_eq!(checked_sum(i32::MIN, -1), None);
        assert_eq!(sat_sub(3, 10), 0);
        assert_eq!(sat_sub(10, 3), 7);
    }

    #[test]
    fn digits() {
        assert_eq!(digit_sum(0), 0);
        assert_eq!(digit_sum(1234), 10);
        assert_eq!(digit_sum(u64::MAX), 87);
    }

    #[test]
    fn max_expression() {
        assert_eq!(max_expr(1, 2), 2);
        assert_eq!(max_expr(5, -5), 5);
        assert_eq!(max_expr(3, 3), 3);
    }
}
