pub fn num_token(tok: &str) -> Option<f64> {
    let s = tok.trim_start_matches('+');
    if !num_grammar(s) {
        return None;
    }
    s.parse::<f64>().ok().filter(|v| v.is_finite())
}
