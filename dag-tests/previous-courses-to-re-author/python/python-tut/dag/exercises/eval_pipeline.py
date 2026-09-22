"""First eval-focused fluency assessment. Implement from the assessment brief.

Run from the repository root:
python3 -m unittest discover -s evals/courses/dag-tests -p 'test_python_evals.py' -v
"""


def score_ticket(prediction, reference):
    """Return a strict Boolean for exact-schema, exact-type ticket extraction."""
    raise NotImplementedError("Implement score_ticket after attempting its behavior tests")


def load_cases(path):
    """Read validated JSONL cases; reject bad lines and duplicate case ids."""
    raise NotImplementedError("Implement load_cases after attempting its behavior tests")


def summarize_run(scheduled_ids, results):
    """Account for every scheduled case, including errors and missing results."""
    raise NotImplementedError("Implement summarize_run after attempting its behavior tests")
