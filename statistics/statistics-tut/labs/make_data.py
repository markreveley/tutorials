"""Generate original synthetic fixtures; never call a model or fetch data."""
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parent / 'data'


def fixtures():
    # 200 independent hypothetical tasks: both 120, A-only 24, B-only 36, neither 20.
    pairs = []
    for a, b, count in [(1, 1, 120), (1, 0, 24), (0, 1, 36), (0, 0, 20)]:
        for _ in range(count):
            i = len(pairs)
            pairs.append(dict(task_id=f'task-{i:03}', cluster_id=f'task-{i:03}',
                              slice='all', a=[a], b=[b]))
    # 30 repositories, four tasks each, three attempts each, balanced slice sizes.
    # Tasks within a repo deliberately share patterns, exposing pseudoreplication.
    clustered = []
    patterns = [(0, 0, 1), (0, 1, 1), (1, 1, 1)]
    for repo in range(30):
        part = 'routine' if repo < 20 else 'sensitive'
        a = list(patterns[repo % 3])
        b = a.copy()
        if part == 'routine' and repo % 3 != 2:
            b[b.index(0)] = 1
        elif part == 'sensitive' and repo % 2 == 0:
            b[b.index(1)] = 0
        for task in range(4):
            clustered.append(dict(task_id=f'repo-{repo:02}-task-{task}',
                                  cluster_id=f'repo-{repo:02}', slice=part, a=a, b=b))
    return {'paired_tasks.jsonl': pairs, 'clustered_tasks.jsonl': clustered,
            'candidates.jsonl': candidates()}


def candidates(count=60, n=40, planted=6, effect=.6, seed=24):
    """Many candidate units screened against one label vector.

    Every candidate has an activation on the same n synthetic inputs. The label
    is one continuous feature of each input, shared by all candidates. Most
    candidates are pure noise, independent of the label. The planted ones add
    `effect` times the label to their noise, so a real association exists for
    them. Values are rounded so the fixture is small and the file is exact.
    """
    rng = random.Random(seed)
    label = [round(rng.gauss(0, 1), 2) + 0.0 for _ in range(n)]
    rows = []
    for i in range(count):
        is_planted = i % (count//planted) == 3   # candidates 3, 13, 23, ...
        noise = [rng.gauss(0, 1) for _ in range(n)]
        activation = [round(v + (effect*l if is_planted else 0), 2) + 0.0 for v, l in zip(noise, label)]
        rows.append(dict(candidate_id=f'unit-{i:03}', activation=activation,
                         label=list(label), planted=is_planted))
    return rows


if __name__ == '__main__':
    ROOT.mkdir(exist_ok=True)
    for name, rows in fixtures().items():
        (ROOT/name).write_text(''.join(json.dumps(row, sort_keys=True)+'\n' for row in rows))
        print(f'{name}: {len(rows)} synthetic records')
