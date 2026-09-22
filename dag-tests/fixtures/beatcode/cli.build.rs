fn build(score_path: &str) -> Result<render::Render, String> {
    let src = std::fs::read_to_string(score_path)
        .map_err(|e| format!("cannot read {score_path}: {e}"))?;
    let sc = score::parse(&src).map_err(|e| e.to_string())?;
    let evs = events::compile(&sc).map_err(|e| e.to_string())?;
    render::render(&evs).map_err(|e| e.to_string())
}
