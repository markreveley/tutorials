pub fn event_line(e: &Event) -> String {
    // Fixed full key sequence (byte order): gain, grid, hum_ms, kind,
    // lane_ms, pan, performed_s, pitch, step, swing_ms, vel, voice.
    let mut s = String::from("{\"gain\":");
    push_f64(&mut s, e.gain);
    s.push_str(",\"grid\":");
    push_str_val(&mut s, &e.grid.to_s());
    s.push_str(",\"hum_ms\":");
    push_f64(&mut s, e.hum_ms);
    s.push_str(",\"kind\":");
    push_str_val(&mut s, e.kind.name());
    s.push_str(",\"lane_ms\":");
    push_f64(&mut s, e.lane_ms);
    s.push_str(",\"pan\":");
    push_f64(&mut s, e.pan);
    s.push_str(",\"performed_s\":");
    push_f64(&mut s, e.performed_s);
    if let Some(p) = &e.pitch {
        s.push_str(",\"pitch\":");
        push_str_val(&mut s, p);
    }
    s.push_str(",\"step\":");
    s.push_str(&e.step.to_string());
    s.push_str(",\"swing_ms\":");
    push_f64(&mut s, e.swing_ms);
    s.push_str(",\"vel\":");
    s.push_str(&e.vel.to_string());
    s.push_str(",\"voice\":");
    push_str_val(&mut s, &e.voice);
    s.push('}');
    s
}
