"""Regression checks for the learner's start/resume flow, in temporary copies."""
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import curriculum


class StartFlowTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        root = Path(self.workspace.name).resolve()
        for folder in ("curriculum", "templates"):
            shutil.copytree(curriculum.ROOT / folder, root / folder)
        self.root_patch = patch.object(curriculum, "ROOT", root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.manifest = curriculum.read_json("curriculum/manifest.json")
        self.progress = curriculum.read_json("curriculum/progress.json")

    def test_every_lesson_links_to_instructions_without_copying_them(self):
        for lesson in self.manifest["lessons"]:
            with self.subTest(lesson=lesson["id"]):
                progress = json.loads(json.dumps(self.progress))
                # Satisfy prerequisite gates only in the isolated start fixture.
                for state in progress["lessons"].values():
                    state.update(status="completed", attempts=[])
                state = progress["lessons"][lesson["id"]]
                state["status"] = "not_started"
                output = StringIO()
                with redirect_stdout(output):
                    curriculum.start(lesson["id"], self.manifest, progress)
                record = curriculum.local_path(state["attempts"][0]["session"]).read_text()
                authored = curriculum.local_path(lesson["path"]).read_text()
                for heading in ("Concept", "Predict before reading"):
                    expected = authored.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0].strip()
                    self.assertNotIn(expected, record)
                    self.assertNotIn(expected, output.getvalue())
                self.assertIn("../../" + lesson["path"] + "#predict-before-reading", record)
                if lesson.get("delivery") == "agent-led":
                    self.assertIn("Continue in the conversation", output.getvalue())
                    self.assertIn(lesson["path"] + "#todays-path", output.getvalue())
                    self.assertEqual(state["attempts"][0]["step"], "purpose")
                else:
                    self.assertIn(lesson["path"] + "#predict-before-reading", output.getvalue())
                self.assertIn("**Your response:**", record)
                self.assertNotIn("{{", record)
                self.assertEqual(state["status"], "in_progress")
                self.assertEqual(state["attempts"][0]["independent_check"], "not_attempted")
                self.assertEqual(state["attempts"][0]["evidence"], [])
                self.assertNotIn("minutes", state["attempts"][0])
                self.assertNotIn("Planned core:", record)
                self.assertEqual(progress["capabilities"], self.progress["capabilities"])

    def test_resume_preserves_answer_and_does_not_order_prediction_again(self):
        lesson = self.manifest["lessons"][0]
        state = self.progress["lessons"][lesson["id"]]
        state.update(status="in_progress", attempts=[{
            "session": "sessions/M1-01/attempt-01.md",
            "independent_check": "not_attempted", "evidence": [],
        }])
        record = curriculum.local_path(state["attempts"][-1]["session"])
        record.parent.mkdir(parents=True)
        original = "Learner response sentinel\nHandover: reading is next.\n"
        record.write_text(original)
        before = json.dumps(self.progress, sort_keys=True)
        output = StringIO()
        with redirect_stdout(output):
            curriculum.start(lesson["id"], self.manifest, self.progress)
        self.assertEqual(record.read_text(), original)
        self.assertEqual(json.dumps(self.progress, sort_keys=True), before)
        self.assertIn("Resuming:", output.getvalue())
        self.assertNotIn("Next action: write", output.getvalue())

    def test_agent_resume_preserves_saved_step_and_answers(self):
        lesson = self.manifest["lessons"][0]
        state = self.progress["lessons"][lesson["id"]]
        state.update(status="in_progress", attempts=[{
            "session": "sessions/M1-01/attempt-02.md",
            "independent_check": "not_attempted", "evidence": [], "step": "explain",
        }])
        record = curriculum.local_path(state["attempts"][-1]["session"])
        record.parent.mkdir(parents=True)
        original = "Actual learner answer remains here.\n"
        record.write_text(original)
        before = json.dumps(self.progress, sort_keys=True)
        output = StringIO()
        with redirect_stdout(output):
            curriculum.start(lesson["id"], self.manifest, self.progress)
        self.assertIn("Resuming: Explain the observed result", output.getvalue())
        self.assertIn("#explain-the-observed-result", output.getvalue())
        self.assertNotIn("First session:", output.getvalue())
        self.assertEqual(json.dumps(self.progress, sort_keys=True), before)
        self.assertEqual(record.read_text(), original)

    def test_blank_prompt_is_rejected_before_creating_an_attempt(self):
        lesson = self.manifest["lessons"][0]
        curriculum.local_path(lesson["path"]).write_text(
            "## Concept\nA baseline.\n\n## Predict before reading\n\n## Exercise\n"
        )
        self.progress["lessons"][lesson["id"]].update(status="not_started", attempts=[])
        with self.assertRaisesRegex(ValueError, "missing or empty section Predict before reading"):
            curriculum.start(lesson["id"], self.manifest, self.progress)
        self.assertFalse((curriculum.ROOT / "sessions").exists())

    def test_completion_needs_evidence_and_independent_pass_without_time_fields(self):
        for state in self.progress["lessons"].values():
            state.update(status="not_started", attempts=[])
        for state in self.progress["capabilities"].values():
            state.update(status="not_assessed", evidence=[])
        record = curriculum.ROOT / "sessions/M1-01/attempt-01.md"
        record.parent.mkdir(parents=True)
        record.write_text("Isolated validation fixture; not learner evidence.\n")
        evidence = curriculum.ROOT / "fixture.txt"
        evidence.write_text("Isolated artifact fixture.\n")
        attempt = {
            "session": "sessions/M1-01/attempt-01.md", "date": "2026-09-09",
            "assistance": "independent", "independent_check": "passed",
            "evidence": ["fixture.txt"],
        }
        self.progress["lessons"]["M1-01"].update(status="completed", attempts=[attempt])
        progress_file = curriculum.ROOT / "curriculum/progress.json"
        # Link validation is separate; this fixture copies only curriculum files.
        with patch.object(curriculum, "check_local_links"):
            progress_file.write_text(json.dumps(self.progress))
            curriculum.validate()
            for result, paths in [("not_attempted", ["fixture.txt"]), ("passed", [])]:
                with self.subTest(result=result, evidence=paths):
                    attempt.update(independent_check=result, evidence=paths)
                    progress_file.write_text(json.dumps(self.progress))
                    with self.assertRaisesRegex(ValueError, "independent pass and evidence"):
                        curriculum.validate()

    def test_agent_step_must_reference_an_existing_heading(self):
        self.manifest["lessons"][0]["steps"]["explain"] = "Missing heading"
        curriculum.local_path("curriculum/manifest.json").write_text(
            json.dumps(self.manifest)
        )
        with self.assertRaisesRegex(ValueError, "has no lesson heading"):
            curriculum.validate()

    def test_invalid_saved_step_is_rejected(self):
        for state in self.progress["lessons"].values():
            for attempt in state["attempts"]:
                record = curriculum.local_path(attempt["session"])
                record.parent.mkdir(parents=True, exist_ok=True)
                record.write_text("Isolated test record, not learner evidence.\n")
                attempt["evidence"] = []
        self.progress["lessons"]["M1-01"]["attempts"][-1]["step"] = "made-up"
        curriculum.local_path("curriculum/progress.json").write_text(json.dumps(self.progress))
        with self.assertRaisesRegex(ValueError, "invalid saved step"):
            curriculum.validate()

    def test_pilot_has_no_baseline_or_rust_completion_requirement(self):
        lesson = self.manifest["lessons"][0]
        self.assertEqual(lesson["artifacts"], ["sessions/M1-01/"])
        self.assertNotIn("book1", lesson["resources"])
        first_rust_lesson = self.manifest["lessons"][4]
        self.assertIn("book1", first_rust_lesson["resources"])
        self.assertNotIn("Rust", curriculum.lesson_section(lesson, "Exit criteria"))
        self.assertNotIn("staging", curriculum.lesson_section(lesson, "Exit criteria"))


if __name__ == "__main__":
    unittest.main()
