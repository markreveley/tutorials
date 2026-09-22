# Synthetic fixtures

These files are original, constructed teaching data, not observations of any real
agent or user. `../make_data.py` regenerates them deterministically without network
access. The committed fixtures let learners start without a generation step.

- `paired_tasks.jsonl`: 200 hypothetical independent tasks, one binary attempt per
  version. Counts: 120 both pass, 24 A-only, 36 B-only, 20 neither. A=72%, B=78%.
- `clustered_tasks.jsonl`: 30 repository groups, four tasks each, three attempts per
  version and task. Tasks in a repository deliberately share outcome patterns to
  demonstrate strong dependence. Twenty repositories are routine and ten sensitive.
  A=66.67%, B=76.67%; routine difference +23.33 points, sensitive −16.67 points.

The statistical sampling assumptions are teaching hypotheticals. The generator
constructs patterns directly; it is not a simulator whose draws certify nominal
confidence-interval coverage. Coverage is studied separately by the `sample` lab.

Schema: one JSON object per line, unique `task_id`, nonempty `cluster_id` and `slice`,
and nonempty binary integer lists `a` and `b` with equal lengths within a task.
Attempt order is descriptive; the analysis pairs versions at the task level.
Cluster bootstrap resamples complete task-difference groups, retaining task weights.
