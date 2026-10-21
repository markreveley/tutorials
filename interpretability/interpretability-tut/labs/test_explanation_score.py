"""Held-out explanation scoring with controls (lessons 04 and 05)."""
import unittest

import numpy as np

from _impl import load

E = load('explanation_score')


def synthetic(seed=0, n=2000, units=50):
    """Unit 0 fires on digits (with noise); unit 1 fires on capitals; others are noise."""
    rng = np.random.default_rng(seed)
    vocab = [' 12', ' 7', ' 1911', ' Alice', ' Bob', ' the', ' kettle', ',', '.', ' of']
    toks = [vocab[i] for i in rng.integers(0, len(vocab), size=n)]
    digit = np.array([t.strip().isdigit() for t in toks], dtype=float)
    capital = np.array([t.strip()[:1].isupper() for t in toks], dtype=float)
    acts = rng.normal(0, 0.2, size=(n, units))
    acts[:, 0] += 2.0 * digit
    acts[:, 1] += 1.5 * capital
    return toks, acts, digit, capital


class ScoringChecks(unittest.TestCase):
    def test_pearson_known_values_and_degenerate_input(self):
        self.assertAlmostEqual(E.pearson([1, 2, 3, 4], [2, 4, 6, 8]), 1.0)
        self.assertAlmostEqual(E.pearson([1, 2, 3, 4], [8, 6, 4, 2]), -1.0)
        self.assertAlmostEqual(E.pearson([1, 2, 3, 4], [1, 3, 2, 4]), 0.8)
        self.assertEqual(E.pearson([1, 1, 1], [1, 2, 3]), 0.0)
        with self.assertRaises(ValueError):
            E.pearson([1, 2], [1, 2, 3])

    def test_split_alternates_and_never_overlaps(self):
        train, test = E.split_chunks(800, 128)  # 6 full chunks; the partial tail is dropped
        self.assertEqual(train, [(0, 128), (256, 384), (512, 640)])
        self.assertEqual(test, [(128, 256), (384, 512), (640, 768)])
        covered = sorted(i for a, b in train + test for i in range(a, b))
        self.assertEqual(covered, list(range(768)))
        self.assertEqual(E.split_chunks(100, 128), ([], []))

    def test_rule_predictions_regex_and_callable(self):
        toks = [' 12', ' Alice', '.', ' 7']
        np.testing.assert_array_equal(E.rule_predictions(toks, r'^\s*\d+$'), [1, 0, 0, 1])
        after_dot = lambda t, prev: prev.strip().endswith('.')
        np.testing.assert_array_equal(E.rule_predictions(toks, after_dot), [0, 0, 0, 1])

    def test_true_explanation_scores_high_and_passes(self):
        toks, acts, digit, _ = synthetic()
        preds = E.rule_predictions(toks, r'^\s*\d+$')
        np.testing.assert_array_equal(preds, digit)
        r = E.score_explanation(acts[:, 0], preds)
        self.assertGreater(r, 0.9)
        rand = E.random_unit_control(acts, preds, unit=0, n=40, seed=1)
        shuf = E.shuffled_control(acts[:, 0], preds, n=100, seed=1)
        self.assertEqual(len(rand), 40); self.assertEqual(len(shuf), 100)
        # Unit 1 (capitals) is anti-correlated with digits, so allow a modest negative tail.
        self.assertLess(np.percentile(rand, 95), 0.2)
        self.assertLess(np.abs(rand).max(), 0.4)
        self.assertLess(np.abs(shuf).max(), 0.2)
        self.assertTrue(E.verdict(r, rand, shuf, threshold=0.5)['demonstrated'])

    def test_wrong_explanation_of_a_real_unit_is_not_demonstrated(self):
        toks, acts, _, capital = synthetic()
        preds = E.rule_predictions(toks, r'^\s*[A-Z]')
        r = E.score_explanation(acts[:, 0], preds)  # capital rule against the digit unit
        rand = E.random_unit_control(acts, preds, unit=0, n=49, seed=2)  # every other unit
        shuf = E.shuffled_control(acts[:, 0], preds, n=100, seed=2)
        self.assertFalse(E.verdict(r, rand, shuf, threshold=0.5)['demonstrated'])
        # The random-unit control catches it: unit 1 really does carry this rule.
        self.assertGreater(np.max(rand), 0.5)

    def test_random_unit_control_excludes_the_unit_itself(self):
        toks, acts, digit, _ = synthetic(units=3)
        rand = E.random_unit_control(acts, digit, unit=0, n=10, seed=0)
        self.assertEqual(len(rand), 2)
        self.assertLess(np.abs(rand).max(), 0.5)  # unit 1 anti-correlates mildly

    def test_verdict_reports_control_percentiles(self):
        v = E.verdict(0.6, np.linspace(-0.1, 0.1, 100), np.linspace(-0.05, 0.05, 100), threshold=0.5)
        self.assertAlmostEqual(v['random_p95'], 0.09, places=2)
        self.assertTrue(v['demonstrated'])
        self.assertFalse(E.verdict(0.6, np.full(10, 0.7), np.zeros(10), threshold=0.5)['demonstrated'])


if __name__ == '__main__':
    unittest.main()
