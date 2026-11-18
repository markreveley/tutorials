//! Lesson 06 — lifetimes.

/// Return the longer of two string slices. Both inputs and the output share one lifetime.
pub fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {
    if a.len() >= b.len() { a } else { b }
}

/// Return the first word of `s` (up to the first space). Elision applies: one input
/// reference, so the output borrows from it.
pub fn first_word(s: &str) -> &str {
    match s.find(' ') {
        Some(i) => &s[..i],
        None => s,
    }
}

/// Return the first element of `xs` that is strictly greater than `bound`, or None.
/// The output borrows from `xs`, not from `bound` — write the lifetimes so that
/// `bound` can have a shorter lifetime than the result.
pub fn first_above<'a>(xs: &'a [i32], bound: &i32) -> Option<&'a i32> {
    xs.iter().find(|&&x| x > *bound)
}

/// A struct holding a borrowed slice. `Window` cannot outlive the data it views.
pub struct Window<'a> {
    pub data: &'a [i32],
}

impl<'a> Window<'a> {
    /// Construct a window over `data`.
    pub fn new(data: &'a [i32]) -> Self {
        Window { data }
    }

    /// Sum of the window's elements.
    pub fn sum(&self) -> i32 {
        self.data.iter().sum()
    }

    /// A narrower window: `self.data[lo..hi]`. The result has the *data's* lifetime,
    /// not `&self`'s — `'a`, not elided.
    pub fn narrow(&self, lo: usize, hi: usize) -> Window<'a> {
        Window { data: &self.data[lo..hi] }
    }
}

/// Split a string on the first occurrence of `sep`. Return (before, after).
/// If `sep` is absent, after is "".
pub fn split_once_at<'a>(s: &'a str, sep: char) -> (&'a str, &'a str) {
    match s.find(sep) {
        Some(i) => (&s[..i], &s[i + sep.len_utf8()..]),
        None => (s, ""),
    }
}

/// Return a reference into `map` for the longest key, or None. The output lifetime
/// comes from the map borrow.
pub fn longest_key(map: &std::collections::HashMap<String, i32>) -> Option<&str> {
    map.keys().max_by_key(|k| k.len()).map(|k| k.as_str())
}

/// `'static` data: return a string slice that lives for the whole program.
pub fn greeting() -> &'static str {
    "hello"
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    #[test]
    fn longest_works() {
        let a = String::from("abcd");
        let r;
        {
            let b = String::from("xy");
            r = longest(a.as_str(), b.as_str()).to_string();
        }
        assert_eq!(r, "abcd");
    }

    #[test]
    fn words() {
        assert_eq!(first_word("hello world"), "hello");
        assert_eq!(first_word("hello"), "hello");
        assert_eq!(first_word(""), "");
    }

    #[test]
    fn above() {
        let xs = vec![1, 5, 3, 8];
        let r = {
            let bound = 4;
            first_above(&xs, &bound) // `bound` dies here; the result must not borrow it
        };
        assert_eq!(r, Some(&5));
        assert_eq!(first_above(&xs, &100), None);
    }

    #[test]
    fn window() {
        let data = vec![1, 2, 3, 4];
        let narrow = {
            let w = Window::new(&data);
            assert_eq!(w.sum(), 10);
            w.narrow(1, 3) // `w` dies; `narrow` must borrow `data`, not `w`
        };
        assert_eq!(narrow.sum(), 5);
    }

    #[test]
    fn splitting() {
        assert_eq!(split_once_at("a=b=c", '='), ("a", "b=c"));
        assert_eq!(split_once_at("abc", '='), ("abc", ""));
        assert_eq!(split_once_at("x→y", '→'), ("x", "y"));
    }

    #[test]
    fn keys() {
        let mut m = HashMap::new();
        assert_eq!(longest_key(&m), None);
        m.insert("ab".to_string(), 1);
        m.insert("abcd".to_string(), 2);
        assert_eq!(longest_key(&m), Some("abcd"));
        assert_eq!(greeting(), "hello");
    }
}
