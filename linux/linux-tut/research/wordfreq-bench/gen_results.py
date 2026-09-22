#!/usr/bin/env python3
"""Generate a deterministic results.jsonl for the text-fu page: 3 models x 8 tasks x 8 epochs.
Usage: python3 gen_results.py > results.jsonl   (stdlib only; fixed seed, same file every time)"""
import json
import random

random.seed(20260920)
MODELS = {"model-a": 0.78, "model-b": 0.61, "model-c": 0.44}
TASKS = ["wordfreq", "csvsum", "logrotate", "jsonfix", "pathwalk", "dedupe", "tzparse", "symlinks"]
HARD = {"tzparse": 0.35, "symlinks": 0.0}          # symlinks never passes: a broken task, not a hard one
FAILS = [                                           # (exit_code, stderr_tail, weight)
    (1, "AssertionError: Lists differ: [('The', 3)] != [('the', 7)]", 40),
    (1, "ModuleNotFoundError: No module named 'wordfreq'", 6),
    (124, "", 14),
    (137, "Killed", 10),
    (127, "bash: line 1: pytest: command not found", 12),
    (126, "bash: line 1: ./run.sh: Permission denied", 5),
    (1, "OSError: [Errno 28] No space left on device", 3),
    (1, "PermissionError: [Errno 13] Permission denied: '/opt/grader/expected.json'", 4),
    (2, "E: Could not get lock /var/lib/dpkg/lock-frontend", 3),
]
for model, skill in MODELS.items():
    for task in TASKS:
        for epoch in range(1, 9):
            p = skill * HARD.get(task, 1.0)
            if random.random() < p:
                row = {"exit_code": 0, "passed": True, "stderr_tail": ""}
                dur = random.uniform(18, 95)
            else:
                code, tail, _ = random.choices(FAILS, weights=[f[2] for f in FAILS])[0]
                row = {"exit_code": code, "passed": False, "stderr_tail": tail}
                dur = 300.0 if code == 124 else random.uniform(12, 240)
            print(json.dumps({"task": task, "model": model, "epoch": epoch, **row, "duration_s": round(dur, 1)}))
