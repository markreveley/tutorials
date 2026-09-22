import json
import os
import unittest
from wordfreq import top

HERE = os.path.dirname(os.path.abspath(__file__))


class Hidden(unittest.TestCase):
    def test_case_and_punctuation(self):
        with open(os.path.join(HERE, "expected.json"), encoding="utf-8") as f:
            expected = [tuple(pair) for pair in json.load(f)["sample_top3"]]
        with open(os.path.join(os.environ.get("APP_DIR", "/app"), "data/sample.txt"), encoding="utf-8") as f:
            self.assertEqual(top(f.read(), 3), expected)

    def test_apostrophes_stay_inside_words(self):
        self.assertEqual(top("don't stop. Don't!", 1), [("don't", 2)])


if __name__ == "__main__":
    unittest.main()
