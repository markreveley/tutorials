"""Lab: detect induction heads with a pre-registered test.

Build repeated and control sequences, compute the prefix-matching score from an
attention pattern, and judge the result. Spec and tests: test_induction.py (lesson 11).
"""

import torch


def repeated_sequence(seq_len, seed, bos_id, low=1000, high=20000):
    """[1, 1 + 2*seq_len]: BOS followed by a random block and its exact repeat."""
    raise NotImplementedError('implement after reading the tests')


def control_sequence(seq_len, seed, bos_id, low=1000, high=20000):
    """Same first block as repeated_sequence(seed), but a fresh random second block."""
    raise NotImplementedError('implement after reading the tests')


def prefix_matching_score(pattern, seq_len):
    """pattern: [heads, pos, pos] attention for one BOS + 2*seq_len sequence.
    For each second-copy position i, the induction target is i - seq_len + 1 (the
    token that followed this token's first occurrence). Return the mean attention
    there per head: a [heads] tensor."""
    raise NotImplementedError('implement after reading the tests')


def verdict(repeated_scores, control_scores, loss_first, loss_second, threshold=0.5, control_max=0.1):
    """repeated_scores / control_scores: [layers, heads]. Pass if at least one head
    reaches the threshold on the repeat, every such head is below control_max on the
    control, and the second-copy loss is lower than the first-copy loss."""
    raise NotImplementedError('implement after reading the tests')
