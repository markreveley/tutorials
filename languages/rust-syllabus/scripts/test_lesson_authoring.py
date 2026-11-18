"""Authoring regressions: these checks never run a learner exercise."""
import json
from contextlib import redirect_stdout
from io import StringIO
import re
import subprocess
import unittest
from unittest.mock import patch

import curriculum
import m1_01_preflight
import m1_04_preflight


class LessonAuthoringTests(unittest.TestCase):
    def test_optional_m1_01_report_does_not_check_rust(self):
        output = StringIO()
        with patch.object(m1_01_preflight, "version", return_value="git test") as version:
            with redirect_stdout(output):
                m1_01_preflight.main()
        self.assertEqual(set(json.loads(output.getvalue())), {
            "os", "architecture", "python", "git",
        })
        version.assert_called_once_with(["git", "--version"])

    def test_remaining_lessons_use_their_own_preflight(self):
        for number in range(2, 31):
            key = f"{number:02}"
            with self.subTest(lesson=key):
                lesson = (curriculum.ROOT / f"curriculum/month-01/lessons/{key}.md").read_text()
                preflight = curriculum.ROOT / f"curriculum/month-01/preflight/{key}.md"
                self.assertIn(f"../preflight/{key}.md", lesson)
                self.assertTrue(preflight.is_file())
                setup = preflight.read_text()
                self.assertTrue(setup.startswith(f"# M1-{key} preflight\n"))
                self.assertNotIn("lab-setup.md", lesson + setup)
                self.assertNotIn("scripts/preflight.py", lesson + setup)
                self.assertNotRegex(setup, r"preflight/\d\d\.md")
                self.assertIn("## Return to the lesson", setup)
                if "Use the Ubuntu VM" in lesson:
                    self.assertIn("## Save work and return to your Mac", setup)
                    self.assertIn("git merge --ff-only FETCH_HEAD", setup)

    def test_manifest_artifacts_are_listed_in_commit_section(self):
        manifest = curriculum.read_json("curriculum/manifest.json")
        for lesson in manifest["lessons"][1:]:
            with self.subTest(lesson=lesson["id"]):
                source = curriculum.local_path(lesson["path"]).read_text()
                commit = source.split("## Required artifacts and commit\n")[1].split("\n## ")[0]
                for artifact in lesson["artifacts"]:
                    self.assertIn(f"`{artifact}`", commit)
                    self.assertNotIn(" or ", artifact)

    def test_shell_examples_parse_without_execution(self):
        base = curriculum.ROOT / "curriculum/month-01"
        for folder in ("lessons", "preflight"):
            for path in sorted((base / folder).glob("*.md")):
                blocks = re.findall(r"^```(?:sh|bash)\n(.*?)^```$", path.read_text(), re.M | re.S)
                for index, block in enumerate(blocks):
                    with self.subTest(file=path.name, folder=folder, block=index):
                        checked = subprocess.run(
                            ["/bin/bash", "-n"], input=block, text=True,
                            capture_output=True, check=False,
                        )
                        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_m1_04_inventory_is_process_specific_and_non_linux_is_honest(self):
        with patch.object(m1_04_preflight.platform, "system", return_value="Darwin"), \
             patch.object(m1_04_preflight, "version", return_value="git test"), \
             patch.object(m1_04_preflight.os, "geteuid", return_value=501), \
             patch.object(m1_04_preflight.os, "access", return_value=False):
            report = m1_04_preflight.inventory()
        self.assertEqual(set(report), {
            "os", "architecture", "distribution", "distribution_version",
            "running_as_root", "python", "git", "ps", "proc_status_readable",
        })
        self.assertEqual(report["os"], "Darwin")
        self.assertIsNone(report["distribution"])
        self.assertIsNone(report["ps"])
        self.assertFalse(report["proc_status_readable"])

    def test_m1_04_linux_values_are_read_without_future_capabilities(self):
        with patch.object(m1_04_preflight.platform, "system", return_value="Linux"), \
             patch.object(m1_04_preflight.platform, "freedesktop_os_release",
                          return_value={"ID": "ubuntu", "VERSION_ID": "24.04"}), \
             patch.object(m1_04_preflight, "version", side_effect=["git test", "ps test"]), \
             patch.object(m1_04_preflight.os, "geteuid", return_value=1000), \
             patch.object(m1_04_preflight.os, "access", return_value=True):
            report = m1_04_preflight.inventory()
        self.assertEqual(report["distribution_version"], "24.04")
        self.assertEqual(report["ps"], "ps test")
        self.assertFalse(report["running_as_root"])
        self.assertTrue(report["proc_status_readable"])
        json.dumps(report)


if __name__ == "__main__":
    unittest.main()
