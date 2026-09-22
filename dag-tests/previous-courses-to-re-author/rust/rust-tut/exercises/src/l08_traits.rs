//! Lesson 08 — traits, generics, bounds, dispatch.

/// Largest element of a slice for any `PartialOrd + Copy` type.
pub fn largest<T: PartialOrd + Copy>(xs: &[T]) -> Option<T> {
    todo!()
}

/// A trait for things with an area.
pub trait Area {
    fn area(&self) -> f64;
    /// Default method: true if area is zero.
    fn is_degenerate(&self) -> bool {
        todo!()
    }
}

pub struct Square(pub f64);
pub struct Circle(pub f64);

impl Area for Square {
    fn area(&self) -> f64 {
        todo!()
    }
}

impl Area for Circle {
    fn area(&self) -> f64 {
        todo!()
    }
}

/// Total area via static dispatch (generic, monomorphized).
pub fn total_area_static<T: Area>(xs: &[T]) -> f64 {
    todo!()
}

/// Total area via dynamic dispatch: heterogeneous shapes behind `dyn Area`.
pub fn total_area_dyn(xs: &[Box<dyn Area>]) -> f64 {
    todo!()
}

/// Implement `Display` for a Point so `format!("{p}")` gives "(x, y)".
pub struct Point {
    pub x: i32,
    pub y: i32,
}

impl std::fmt::Display for Point {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        todo!()
    }
}

/// A min-by-key with a closure bound. Returns the element minimizing `key`.
pub fn min_by_key_fn<T, K: Ord>(xs: &[T], key: impl Fn(&T) -> K) -> Option<&T> {
    todo!()
}

/// Implement `Ord` for `Version` so versions sort by (major, minor, patch).
/// Derive what you can.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub struct Version {
    pub major: u32,
    pub minor: u32,
    pub patch: u32,
}

/// Parse "1.2.3" into a Version via the `FromStr` trait so `"1.2.3".parse()` works.
impl std::str::FromStr for Version {
    type Err = String;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        todo!()
    }
}

/// Generic pair-sum: works for anything that can be added and copied.
pub fn pair_sum<T: std::ops::Add<Output = T> + Copy>(p: (T, T)) -> T {
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn generic_largest() {
        assert_eq!(largest(&[3, 9, 2]), Some(9));
        assert_eq!(largest(&[1.5, -2.0]), Some(1.5));
        assert_eq!(largest::<char>(&[]), None);
    }

    #[test]
    fn dispatch() {
        let sq = [Square(1.0), Square(2.0)];
        assert!((total_area_static(&sq) - 5.0).abs() < 1e-9);
        let mixed: Vec<Box<dyn Area>> = vec![Box::new(Square(1.0)), Box::new(Circle(1.0))];
        assert!((total_area_dyn(&mixed) - (1.0 + std::f64::consts::PI)).abs() < 1e-9);
        assert!(Square(0.0).is_degenerate());
        assert!(!Circle(1.0).is_degenerate());
    }

    #[test]
    fn display() {
        assert_eq!(format!("{}", Point { x: 1, y: -2 }), "(1, -2)");
    }

    #[test]
    fn min_key() {
        let ws = ["ccc", "a", "bb"];
        assert_eq!(min_by_key_fn(&ws, |w| w.len()), Some(&"a"));
        assert_eq!(min_by_key_fn::<i32, i32>(&[], |x| *x), None);
    }

    #[test]
    fn versions() {
        let a: Version = "1.2.3".parse().unwrap();
        let b: Version = "1.10.0".parse().unwrap();
        assert!(a < b);
        assert!("1.2".parse::<Version>().is_err());
        let mut vs = vec![b, a];
        vs.sort();
        assert_eq!(vs[0], a);
    }

    #[test]
    fn sums() {
        assert_eq!(pair_sum((1, 2)), 3);
        assert_eq!(pair_sum((1.5, 2.5)), 4.0);
    }
}
