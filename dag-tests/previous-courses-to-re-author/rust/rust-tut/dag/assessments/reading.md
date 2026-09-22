# Rust: read, trace, and explain beatcode

These are source-reading assessments for the [DAG redesign](../../../../dag-tests/README.md).
Writing a Rust implementation is not required. Use the pinned excerpts below
and navigate the clone when you need a type definition, helper, spec, or test.
Do not read the separate assessor guide until after an attempt.

All excerpts are unaltered from beatcode commit
`b2042746329c21d6bb29deb0cec77ff666eac779`; provenance is in the
[source lock](../../../../dag-tests/fixtures/beatcode.lock.json).
These published prompts are practice. Later independent checks need fresh
inputs or a different real function, with the same capabilities assessed.

## R1. Walk the pipeline

Payload: [`cli::build`](../../../../dag-tests/fixtures/beatcode/cli.build.rs).

Explain what a successful call returns. Trace the intermediate values from
path to text to score to events to rendered output. Identify which functions
receive borrowed data and which locals own their values. Explain `map_err`,
the closure, each `?`, and the last expression without a semicolon.

Predict which stages run if reading succeeds but parsing fails. Does `build`
write a WAV file? Point to the caller or helper that settles that question.
If errors carried richer context instead of strings, identify what you would
inspect before proposing a change. No patch is required.

## R2. Distinguish successful parsing from a valid number

Payload: [`score::num_token`](../../../../dag-tests/fixtures/beatcode/score.num_token.rs).
Dependency: [`num_grammar`](../../../../dag-tests/fixtures/beatcode/score.num_grammar.rs).

Predict results for `"++5"`, `".5"`, `"1e999"`, `"-2.5e1"`, and `"5x"`.
Explain the return type, `None`, the turbofish in `parse::<f64>()`, `.ok()`,
the `filter` closure, and the borrowed string after trimming. State which
inputs are rejected by grammar and which by the finite-value check.

Locate a test covering numeric syntax and one covering non-finite inputs.
Explain why replacing the whole function with `tok.parse().ok()` would change
the accepted language and the downstream event contract.

## R3. Account for optional time lanes

Payload: [`events::time_offset`](../../../../dag-tests/fixtures/beatcode/events.time_offset.rs).
Dependency: [`lane_idx`](../../../../dag-tests/fixtures/beatcode/events.lane_idx.rs).

Explain `Option<&Lane<TimeEntry>>`, `let Some(lane) = lane else`, the shadowed
binding, `match`, and why the match result is wrapped in `Ok`.
For a grid selecting the first entry and `step_s = 0.5`, predict the result
for no lane, `Ms(25.0)`, and `Frac(0.25)`.

In `lane_idx<T>`, why is `T` sufficient without arithmetic on `T`? What does
the index count, and how does an error reach the caller? Find where nonempty
lane values are guaranteed; identify the indexing hazard if that guarantee
does not hold. Distinguish a repo invariant from a guarantee of Rust's types.

## R4. Explain compilation and reproducible ordering

Payload: [`events::compile`](../../../../dag-tests/fixtures/beatcode/events.compile.rs).

Identify the input/output types, early error branches, mutable event vector,
borrows inside the loop, and the owned return value. Explain `and_then`,
`map_err`, `?`, `expect`, and how the sorting closure chooses its order.

Predict the outcome for zero tempo, bars below one, and a finite positive
tempo so tiny that seconds-per-beat overflows. For events equal on all three
sort keys, what decides their order? Find the test that captures this behavior.
Explain a possible observable consequence of replacing stable sorting with
an unstable sort, and what evidence is needed before claiming a render changes.

## R5. Read borrowing and output construction

Payload: [`jsonl::events_jsonl`](../../../../dag-tests/fixtures/beatcode/jsonl.events_jsonl.rs).
Dependency: [`event_line`](../../../../dag-tests/fixtures/beatcode/jsonl.event_line.rs).

What do `&[Event]`, `for e in events`, `let mut out`, `&event_line(e)`, and the
final `out` mean? Predict the output for an empty slice. For two events,
describe exactly where newline characters appear. Are the input events moved
or mutated? Is text borrowed forever from a temporary string?

In `event_line`, explain `if let Some(p) = &e.pitch` and why absent pitch is
omitted rather than serialized as `null`. Find the relevant JSONL specification
and escaping test. State the limits of treating this specialized encoder as a
general-purpose JSON encoder.

## R6. Trace the render receipt and a proposed change

Payload: [`render::render`](../../../../dag-tests/fixtures/beatcode/render.render.rs).

Trace borrowed events through sample buffers, mix frames, quantization,
WAV bytes, and the returned `Render`. Explain `Option<usize>`, the empty-input
branch, `.iter().enumerate()`, the `s16` closure, `.map(...).collect()`, and
which values move into the return struct.

For no events, what are the frame count and peak-normalization flag? What
bytes are hashed? If a change proposes parallelizing/reordering mix summation,
what deterministic behavior might change and which tests/spec sections would
you inspect? Distinguish an argument from a verified cross-platform guarantee.

## Evidence record

For each attempt retain: source symbol and revision, your prediction before
running anything, explanation, supporting paths/lines or tests, help received,
and the next concept needing review. Use **unassessed** until an attempt exists.
The assessor evaluates accurate tracing, language-rule explanations, repo
evidence, and sensible change-impact reasoning. Speed, syntax memorization,
and ability to author the function from scratch are not gates.
