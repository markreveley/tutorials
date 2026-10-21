"""Lab: score an explanation by held-out activation prediction.

An explanation in rule form (a regex or a predicate) predicts, for each token,
whether a unit should fire. Score the prediction against the true activations on
held-out tokens, and compare with a random-unit control and a shuffled-label
control. Spec and tests: test_explanation_score.py (lessons 04 and 05).
"""

import re

import numpy as np


def pearson(x, y):
    raise NotImplementedError('implement after reading the tests')


def split_chunks(n_tokens, chunk):
    """Alternate contiguous chunks between screening (even) and held-out (odd).
    Returns two lists of (start, stop) index pairs; a trailing partial chunk is dropped."""
    raise NotImplementedError('implement after reading the tests')


def rule_predictions(str_tokens, rule):
    """Turn an explanation into predicted activations: 1 where the rule holds, else 0.
    `rule` is a regex string matched against the token text, or a callable
    (token, previous_token) -> bool."""
    raise NotImplementedError('implement after reading the tests')


def score_explanation(activations, predictions):
    """Held-out explanation score: Pearson r between predicted and true activations."""
    raise NotImplementedError('implement after reading the tests')


def random_unit_control(activation_matrix, predictions, unit, n=200, seed=0):
    """Score the same predictions against n other units (columns) chosen at random."""
    raise NotImplementedError('implement after reading the tests')


def shuffled_control(activations, predictions, n=500, seed=0):
    """Score the unit against n random permutations of the predictions."""
    raise NotImplementedError('implement after reading the tests')


def verdict(score, random_scores, shuffled_scores, threshold=0.5):
    raise NotImplementedError('implement after reading the tests')
