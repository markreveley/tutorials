"""Reference solution for labs/explanation_score.py: held-out prediction scoring
of a rule-form explanation, with random-unit and shuffled-label controls."""
import re

import numpy as np


def pearson(x, y):
    x = np.asarray(x, dtype=np.float64); y = np.asarray(y, dtype=np.float64)
    if len(x) != len(y):
        raise ValueError('series must have the same length')
    if x.std() == 0 or y.std() == 0:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def split_chunks(n_tokens, chunk):
    """Alternate contiguous chunks between screening (even) and held-out (odd).
    Returns two lists of (start, stop) index pairs; a trailing partial chunk is dropped."""
    n = n_tokens // chunk
    spans = [(i * chunk, (i + 1) * chunk) for i in range(n)]
    return spans[0::2], spans[1::2]


def rule_predictions(str_tokens, rule):
    """Turn an explanation into predicted activations: 1 where the rule holds, else 0.
    `rule` is a regex string matched against the token text, or a callable
    (token, previous_token) -> bool."""
    out = np.zeros(len(str_tokens), dtype=np.float64)
    if isinstance(rule, str):
        pattern = re.compile(rule)
        for i, t in enumerate(str_tokens):
            out[i] = 1.0 if pattern.search(t) else 0.0
    else:
        for i, t in enumerate(str_tokens):
            out[i] = 1.0 if rule(t, str_tokens[i - 1] if i > 0 else '') else 0.0
    return out


def score_explanation(activations, predictions):
    """Held-out explanation score: Pearson r between predicted and true activations."""
    return pearson(activations, predictions)


def random_unit_control(activation_matrix, predictions, unit, n=200, seed=0):
    """Score the same predictions against n other units (columns) chosen at random."""
    rng = np.random.default_rng(seed)
    others = [j for j in range(activation_matrix.shape[1]) if j != unit]
    pick = rng.choice(others, size=min(n, len(others)), replace=False)
    return np.array([pearson(activation_matrix[:, j], predictions) for j in pick])


def shuffled_control(activations, predictions, n=500, seed=0):
    """Score the unit against n random permutations of the predictions."""
    rng = np.random.default_rng(seed)
    return np.array([pearson(activations, rng.permutation(predictions)) for _ in range(n)])


def verdict(score, random_scores, shuffled_scores, threshold=0.5):
    r95 = float(np.percentile(random_scores, 95)); s95 = float(np.percentile(shuffled_scores, 95))
    ok = score >= threshold and score > r95 and score > s95
    return dict(score=float(score), random_p95=r95, shuffled_p95=s95, threshold=threshold,
                demonstrated=bool(ok))
