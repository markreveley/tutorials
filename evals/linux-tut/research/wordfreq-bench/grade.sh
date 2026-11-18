#!/usr/bin/env bash
# Grade a finished rollout from OUTSIDE the sandbox. Usage: grade.sh CONTAINER RESULT_FILE
# Copies /app out of the (stopped or running) sandbox and runs the hidden tests against the copy
# in a fresh, network-less, read-only container that the agent never touched.
set -euo pipefail
container=${1:?usage: grade.sh CONTAINER RESULT_FILE}
result_file=${2:?usage: grade.sh CONTAINER RESULT_FILE}
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

docker cp "$container:/app" "$work/app"
touch "$work/result.jsonl"
status=0
# --workdir /tmp: the image's WORKDIR is /app, which holds the image's own pristine (buggy)
# wordfreq.py; "python3 -m" puts the cwd first on sys.path, so without this the grader would
# import that copy and grade the image instead of the submission.
docker run --rm --network none --read-only --tmpfs /tmp --workdir /tmp \
  --mount "type=bind,src=$work/app,dst=/submission,readonly" \
  --mount "type=bind,src=$here/grader,dst=/opt/grader,readonly" \
  --mount "type=bind,src=$work/result.jsonl,dst=/result.jsonl" \
  wordfreq-bench:hardened /opt/grader/run-tests.sh /submission /result.jsonl || status=$?
cat "$work/result.jsonl" >>"$result_file"
exit "$status"
