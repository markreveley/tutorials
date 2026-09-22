//! Lesson 04 — ownership and move semantics.

/// Take ownership of a String and return its length. The caller loses `s`.
pub fn consume_len(s: String) -> usize {
    s.len()
}

/// Take ownership, append "!" and give it back. No allocation of a new String.
pub fn shout(mut s: String) -> String {
    s.push('!');
    s
}

/// Build a Vec of the first n squares. The Vec is moved out to the caller.
pub fn squares(n: usize) -> Vec<u64> {
    let mut v = Vec::with_capacity(n);
    for i in 0..n as u64 {
        v.push(i * i);
    }
    v
}

/// Given a Vec, return (Vec of evens, Vec of odds), consuming the input.
/// Use `into_iter()` so elements move, not copy.
pub fn partition_parity(v: Vec<i32>) -> (Vec<i32>, Vec<i32>) {
    let mut evens = Vec::new();
    let mut odds = Vec::new();
    for x in v.into_iter() {
        if x % 2 == 0 { evens.push(x) } else { odds.push(x) }
    }
    (evens, odds)
}

/// Swap two values in place using `std::mem::swap` (or destructuring). No clones.
pub fn swap_in_place(a: &mut String, b: &mut String) {
    std::mem::swap(a, b);
}

/// Replace the contents of `slot` with a fresh empty Vec and return the old contents.
/// Hint: `std::mem::take`.
pub fn take_out(slot: &mut Vec<i32>) -> Vec<i32> {
    std::mem::take(slot)
}

/// Clone exactly when needed: return a Vec containing `s` twice.
/// `s` is moved in, so one clone is necessary and sufficient.
pub fn duplicate(s: String) -> Vec<String> {
    let c = s.clone();
    vec![s, c]
}

/// Copy types don't move: return the sum of a `[i32; 4]` without taking a reference.
/// The array is copied into this function; the caller keeps its own.
pub fn sum4(arr: [i32; 4]) -> i32 {
    arr.iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn consuming() {
        let s = String::from("hello");
        assert_eq!(consume_len(s), 5);
        // `s` cannot be used here: it was moved. Uncomment to see E0382.
        // let _ = s.len();
    }

    #[test]
    fn give_back() {
        let s = String::from("hi");
        let s = shout(s);
        assert_eq!(s, "hi!");
        assert_eq!(shout(s), "hi!!");
    }

    #[test]
    fn squares_move_out() {
        assert_eq!(squares(0), Vec::<u64>::new());
        assert_eq!(squares(5), vec![0, 1, 4, 9, 16]);
    }

    #[test]
    fn partition() {
        let v = vec![1, 2, 3, 4, 5];
        let (e, o) = partition_parity(v);
        assert_eq!(e, vec![2, 4]);
        assert_eq!(o, vec![1, 3, 5]);
    }

    #[test]
    fn swapping() {
        let mut a = String::from("a");
        let mut b = String::from("b");
        swap_in_place(&mut a, &mut b);
        assert_eq!((a.as_str(), b.as_str()), ("b", "a"));
    }

    #[test]
    fn taking() {
        let mut slot = vec![1, 2, 3];
        let old = take_out(&mut slot);
        assert_eq!(old, vec![1, 2, 3]);
        assert!(slot.is_empty());
    }

    #[test]
    fn dup_and_copy() {
        assert_eq!(duplicate("x".to_string()), vec!["x", "x"]);
        let arr = [1, 2, 3, 4];
        assert_eq!(sum4(arr), 10);
        assert_eq!(arr[0], 1); // still usable: arrays of Copy are Copy
    }
}
