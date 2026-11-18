#!/usr/bin/env bash
# Grade one rollout. Usage: run-tests.sh APP_DIR RESULT_FILE
# Exit status = the hidden tests' exit status (0 pass, non-zero fail, 124 timeout).
set -euo pipefail

app_dir=${1:?usage: run-tests.sh APP_DIR RESULT_FILE}
result_file=${2:?usage: run-tests.sh APP_DIR RESULT_FILE}
grader_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

status=0
APP_DIR="$app_dir" PYTHONPATH="$app_dir" PYTHONDONTWRITEBYTECODE=1 \
  timeout -k 5 60 python3 -m unittest discover -s "$grader_dir" -p 'test_hidden.py' \
  >"$work/stdout" 2>"$work/stderr" || status=$?

passed=false
if [[ $status -eq 0 ]]; then passed=true; fi
tail_text=$(tail -n 3 "$work/stderr" | tr '\n' ' ' | tr -d '"\134')
printf '{"exit_code": %d, "passed": %s, "stderr_tail": "%s"}\n' \
  "$status" "$passed" "$tail_text" >>"$result_file"
exit "$status"
