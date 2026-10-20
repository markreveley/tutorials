"""Lab: the pre-registration protocol.

Implement a Preregistration record that must be complete before run() will
execute an experiment, and a judge() that compares a score with its controls.
Spec and tests: test_protocol.py. Read lesson 01 first; do not open
reference/sol_protocol.py until your tests pass.
"""

from dataclasses import dataclass, field, asdict

REQUIRED = ('claim', 'unit', 'heldout_data', 'scoring', 'prediction', 'threshold', 'controls', 'failure_means')
PLACEHOLDERS = ('', 'todo', 'tbd', '...', '?')


class ProtocolError(Exception):
    """Raised when an experiment is run before its protocol is complete."""


@dataclass
class Preregistration:
    claim: str = ''
    unit: str = ''
    heldout_data: str = ''
    scoring: str = ''
    prediction: str = ''
    threshold: float = None
    controls: list = field(default_factory=list)
    failure_means: str = ''
    looked_already: bool = False

    def as_dict(self):
        raise NotImplementedError('implement after reading the tests')


def _blank(value):
    raise NotImplementedError('implement after reading the tests')


def validate(prereg):
    """Return the list of fields that are missing or still placeholders, plus a
    note if the author admits to having looked at the unit already."""
    raise NotImplementedError('implement after reading the tests')


def judge(score, control_scores, threshold):
    """'demonstrated' only if the score meets the threshold AND beats the 95th
    percentile of every control's score distribution."""
    raise NotImplementedError('implement after reading the tests')


def run(prereg, experiment):
    """Run `experiment()` only when the protocol is complete. The experiment
    returns (score, control_scores); the result carries the verdict."""
    raise NotImplementedError('implement after reading the tests')
