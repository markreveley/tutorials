"""Induction-head detection on repeated random tokens (lesson 11)."""
import unittest

import torch

from _impl import load

I = load('induction')


def perfect_induction_pattern(seq, heads=2):
    """Head 0 attends exactly to the induction target; head 1 attends uniformly."""
    n = 2 * seq + 1
    pat = torch.zeros(heads, n, n)
    for i in range(n):
        pat[1, i, :i + 1] = 1.0 / (i + 1)
        if i >= seq + 1:
            pat[0, i, i - seq + 1] = 1.0
        else:
            pat[0, i, 0] = 1.0
    return pat


class InductionChecks(unittest.TestCase):
    def test_sequences_have_the_right_shape_and_structure(self):
        rep = I.repeated_sequence(50, seed=0, bos_id=50256)
        self.assertEqual(tuple(rep.shape), (1, 101))
        self.assertEqual(int(rep[0, 0]), 50256)
        self.assertTrue(torch.equal(rep[0, 1:51], rep[0, 51:]))
        ctrl = I.control_sequence(50, seed=0, bos_id=50256)
        self.assertTrue(torch.equal(ctrl[0, :51], rep[0, :51]))
        self.assertFalse(torch.equal(ctrl[0, 51:], rep[0, 51:]))
        self.assertTrue(torch.equal(I.repeated_sequence(50, 0, 50256), I.repeated_sequence(50, 0, 50256)))
        self.assertFalse(torch.equal(I.repeated_sequence(50, 0, 50256), I.repeated_sequence(50, 1, 50256)))

    def test_prefix_matching_score_on_synthetic_patterns(self):
        seq = 20
        s = I.prefix_matching_score(perfect_induction_pattern(seq), seq)
        self.assertEqual(tuple(s.shape), (2,))
        self.assertAlmostEqual(float(s[0]), 1.0, places=6)
        self.assertLess(float(s[1]), 0.06)

    def test_verdict(self):
        rep = torch.zeros(3, 4); ctrl = torch.zeros(3, 4)
        rep[1, 2] = 0.9
        v = I.verdict(rep, ctrl, loss_first=10.0, loss_second=1.0)
        self.assertEqual(v['heads'], [(1, 2)]); self.assertTrue(v['passed'])
        ctrl[1, 2] = 0.5
        self.assertFalse(I.verdict(rep, ctrl, 10.0, 1.0)['passed'])
        ctrl[1, 2] = 0.0
        self.assertFalse(I.verdict(rep, ctrl, 1.0, 10.0)['passed'])
        self.assertFalse(I.verdict(torch.zeros(3, 4), ctrl, 10.0, 1.0)['passed'])


if __name__ == '__main__':
    unittest.main()
