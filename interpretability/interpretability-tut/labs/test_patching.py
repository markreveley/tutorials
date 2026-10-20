"""Activation patching, model-free parts (lesson 10)."""
import unittest

import torch

from _impl import load

A = load('patching')


class PatchingChecks(unittest.TestCase):
    def test_recovered_fraction(self):
        self.assertAlmostEqual(A.recovered_fraction(1.0, -4.0, -4.0), 0.0)
        self.assertAlmostEqual(A.recovered_fraction(1.0, -4.0, 1.0), 1.0)
        self.assertAlmostEqual(A.recovered_fraction(1.0, -4.0, -1.5), 0.5)
        self.assertAlmostEqual(A.recovered_fraction(1.0, -4.0, -6.5), -0.5)
        with self.assertRaises(ValueError):
            A.recovered_fraction(2.0, 2.0, 2.0)

    def test_hook_overwrites_only_the_named_position(self):
        clean = torch.arange(2 * 5 * 3, dtype=torch.float32).reshape(2, 5, 3)
        running = torch.zeros(2, 5, 3)
        hook = A.make_patch_hook(clean, position=2)
        out = hook(running, None)
        self.assertTrue(torch.equal(out[:, 2, :], clean[:, 2, :]))
        mask = torch.ones(5, dtype=torch.bool); mask[2] = False
        self.assertTrue(torch.equal(out[:, mask, :], torch.zeros(2, 4, 3)))
        self.assertIs(out, running)

    def test_verdict_with_claim_and_control_positions(self):
        table = {0: [0.0, 0.0, 0.95, 0.1], 1: [0.02, 0.0, 0.6, 0.3], 2: [0.0, 0.0, 0.1, 0.9]}
        v = A.verdict(table, claim_position=2, control_position=0)
        self.assertTrue(v['passed']); self.assertAlmostEqual(v['best_claim'], 0.95)
        v = A.verdict(table, claim_position=1, control_position=0)
        self.assertFalse(v['claim_passed'])
        table[1][0] = 0.5
        self.assertFalse(A.verdict(table, claim_position=2, control_position=0)['control_passed'])


if __name__ == '__main__':
    unittest.main()
