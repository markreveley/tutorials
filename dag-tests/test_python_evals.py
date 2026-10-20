"""Public fluency exercises. RED on the supplied stubs; no reference solution here."""

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from checks import COURSES

IMPLEMENTATION = COURSES / "python/python-tut/labs/eval_pipeline.py"
spec = importlib.util.spec_from_file_location("eval_pipeline", IMPLEMENTATION)
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)


def reference(**changes):
    return {"category": "refund", "urgent": True, "order_id": "A-42", **changes}


def case(case_id="ticket-1", **changes):
    return {"id": case_id, "input": "Refund order A-42 urgently, please.",
            "reference": reference(), **changes}


class ScorerTests(unittest.TestCase):
    def test_accepts_exact_answer_without_relying_on_key_order(self):
        gold = reference()
        actual = pipeline.score_ticket(dict(reversed(list(gold.items()))), gold)
        self.assertIs(actual, True)

    def test_accepts_null_order_id_and_false_urgency(self):
        gold = reference(order_id=None, urgent=False)
        self.assertIs(pipeline.score_ticket(copy.deepcopy(gold), gold), True)

    def test_rejects_incorrect_values_and_representation(self):
        bad_predictions = [
            None, [], "refund", {},
            {"category": "refund", "urgent": True},
            reference(extra="ignored?"), reference(category="billing"),
            reference(category="REFUND"), reference(category="refund "),
            reference(order_id=42), reference(order_id=None), reference(urgent=False),
            reference(urgent=1), reference(urgent="true"),
        ]
        for prediction in bad_predictions:
            with self.subTest(prediction=prediction):
                self.assertIs(pipeline.score_ticket(prediction, reference()), False)

    def test_python_equal_values_can_still_have_wrong_types(self):
        self.assertEqual(reference(urgent=1), reference())  # Demonstrates the trap.
        self.assertIs(pipeline.score_ticket(reference(urgent=1), reference()), False)
        self.assertIs(pipeline.score_ticket(reference(urgent=0), reference(urgent=False)), False)

    def test_invalid_gold_is_an_evaluation_error(self):
        bad_references = [None, [], {}, reference(extra=1), reference(category=""),
                          reference(category=9), reference(urgent=1), reference(order_id=42),
                          reference(order_id="")]
        for gold in bad_references:
            with self.subTest(gold=gold), self.assertRaises(ValueError):
                pipeline.score_ticket(reference(), gold)

    def test_does_not_mutate_candidate_or_reference_even_on_rejection(self):
        for prediction in (reference(), reference(extra="do not delete me")):
            gold = reference()
            before = copy.deepcopy((prediction, gold))
            pipeline.score_ticket(prediction, gold)
            self.assertEqual((prediction, gold), before)


class LoaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "cases.jsonl"

    def load(self, text):
        self.path.write_text(text, encoding="utf-8")
        return pipeline.load_cases(self.path)

    def test_reads_utf8_preserves_order_and_ignores_blank_lines(self):
        rows = [case("b", input="Où est ma commande ?"), case("a", reference=reference(order_id=None))]
        text = "\n" + json.dumps(rows[0], ensure_ascii=False) + "\n \t\n" + json.dumps(rows[1])
        self.assertEqual(self.load(text), rows)

    def test_empty_dataset_is_explicit(self):
        self.assertEqual(self.load("\n \t\n"), [])

    def test_bad_json_reports_physical_line_not_record_index(self):
        with self.assertRaisesRegex(ValueError, r"\bline 3\b"):
            self.load(json.dumps(case()) + "\n\n{bad json}")

    def test_duplicate_case_id_is_not_silently_deduplicated(self):
        text = json.dumps(case()) + "\n" + json.dumps(case(input="A different input"))
        with self.assertRaisesRegex(ValueError, r"\bline 2\b"):
            self.load(text)

    def test_rejects_invalid_record_and_reference_schema(self):
        bad_rows = [None, [], "text", {}, case(""), case(7), case(input=2), case(input=""),
                    case(extra=True), case(reference=reference(urgent=1)),
                    case(reference=reference(order_id=[])), case(reference=reference(category=""))]
        for row in bad_rows:
            with self.subTest(row=row), self.assertRaisesRegex(ValueError, r"\bline 2\b"):
                self.load(json.dumps(case()) + "\n" + json.dumps(row))

    def test_duplicate_json_keys_are_rejected_at_both_depths(self):
        texts = [
            '{"id":"a","id":"b","input":"ticket","reference":{"category":"refund","urgent":true,"order_id":null}}',
            '{"id":"a","input":"ticket","reference":{"category":"refund","urgent":true,"urgent":false,"order_id":null}}',
        ]
        for text in texts:
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, r"\bline 1\b"):
                self.load(text)

    def test_missing_file_is_distinct_from_invalid_data(self):
        with self.assertRaises(FileNotFoundError):
            pipeline.load_cases(self.path)


class ReportingTests(unittest.TestCase):
    def assert_summary(self, scheduled, rows, expected):
        before = copy.deepcopy((scheduled, rows))
        result = pipeline.summarize_run(scheduled, rows)
        self.assertEqual(result, expected)
        self.assertEqual((scheduled, rows), before)
        for field in ("scheduled", "scored", "passed", "failed", "errors", "missing"):
            self.assertIs(type(result[field]), int)
        for field in ("accuracy_on_scored", "success_on_scheduled", "coverage"):
            if result[field] is not None:
                self.assertIs(type(result[field]), float)
        self.assertEqual(result["passed"] + result["failed"], result["scored"])
        self.assertEqual(result["scored"] + result["errors"] + result["missing"], result["scheduled"])

    def test_denominators_keep_failed_calls_and_missing_cases_visible(self):
        rows = [{"case_id": "a", "status": "scored", "passed": True},
                {"case_id": "b", "status": "scored", "passed": False},
                {"case_id": "c", "status": "error", "error": "timeout"}]
        self.assert_summary(["a", "b", "c", "d"], rows, {
            "scheduled": 4, "scored": 2, "passed": 1, "failed": 1, "errors": 1, "missing": 1,
            "accuracy_on_scored": 0.5, "success_on_scheduled": 0.25, "coverage": 0.5})

    def test_empty_run_does_not_claim_perfect_accuracy(self):
        self.assert_summary([], [], {
            "scheduled": 0, "scored": 0, "passed": 0, "failed": 0, "errors": 0, "missing": 0,
            "accuracy_on_scored": None, "success_on_scheduled": None, "coverage": None})

    def test_all_errors_leave_conditional_accuracy_undefined(self):
        self.assert_summary(["a"], [{"case_id": "a", "status": "error", "error": "timeout"}], {
            "scheduled": 1, "scored": 0, "passed": 0, "failed": 0, "errors": 1, "missing": 0,
            "accuracy_on_scored": None, "success_on_scheduled": 0.0, "coverage": 0.0})

    def test_no_terminal_results_are_counted_as_missing(self):
        self.assert_summary(["a", "b"], [], {
            "scheduled": 2, "scored": 0, "passed": 0, "failed": 0, "errors": 0, "missing": 2,
            "accuracy_on_scored": None, "success_on_scheduled": 0.0, "coverage": 0.0})

    def test_run_order_does_not_change_summary(self):
        rows = [{"case_id": "b", "status": "scored", "passed": False},
                {"case_id": "a", "status": "scored", "passed": True}]
        forward = pipeline.summarize_run(["a", "b"], rows)
        reverse = pipeline.summarize_run(["b", "a"], rows[::-1])
        self.assertEqual(forward, reverse)

    def test_duplicate_terminal_result_cannot_inflate_sample_size(self):
        row = {"case_id": "a", "status": "scored", "passed": True}
        with self.assertRaises(ValueError):
            pipeline.summarize_run(["a"], [row, dict(row)])

    def test_unknown_case_cannot_join_the_denominator(self):
        with self.assertRaises(ValueError):
            pipeline.summarize_run(["a"], [{"case_id": "b", "status": "scored", "passed": True}])

    def test_bad_terminal_rows_are_rejected(self):
        rows = [None, {}, {"case_id": "a", "status": "scored"},
                {"case_id": "a", "status": "scored", "passed": 1},
                {"case_id": "a", "status": "pending"},
                {"case_id": "a", "status": "error", "error": ""},
                {"case_id": "a", "status": "error", "error": "timeout", "passed": False},
                {"case_id": "a", "status": "scored", "passed": True, "attempt": 2}]
        for row in rows:
            with self.subTest(row=row), self.assertRaises(ValueError):
                pipeline.summarize_run(["a"], [row])

    def test_invalid_schedule_is_rejected(self):
        for schedule in (["a", "a"], [""], [7], [True]):
            with self.subTest(schedule=schedule), self.assertRaises(ValueError):
                pipeline.summarize_run(schedule, [])


if __name__ == "__main__":
    unittest.main()
