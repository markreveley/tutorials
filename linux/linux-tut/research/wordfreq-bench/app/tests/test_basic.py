import unittest
from wordfreq import top


class Basic(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(top("a b a", 1), [("a", 2)])


if __name__ == "__main__":
    unittest.main()
