"""Reference solution for labs/protocol.py: a pre-registration that gates run()."""
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
        return asdict(self)


def _blank(value):
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().lower() in PLACEHOLDERS or value.strip().lower().startswith('todo')
    if isinstance(value, (list, tuple)):
        return len(value) == 0 or any(_blank(v) for v in value)
    return False


def validate(prereg):
    """Return the list of fields that are missing or still placeholders, plus a
    note if the author admits to having looked at the unit already."""
    problems = [name for name in REQUIRED if _blank(getattr(prereg, name))]
    if prereg.threshold is not None and not isinstance(prereg.threshold, (int, float)):
        problems.append('threshold')
    if not _blank(prereg.controls) and len(prereg.controls) < 2:
        problems.append('controls (name at least two)')
    if prereg.looked_already:
        problems.append('looked_already (the test must be written before the look)')
    return problems


def judge(score, control_scores, threshold):
    """'demonstrated' only if the score meets the threshold AND beats the 95th
    percentile of every control's score distribution."""
    import numpy as np
    if score < threshold:
        return 'not demonstrated'
    for name, scores in control_scores.items():
        if score <= float(np.percentile(np.asarray(scores, dtype=float), 95)):
            return 'not demonstrated'
    return 'demonstrated'


def run(prereg, experiment):
    """Run `experiment()` only when the protocol is complete. The experiment
    returns (score, control_scores); the result carries the verdict."""
    problems = validate(prereg)
    if problems:
        raise ProtocolError('protocol incomplete: ' + ', '.join(problems))
    score, controls = experiment()
    missing = [c for c in prereg.controls if c not in controls]
    if missing:
        raise ProtocolError('experiment did not report pre-registered controls: ' + ', '.join(missing))
    return dict(score=float(score), controls={k: list(map(float, v)) for k, v in controls.items()},
                threshold=float(prereg.threshold), verdict=judge(score, controls, prereg.threshold),
                protocol=prereg.as_dict())
