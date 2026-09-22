fn lane_idx<T>(lane: &Lane<T>, grid: Rational) -> Result<usize, Error> {
    let q = grid.divr(lane.div).map_err(rat_err)?;
    Ok(q.floor_i().rem_euclid(lane.vals.len() as i64) as usize)
}
