fn time_offset(lane: Option<&Lane<TimeEntry>>, grid: Rational, step_s: f64) -> Result<f64, Error> {
    let Some(lane) = lane else { return Ok(0.0) };
    Ok(match lane.vals[lane_idx(lane, grid)?] {
        TimeEntry::Ms(v) => v / 1000.0,
        TimeEntry::Frac(v) => v * step_s,
    })
}
