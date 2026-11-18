//! Lesson 05 — shared and mutable borrows.

/// Length of the longest string in the slice, borrowing only.
pub fn longest_len(words: &[String]) -> usize {
    todo!()
}

/// Add `delta` to every element through a mutable borrow.
pub fn add_all(xs: &mut [i32], delta: i32) {
    todo!()
}

/// Return the max element by shared reference, or None if empty.
/// Note the signature: the returned reference borrows from `xs`.
pub fn max_ref(xs: &[i32]) -> Option<&i32> {
    todo!()
}

/// Increment the element at `i` if it exists; return whether it did.
/// Use `get_mut`, not indexing (no panics).
pub fn bump_at(xs: &mut Vec<i32>, i: usize) -> bool {
    todo!()
}

/// Split a mutable slice into two halves and add 1 to the left half, 2 to the right.
/// You need two simultaneous `&mut` into one slice: use `split_at_mut`.
pub fn bump_halves(xs: &mut [i32]) {
    todo!()
}

/// Remove all elements equal to `v` in place. `retain` is allowed; or do it
/// with an index loop. Must not allocate a new Vec.
pub fn remove_all(xs: &mut Vec<i32>, v: i32) {
    todo!()
}

/// Count occurrences of `needle` in `haystack`. Both are borrowed; return value is owned.
pub fn count_occurrences(haystack: &str, needle: char) -> usize {
    todo!()
}

/// The classic borrow-checker puzzle. Given a Vec, push the first element onto
/// the end (if non-empty). `v.push(v[0])` does not compile in general because
/// `v[0]` borrows `v` while `push` needs `&mut v`. Copy the value out first.
pub fn push_first(v: &mut Vec<i32>) {
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn shared() {
        let ws = vec!["a".to_string(), "abc".to_string(), "ab".to_string()];
        assert_eq!(longest_len(&ws), 3);
        assert_eq!(longest_len(&[]), 0);
        assert_eq!(ws.len(), 3); // still owned by us
    }

    #[test]
    fn mutable() {
        let mut xs = vec![1, 2, 3];
        add_all(&mut xs, 10);
        assert_eq!(xs, vec![11, 12, 13]);
        assert!(bump_at(&mut xs, 0));
        assert!(!bump_at(&mut xs, 99));
        assert_eq!(xs[0], 12);
    }

    #[test]
    fn max_borrows() {
        let xs = vec![3, 9, 2];
        let m = max_ref(&xs);
        assert_eq!(m, Some(&9));
        assert_eq!(max_ref(&[]), None);
    }

    #[test]
    fn halves() {
        let mut xs = vec![0, 0, 0, 0, 0];
        bump_halves(&mut xs);
        assert_eq!(xs, vec![1, 1, 2, 2, 2]);
    }

    #[test]
    fn removal() {
        let mut xs = vec![1, 2, 1, 3, 1];
        remove_all(&mut xs, 1);
        assert_eq!(xs, vec![2, 3]);
    }

    #[test]
    fn counting() {
        assert_eq!(count_occurrences("banana", 'a'), 3);
        assert_eq!(count_occurrences("", 'a'), 0);
    }

    #[test]
    fn push_first_works() {
        let mut v = vec![7, 8];
        push_first(&mut v);
        assert_eq!(v, vec![7, 8, 7]);
        let mut e: Vec<i32> = vec![];
        push_first(&mut e);
        assert!(e.is_empty());
    }
}
