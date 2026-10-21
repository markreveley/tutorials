"""Linear probe with shuffled-label and random-direction controls (lesson 08)."""
import unittest

import numpy as np

from _impl import load

B = load('probe')


def data(seed=0, n=600, d=20, signal=4.0):
    """Label depends on one hidden direction; the rest is noise. 15% positives."""
    direction = np.random.default_rng(12345).standard_normal(d); direction /= np.linalg.norm(direction)
    rng = np.random.default_rng(seed)
    y = (rng.random(n) < 0.15).astype(float)
    x = rng.standard_normal((n, d)) + signal * np.outer(y - 0.15, direction)
    return x, y


class ProbeChecks(unittest.TestCase):
    def test_majority_rate(self):
        self.assertAlmostEqual(B.majority_rate([0, 0, 0, 1]), 0.75)
        self.assertAlmostEqual(B.majority_rate([1, 1, 1, 0]), 0.75)

    def test_probe_recovers_a_linear_label_on_held_out_data(self):
        xtr, ytr = data(0); xte, yte = data(1)
        probe = B.fit_logistic(xtr, ytr)
        self.assertEqual(B.predict(probe, xte).shape, (len(yte),))
        self.assertGreater(B.accuracy(probe, xte, yte), 0.95)
        self.assertGreater(B.accuracy(probe, xte, yte), B.majority_rate(yte) + 0.05)

    def test_shuffled_labels_fall_to_about_the_majority_rate(self):
        xtr, ytr = data(0); xte, yte = data(1)
        shuf = B.shuffled_label_control(xtr, ytr, xte, yte, n=8, seed=0)
        self.assertEqual(len(shuf), 8)
        self.assertLess(np.max(shuf), B.majority_rate(yte) + 0.03)

    def test_random_direction_rarely_beats_the_probe(self):
        xtr, ytr = data(0); xte, yte = data(1)
        probe_acc = B.accuracy(B.fit_logistic(xtr, ytr), xte, yte)
        rand = B.random_direction_control(xtr, ytr, xte, yte, n=8, seed=0)
        self.assertEqual(len(rand), 8)
        self.assertLess(np.max(rand), probe_acc)

    def test_no_signal_means_no_pass(self):
        xtr, ytr = data(0, signal=0.0); xte, yte = data(1, signal=0.0)
        acc = B.accuracy(B.fit_logistic(xtr, ytr), xte, yte)
        shuf = B.shuffled_label_control(xtr, ytr, xte, yte, n=5, seed=0)
        rand = B.random_direction_control(xtr, ytr, xte, yte, n=5, seed=0)
        self.assertFalse(B.verdict(acc, B.majority_rate(yte), shuf, rand)['passed'])

    def test_verdict_logic(self):
        v = B.verdict(0.95, 0.80, np.array([0.80, 0.79]), np.array([0.82, 0.81]))
        self.assertTrue(v['passed'])
        self.assertFalse(B.verdict(0.89, 0.80, np.array([0.80]), np.array([0.82]))['passed'])
        self.assertFalse(B.verdict(0.95, 0.80, np.array([0.96]), np.array([0.82]))['passed'])


if __name__ == '__main__':
    unittest.main()
