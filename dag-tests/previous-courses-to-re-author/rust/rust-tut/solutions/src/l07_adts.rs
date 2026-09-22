//! Lesson 07 — structs, enums, Option/Result, exhaustive matching.

/// A 2D point (product type).
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Point {
    pub x: i64,
    pub y: i64,
}

impl Point {
    /// Manhattan distance |x1-x2| + |y1-y2|.
    pub fn manhattan(self, other: Point) -> i64 {
        (self.x - other.x).abs() + (self.y - other.y).abs()
    }
}

/// A shape (sum type).
#[derive(Debug, Clone, PartialEq)]
pub enum Shape {
    Circle { r: f64 },
    Rect { w: f64, h: f64 },
    Tri { a: f64, b: f64, c: f64 },
}

impl Shape {
    /// Area. Triangle via Heron's formula. Match must be exhaustive: no `_` arm.
    pub fn area(&self) -> f64 {
        match self {
            Shape::Circle { r } => std::f64::consts::PI * r * r,
            Shape::Rect { w, h } => w * h,
            Shape::Tri { a, b, c } => {
                let s = (a + b + c) / 2.0;
                (s * (s - a) * (s - b) * (s - c)).sqrt()
            }
        }
    }
}

/// Arithmetic expression tree.
#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    Num(i64),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
    Div(Box<Expr>, Box<Expr>),
}

/// Evaluate; division by zero is an `Err`. Use `?` to propagate.
pub fn eval(e: &Expr) -> Result<i64, String> {
    Ok(match e {
        Expr::Num(n) => *n,
        Expr::Add(a, b) => eval(a)? + eval(b)?,
        Expr::Mul(a, b) => eval(a)? * eval(b)?,
        Expr::Div(a, b) => {
            let d = eval(b)?;
            if d == 0 {
                return Err("division by zero".to_string());
            }
            eval(a)? / d
        }
    })
}

/// Parse "x,y" into a Point. Errors: wrong shape or non-integer.
/// Use `split_once`, `parse::<i64>()`, `ok_or`, `map_err`, `?`.
pub fn parse_point(s: &str) -> Result<Point, String> {
    let (xs, ys) = s.split_once(',').ok_or_else(|| format!("no comma in {s:?}"))?;
    let x = xs.trim().parse::<i64>().map_err(|e| e.to_string())?;
    let y = ys.trim().parse::<i64>().map_err(|e| e.to_string())?;
    Ok(Point { x, y })
}

/// Second-largest distinct value, or None. Use Option combinators or a match.
pub fn second_largest(xs: &[i32]) -> Option<i32> {
    let mut first: Option<i32> = None;
    let mut second: Option<i32> = None;
    for &x in xs {
        match first {
            Some(f) if x == f => {}
            Some(f) if x > f => {
                second = first;
                first = Some(x);
            }
            Some(_) => match second {
                Some(s) if x <= s => {}
                _ => second = Some(x),
            },
            None => first = Some(x),
        }
    }
    second
}

/// Traffic light state machine.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Light {
    Red,
    Green,
    Yellow,
}

impl Light {
    /// Red -> Green -> Yellow -> Red.
    pub fn next(self) -> Light {
        match self {
            Light::Red => Light::Green,
            Light::Green => Light::Yellow,
            Light::Yellow => Light::Red,
        }
    }
}

/// Sum all `Some` values; return None if *any* is None. (Option<Vec> via collect.)
pub fn sum_all(xs: &[Option<i32>]) -> Option<i32> {
    xs.iter().copied().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn points() {
        let p = Point { x: 1, y: 2 };
        let q = Point { x: -2, y: 6 };
        assert_eq!(p.manhattan(q), 7);
        assert_eq!(parse_point("3, -4"), Ok(Point { x: 3, y: -4 }));
        assert!(parse_point("3 4").is_err());
        assert!(parse_point("a,4").is_err());
    }

    #[test]
    fn shapes() {
        assert!((Shape::Rect { w: 2.0, h: 3.0 }.area() - 6.0).abs() < 1e-9);
        assert!((Shape::Tri { a: 3.0, b: 4.0, c: 5.0 }.area() - 6.0).abs() < 1e-9);
        assert!((Shape::Circle { r: 1.0 }.area() - std::f64::consts::PI).abs() < 1e-9);
    }

    #[test]
    fn exprs() {
        use Expr::*;
        let e = Add(Box::new(Num(2)), Box::new(Mul(Box::new(Num(3)), Box::new(Num(4)))));
        assert_eq!(eval(&e), Ok(14));
        let bad = Div(Box::new(Num(1)), Box::new(Add(Box::new(Num(1)), Box::new(Num(-1)))));
        assert_eq!(eval(&bad), Err("division by zero".to_string()));
    }

    #[test]
    fn second() {
        assert_eq!(second_largest(&[]), None);
        assert_eq!(second_largest(&[5]), None);
        assert_eq!(second_largest(&[5, 5]), None);
        assert_eq!(second_largest(&[1, 3, 2]), Some(2));
        assert_eq!(second_largest(&[3, 3, 1]), Some(1));
    }

    #[test]
    fn lights() {
        assert_eq!(Light::Red.next(), Light::Green);
        assert_eq!(Light::Red.next().next().next(), Light::Red);
    }

    #[test]
    fn sums() {
        assert_eq!(sum_all(&[Some(1), Some(2)]), Some(3));
        assert_eq!(sum_all(&[Some(1), None]), None);
        assert_eq!(sum_all(&[]), Some(0));
    }
}
