# Python: implement, debug, and explain an evaluation

These are the first learner tests for the [DAG redesign](../../../../dag-tests/README.md).
They are public practice cases. There is no recorded learner attempt yet.
Use standard-library Python and ordinary documentation. Implement the three
functions in [eval_pipeline.py](../exercises/eval_pipeline.py); no API calls,
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
