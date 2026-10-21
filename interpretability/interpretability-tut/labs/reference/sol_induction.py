"""Reference solution for labs/induction.py: sequences and the prefix-matching score."""
import torch


def repeated_sequence(seq_len, seed, bos_id, low=1000, high=20000):
    """[1, 1 + 2*seq_len]: BOS followed by a random block and its exact repeat."""
    g = torch.Generator().manual_seed(seed)
    r = torch.randint(low, high, (seq_len,), generator=g)
    return torch.cat([torch.tensor([bos_id]), r, r])[None]


def control_sequence(seq_len, seed, bos_id, low=1000, high=20000):
    """Same first block as repeated_sequence(seed), but a fresh random second block."""
    g = torch.Generator().manual_seed(seed)
    r = torch.randint(low, high, (seq_len,), generator=g)
    r2 = torch.randint(low, high, (seq_len,), generator=g)
    return torch.cat([torch.tensor([bos_id]), r, r2])[None]


def prefix_matching_score(pattern, seq_len):
    """pattern: [heads, pos, pos] attention for one BOS + 2*seq_len sequence.
    For each second-copy position i, the induction target is i - seq_len + 1 (the
    token that followed this token's first occurrence). Return the mean attention
    there per head: a [heads] tensor."""
    scores = [pattern[:, i, i - seq_len + 1] for i in range(seq_len + 1, 2 * seq_len + 1)]
    return torch.stack(scores).mean(0)


def verdict(repeated_scores, control_scores, loss_first, loss_second, threshold=0.5, control_max=0.1):
    """repeated_scores / control_scores: [layers, heads]. Pass if at least one head
    reaches the threshold on the repeat, every such head is below control_max on the
    control, and the second-copy loss is lower than the first-copy loss."""
    hits = [(int(l), int(h)) for l, h in (repeated_scores >= threshold).nonzero().tolist()]
    clean = all(control_scores[l, h] < control_max for l, h in hits)
    return dict(heads=hits, control_clean=bool(clean), icl=bool(loss_second < loss_first),
                passed=bool(hits and clean and loss_second < loss_first))
