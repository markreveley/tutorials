"""Deliberately red until the new course graphs and linked pages are authored."""

import unittest

from checks import COURSES, HERE, check_course, check_pages, read_json


class CourseAcceptanceTests(unittest.TestCase):
    def check(self, language):
        root = COURSES / language / f"{language}-tut"
        course = read_json(root / "dag/course.json")
        check_course(course, language, read_json(HERE / "fixtures/beatcode.lock.json"))
        check_pages(course, root)

    def test_python_course_supports_eval_fluency(self):
        self.check("python")

    def test_rust_course_supports_reading_beatcode(self):
        self.check("rust")


if __name__ == "__main__":
    unittest.main()
