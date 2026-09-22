# Finite workload fixtures

Use Python 3.10 or later. Every mode has a fixed upper bound. The fixtures create no network connections and execute only this same script for the process-tree case.

| Invocation after python3 labs/fixtures/workload.py | Behavior |
|---|---|
| exit --code 0 | One synthetic line on each stream; success |
| exit --code 7 | The same output; nonzero exit |
| sleep --seconds 5 | Finite delay; allowed range 1–30 seconds |
| emit --bytes-per-stream 262144 | Alternating chunks on both streams; maximum 1 MiB per stream |
| environment | Only two synthetic variables and the current directory |
| tree --seconds 15 | Parent plus one finite child; inherits pipes |
| cpu --seconds 2 | Finite CPU work for 1–10 wall-clock seconds |
| memory --mib 16 | Touches 1–64 MiB, holds for two seconds |

For the environment fixture use only synthetic values for SYLLABUS_ALLOWED and SYLLABUS_SECRET. Review the current-directory string before publishing captures.

The tree fixture intentionally demonstrates why killing a direct child and waiting for its stdout readers may not finish the descendant. Before a cleanup solution exists, the finite duration is the outer limit. Do not change this into an unbounded workload.

CPU work uses a wall-clock deadline. Under a quota it will usually do fewer iterations; it is not a calibrated benchmark. The memory exercise must attribute an observed failure using cgroup/service evidence rather than assuming every nonzero exit is an OOM kill.

These fixtures are learning inputs, not completed lesson artifacts. Read the relevant fixture and predict behavior before running it.
