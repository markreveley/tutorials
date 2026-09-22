"""Generate original synthetic fixtures; never call a model or fetch data."""
import json
from pathlib import Path

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
    return {'paired_tasks.jsonl': pairs, 'clustered_tasks.jsonl': clustered}


if __name__ == '__main__':
    ROOT.mkdir(exist_ok=True)
    for name, rows in fixtures().items():
        (ROOT/name).write_text(''.join(json.dumps(row, sort_keys=True)+'\n' for row in rows))
        print(f'{name}: {len(rows)} synthetic tasks')
