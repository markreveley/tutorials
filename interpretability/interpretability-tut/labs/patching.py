"""Lab: activation patching, the model-free parts.

A hook that overwrites one position with the clean activation, the recovered
fraction metric, and the verdict with a control position.
Spec and tests: test_patching.py (lesson 10).
"""


def recovered_fraction(clean_metric, corrupt_metric, patched_metric):
    """0 means the patch did nothing; 1 means it restored the clean metric."""
    raise NotImplementedError('implement after reading the tests')


def make_patch_hook(clean_activation, position):
    """Return a TransformerLens-style hook (act, hook) -> act that overwrites one
    position of the running activation with the clean one. Other positions and
    other batch rows are untouched."""
    raise NotImplementedError('implement after reading the tests')


def verdict(table, claim_position, control_position, claim_min=0.5, control_max=0.1):
    """table: {layer: [fraction per position]}. The claim passes if some layer
    recovers more than claim_min at the claim position; the control passes if no
    layer recovers more than control_max at the control position."""
    raise NotImplementedError('implement after reading the tests')
