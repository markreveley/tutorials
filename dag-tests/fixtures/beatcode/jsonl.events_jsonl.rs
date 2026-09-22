pub fn events_jsonl(events: &[Event]) -> String {
    let mut out = String::new();
    for e in events {
        out.push_str(&event_line(e));
        out.push('\n');
    }
    out
}
