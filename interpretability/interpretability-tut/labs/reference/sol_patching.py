"""Reference solution for labs/patching.py: the model-free parts of activation
patching (the hook, the recovery metric, and the verdict)."""


def recovered_fraction(clean_metric, corrupt_metric, patched_metric):
    """0 means the patch did nothing; 1 means it restored the clean metric."""
    gap = clean_metric - corrupt_metric
    if gap == 0:
        raise ValueError('clean and corrupted metrics are equal; there is nothing to recover')
    return (patched_metric - corrupt_metric) / gap


def make_patch_hook(clean_activation, position):
    """Return a TransformerLens-style hook (act, hook) -> act that overwrites one
    position of the running activation with the clean one. Other positions and
    other batch rows are untouched."""
    def hook(act, hook=None):
        act[:, position, :] = clean_activation[:, position, :]
        return act
    return hook


def verdict(table, claim_position, control_position, claim_min=0.5, control_max=0.1):
    """table: {layer: [fraction per position]}. The claim passes if some layer
    recovers more than claim_min at the claim position; the control passes if no
    layer recovers more than control_max at the control position."""
    best = max(row[claim_position] for row in table.values())
    worst = max(row[control_position] for row in table.values())
    return dict(best_claim=float(best), worst_control=float(worst),
                claim_passed=bool(best > claim_min), control_passed=bool(worst < control_max),
                passed=bool(best > claim_min and worst < control_max))
