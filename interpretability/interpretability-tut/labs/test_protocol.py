"""Behaviour of the pre-registration protocol (lesson 01)."""
import unittest

import numpy as np

from _impl import load

P = load('protocol')


def complete():
    return P.Preregistration(
        claim='neuron L2/2928 fires on the first token of a sentence',
        unit='gpt2-small blocks.2.mlp.hook_post[:, 2928]',
        heldout_data='odd 128-token chunks of labs/data/corpus.txt, never used for screening',
        scoring='Pearson r between the rule indicator and the activation over held-out tokens',
        prediction='r >= 0.5', threshold=0.5,
        controls=['random_unit', 'shuffled_labels'],
        failure_means='the rule is not a demonstrated explanation of this neuron')


class ProtocolChecks(unittest.TestCase):
    def test_complete_protocol_validates(self):
        self.assertEqual(P.validate(complete()), [])

    def test_missing_and_placeholder_fields_are_named(self):
        p = complete(); p.claim = ''; p.scoring = 'TODO'; p.threshold = None
        problems = P.validate(p)
        for name in ('claim', 'scoring', 'threshold'):
            self.assertTrue(any(name in x for x in problems), name)
        self.assertFalse(any('unit' in x for x in problems))

    def test_fewer_than_two_controls_is_a_problem(self):
        p = complete(); p.controls = ['random_unit']
        self.assertTrue(any('controls' in x for x in P.validate(p)))
        p.controls = []
        self.assertTrue(any('controls' in x for x in P.validate(p)))

    def test_looking_first_is_a_problem(self):
        p = complete(); p.looked_already = True
        self.assertTrue(any('looked' in x for x in P.validate(p)))

    def test_run_refuses_incomplete_protocol_without_running(self):
        calls = []
        def experiment():
            calls.append(1); return 0.9, {'random_unit': [0.1], 'shuffled_labels': [0.0]}
        p = complete(); p.prediction = '...'
        with self.assertRaises(P.ProtocolError):
            P.run(p, experiment)
        self.assertEqual(calls, [])

    def test_run_requires_the_preregistered_controls_to_be_reported(self):
        def experiment():
            return 0.9, {'random_unit': [0.1, 0.2]}
        with self.assertRaises(P.ProtocolError):
            P.run(complete(), experiment)

    def test_judge_needs_threshold_and_beats_controls(self):
        rng = np.random.default_rng(0)
        noise = rng.normal(0, 0.05, size=500)
        self.assertEqual(P.judge(0.8, {'a': noise, 'b': noise}, 0.5), 'demonstrated')
        self.assertEqual(P.judge(0.4, {'a': noise, 'b': noise}, 0.5), 'not demonstrated')
        # A control that scores as well as the claim defeats it even above threshold.
        self.assertEqual(P.judge(0.8, {'a': noise, 'b': np.full(100, 0.85)}, 0.5), 'not demonstrated')
        # Only the 95th percentile matters, not a single outlier.
        outlier = np.concatenate([noise, [0.99]])
        self.assertEqual(P.judge(0.8, {'a': outlier}, 0.5), 'demonstrated')

    def test_run_returns_verdict_and_protocol(self):
        def experiment():
            return 0.72, {'random_unit': [0.05, -0.1, 0.12], 'shuffled_labels': [0.0, 0.02, -0.03]}
        result = P.run(complete(), experiment)
        self.assertEqual(result['verdict'], 'demonstrated')
        self.assertAlmostEqual(result['score'], 0.72)
        self.assertEqual(result['protocol']['threshold'], 0.5)
        self.assertEqual(sorted(result['controls']), ['random_unit', 'shuffled_labels'])


if __name__ == '__main__':
    unittest.main()
