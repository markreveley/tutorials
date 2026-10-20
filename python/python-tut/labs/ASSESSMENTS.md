# Python: implement, debug, and explain an evaluation

These are the first learner tests for the [test-first assessment layer](../../../dag-tests/README.md).
They are public practice cases. There is no recorded learner attempt yet.
Use standard-library Python and ordinary documentation. Implement the three
functions in [eval_pipeline.py](eval_pipeline.py); no API calls,
model account, or paid runs are needed.

## 1. Score an extracted support ticket

`score_ticket(prediction, reference) -> bool`

A valid reference is a dictionary with exactly these keys:
`category` (a nonempty string), `urgent` (a Boolean), and `order_id`
(a nonempty string or `None`). A malformed reference raises `ValueError`:
bad gold labels are a defect in the evaluation, not a candidate failure.

For a valid reference, return exactly `True` or `False`. A prediction passes
only if it is a dictionary with exactly the same keys and each field has the
same type and value as the reference. A missing/extra field, wrong type, or
non-dictionary prediction fails without crashing. Do not coerce `1` to `True`,
trim strings, ignore case, or silently discard fields. Key ordering is irrelevant.
Neither input may be mutated. These are explicit teaching-task choices, not
universal rules for grading extraction.

Explain a false pass that an ordinary dictionary equality check would admit,
and a false failure caused by comparing serialized JSON strings. Explain why
representation validity alone cannot establish a correct answer.

## 2. Load and validate a case set

`load_cases(path) -> list[dict]`

Read UTF-8 JSONL from a path. Each nonblank physical line is one JSON object
with exactly `id` (nonempty string), `input` (nonempty string), and `reference`
(a valid reference from task 1). IDs must be unique. Preserve file order and
string contents. Blank/whitespace-only lines are ignored but still count when
reporting physical line numbers. An empty/blank file returns `[]`.

Malformed JSON, non-object records, duplicate JSON object keys at any depth,
invalid schema, invalid reference, and duplicate case IDs raise `ValueError`
whose message includes `line N`, where N is the first bad physical line.
Do not partially accept the file or silently deduplicate it. Missing files
raise `FileNotFoundError`, preserving the distinction from invalid data.

Explain why quietly keeping the last duplicate ID or last duplicate JSON key
could change the evaluation without changing the apparent number of rows.

## 3. Report outcomes without losing failed samples

`summarize_run(scheduled_ids, results) -> dict`

`scheduled_ids` is a list of unique nonempty string IDs. `results` contains
one **terminal** result per completed case. Each is exactly:

- `{"case_id": "a", "status": "scored", "passed": true-or-false}`, or
- `{"case_id": "b", "status": "error", "error": "nonempty description"}`.

Unknown IDs, duplicate terminal results, malformed rows, invalid status,
non-Boolean `passed`, and invalid scheduled IDs raise `ValueError`.
Retries belong in separate attempt records; do not count them as new cases.
Do not mutate either input. Return exactly these fields:

| Field | Definition |
|---|---|
| scheduled | Number of scheduled case IDs |
| scored | Number of terminal scored results |
| passed | Number of scored results with `passed is True` |
| failed | Number of scored results with `passed is False` |
| errors | Number of terminal error results |
| missing | Scheduled IDs with no terminal result |
| accuracy_on_scored | passed / scored, or `None` when scored is zero |
| success_on_scheduled | passed / scheduled, or `None` when scheduled is zero |
| coverage | scored / scheduled, or `None` when scheduled is zero |

Counts are integers; defined rates are floats. Errors and missing results stay
visible. A conditional accuracy and an end-to-end success rate answer different
questions. Neither is automatically a pure estimate of model capability.

## Independent transfer checks

After practice, a tutor chooses an **unseen variant** and waits for an attempt
before showing hints or solutions. The examples below define test families;
once read, they cannot serve as your held-out cases.

1. Change the scoring schema, implement the change, and add a case that rejects
   an incorrect answer and one that accepts a valid alternative. Explain each.
2. Diagnose an unfamiliar loader that drops a malformed or duplicate record.
   Preserve useful location information and show the effect on reported results.
3. Diagnose a report that excludes failed calls from its headline denominator.
   Reconstruct counts from raw records and state what each reported rate supports.
4. Explain your function through its rule/expression dependencies. Start from
   behavior, descend into one unfamiliar expression, then return to the result.

Record the artifact/attempt, assistance, explanation, counterexample, and next
step. Revisit on a different case after another session. Passing the published
tests alone does not mark fluency or certify the full Python course.

## Course labs: shapes, hooks, manifest

The three further stubs in this directory follow the same rule: the test file
is the specification, red until implemented, no solution published.

| Stub | Test | What the tests assert |
|---|---|---|
| `shapes.py` | `test_shapes.py` | `broadcast_shape` matches NumPy on random shapes and raises on mismatch; `row_normalize`, `center_last_axis`, `masked_mean_pool` preserve shape, avoid NaN, exclude padding; `pairwise_dot` is `(n, m)`; `causal_attention_pattern` is `(b, h, q, k)`, rows sum to one, future masked to exactly zero, scaled by √d_head, stable at 1e4 |
| `hooks.py` | `test_hooks.py` | `cache_residual_stream` returns 13 `(batch, seq, 768)` float32 detached copies in order, equal to `hidden_states[0..11]` with `block.11` differing from `hidden_states[12]` by `ln_f`, and leaves no hooks behind even when the forward pass raises; `assert_cache_shapes` rejects each kind of defect |
| `manifest.py` | `test_manifest.py` | digests are stable across non-contiguous views; the manifest is deterministic, JSON-serialisable, plain ints; `check_manifest` reports, never raises, and names the tensor; `write_manifest` writes sorted UTF-8 JSON |

`test_environment.py` is not a lab; it passes as shipped and tests the machine.

### Held-out variant families for a tutor

Once read, an example cannot serve as the held-out case; these define families.

1. **A different hook target.** Cache the output of every block's MLP (or
   attention) instead of the residual stream, with the same four asserts and
   hook removal. Variants change the module, the expected shape (an MLP
   output is still `(batch, seq, 768)`; an attention pattern is
   `(batch, 12, seq, seq)` and needs `output_attentions=True` or a hook inside
   the attention module), or the normalisation of tuple outputs.
2. **A broken cache to diagnose.** Given a cache file and manifest that
   disagree (one tensor with a graph attached, one block captured twice, one
   layer off by one, padding averaged into a mean), identify the defect from
   the manifest and tests alone, then from the code. Variants change which
   defect and whether the symptom is a shape, a size on disk, or a value.
3. **A new shape function from a sentence.** "Per-head mean attention to the
   first token", "cosine similarity between every pair of positions",
   "project a cache onto k directions at once": write the test (shape first,
   then a value on a tiny hand-computable input), then the function with an
   einsum string read aloud. Variants change the sentence and the number of
   axes kept.
4. **Reconcile two toolkits.** Given a TransformerLens cache produced with an
   unknown `prepend_bos` and compatibility setting, determine both from the
   numbers alone by comparing with raw hooks, and write the manifest fields
   that would have made the comparison unnecessary. Variants change which
   setting differs and which layer.
5. **Memory budget.** Given a prompt set, a layer list and a RAM limit, choose
   batch size, dtype and which layers to cache, justify with the arithmetic,
   then run and compare the predicted and actual file size. Variants change
   the limit and the required downstream tolerance.

Record the attempt, assistance, explanation, counterexample, and next step, as
for the eval-pipeline exercises above.
