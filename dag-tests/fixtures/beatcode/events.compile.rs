pub fn compile(sc: &Score) -> Result<Vec<Event>, Error> {
    if sc.tempo == 0.0 {
        // Decided posture (SPEC §5.10 #11): clean error instead of the
        // reference's bare arithmetic crash. Negative tempo stays
        // accepted (all performed_s clamp to 0.0).
        return Err(Error::Compile("tempo must not be zero".to_string()));
    }
    if sc.bars < 1 {
        // Decided posture (SPEC §5.10 #13): reject bars < 1.
        return Err(Error::Compile("bars must be at least 1".to_string()));
    }
    let spb = 60.0 / sc.tempo;
    // A subnormal tempo overflows spb to inf; the oracle's arithmetic
    // raises there (like tempo 0), so reject cleanly (SPEC-GAPS #7).
    if !spb.is_finite() {
        return Err(Error::Compile("tempo out of range".to_string()));
    }
    let pattern = Rational::new(sc.bars, 1)
        .and_then(|b| b.mul(Rational::new(4, 1).expect("4/1")))
        .map_err(rat_err)?;
    let seed = mask_seed(sc.seed);

    let mut events = Vec::new();
    for v in &sc.voices {
        compile_voice(v, sc, pattern, spb, seed, &mut events)?;
    }

    // Ascending by (performed_s, voice bytes, step); stable, so ties
    // beyond the triple (duplicate voice names) keep score order
    // (SPEC §6.11 — this order is also the mix accumulation order).
    events.sort_by(|a, b| {
        a.performed_s
            .partial_cmp(&b.performed_s)
            .expect("performed_s is finite")
            .then_with(|| a.voice.as_bytes().cmp(b.voice.as_bytes()))
            .then_with(|| a.step.cmp(&b.step))
    });
    Ok(events)
}
