# Rust reading assessment: assessor guide

Use after a learner attempt. This guide is evidence to check, not a keyword
matching rubric. Ask follow-ups when an answer is ambiguous. Record help and
gaps; do not infer comprehension from a memorized result. A learner can say
“I need to inspect this helper” and demonstrate good source navigation.

Source is pinned in [beatcode.lock.json](fixtures/beatcode.lock.json). Supporting
paths below refer to that checkout, not files in this course repository.

| Test | Sufficient evidence | Misconception to probe |
|---|---|---|
| R1 | Traces owned `String`, `Score`, `Vec<Event>`, then `Render`; explains borrowed arguments, error mapping, short-circuiting, and tail return. | `?` retries, a borrow copies the entire object, or `build` writes a file. |
| R2 | Predicts grammar and finite-number outcomes and explains the combinator chain. | Rust's float parser alone implements beatcode's numeric syntax. |
| R3 | Separates absence, units, generic indexing, fallible arithmetic, and nonempty-lane invariants. | `Option` is an error, `T` needs numeric behavior, or a slice index cannot panic. |
| R4 | Explains validation, borrow/mutation boundaries, stable tie ordering, and evidence for determinism. | A fixed seed makes ordering irrelevant, or `expect` propagates an ordinary error. |
| R5 | Traces borrowed events into an owned output string, including temporary lifetimes and newline/pitch behavior. | Iteration consumes the input or the output holds pointers into temporary strings. |
| R6 | Traces representations and ownership through rendering, states what the hash covers, and identifies order-sensitive arithmetic. | Equal musical meaning guarantees identical WAV bytes, or a hash proves universal correctness. |

## R1: pipeline

Read failure prevents parsing; parse failure prevents compilation and rendering;
compile failure prevents rendering. `map_err` transforms the error value;
`?` returns early on `Err` and extracts the success value on `Ok`. The final
expression already returns the required `Result`, so it needs no final `?`.
`build` produces bytes and metadata in memory. `render_to` and `write_wav` in
`src/cli.rs` establish where writing occurs. `&src` borrows an owned `String`
for a function accepting `&str`; `&evs` similarly supplies a slice view to
rendering. A strong explanation can navigate signatures rather than guessing.

## R2: numbers

In order: `Some(5.0)`, `None`, `None`, `Some(-25.0)`, `None`.
Leading plus signs are all stripped. `num_grammar` rejects `.5` and `5x`;
`1e999` passes the grammar but cannot yield an accepted finite result.
`parse::<f64>()` selects a result type; `.ok()` discards parse-error detail;
`filter` retains only a finite successful value. Trimming supplies a borrowed
substring, not an owned copy. See `tests/float_semantics.rs` and
`tests/nonfinite.rs`, and SPEC §5.8.

## R3: time lanes

No lane gives `Ok(0.0)`; 25 milliseconds gives `Ok(0.025)` seconds;
0.25 of a 0.5-second step gives `Ok(0.125)`. The `let ... else` exits for
`None`; the inner `lane` binding then denotes the borrowed lane. The enum
payload determines conversion, and the match expression yields the value.
`TimeEntry` is `Copy` in `src/score.rs`, relevant to reading it by indexed value.

The index is floor(grid / division), wrapped by the number of lane values.
It depends on time, not the number of emitted events. `T` is never inspected;
there is no need for a numeric trait bound. Rational failure is converted by
`rat_err` and propagated by `?`. The parser's lane validation supplies a
nonempty collection; `Vec<T>` itself permits empty collections. An empty lane
would break the remainder/indexing logic. Read the parser and calling context
before asserting that every possible library caller satisfies the invariant.

## R4: compilation

The three specified cases return compile errors. `&Score` allows reading the
score without consuming it; `&mut events` lets the helper append. `Ok(events)`
transfers ownership of the finished vector. `and_then` chains a fallible
operation, while `expect` would panic if its claimed invariant were false.
The sort compares performed time, then voice bytes, then step. Ties retain
their previous score order because `sort_by` is stable. Relevant evidence:
`tests/hardening.rs::duplicate_voice_ties_keep_score_order`, SPEC §6.11 and §9.3.
An unstable sort removes that tie-order guarantee; do not assert it necessarily
changes every particular output. Accumulation order can change float rounding.

## R5: JSONL

Empty input yields an empty string. Two events yield two serialized objects,
each followed by `\n`, including the second. Iterating the shared slice yields
shared event references. `event_line` returns a temporary owned `String` whose
contents are borrowed for `push_str`; `push_str` appends those bytes to `out`
before the temporary is dropped. The returned `out` owns its contents.
`&e.pitch` borrows the optional owned string; `if let` handles only `Some`.
Absent pitch is omitted under SPEC §7. The helper escapes backslash and quote,
not all control characters. Check `tests/hardening.rs` and `src/jsonl.rs` rather
than treating the specialized encoding contract as general JSON validity.

## R6: rendering

Empty events yield 44,100 frames and `peak_normalized == false`. The receipt
hashes the complete WAV bytes, including its header. The input slice is
borrowed; `wav_bytes` and `sha256_hex` move into `Render`. The closure captures
the normalization factor; mapping and collecting creates a new vector of
quantized stereo frames. Float accumulation order is consequential; a fixed
seed does not justify reassociation or parallel reduction. Inspect SPEC §9,
`tests/render_determinism.rs`, `tests/render_hashes.rs`, and the golden vectors.
Passing the tests on one machine is bounded evidence, not proof across all
machines or all inputs.

## Independent follow-up

Pick a different pinned function or fresh input and keep the key hidden until
the attempt. Ask for behavior, one language-rule explanation, one source or
test citation, and the impact of one plausible change. Label each capability
introduced, assisted, independently demonstrated, or needs review based on
the evidence. Recheck after another session before claiming retention.
