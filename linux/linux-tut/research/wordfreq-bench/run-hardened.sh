#!/usr/bin/env bash
# Start one hardened rollout sandbox. Usage: run-hardened.sh NAME
set -euo pipefail
name=${1:?usage: run-hardened.sh NAME}
docker run -d --name "$name" \
  --user agent \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --read-only --tmpfs /tmp:size=64m \
  --mount type=volume,dst=/app \
  --network none \
  --memory 512m --cpus 1 --pids-limit 128 \
  --init \
  wordfreq-bench:hardened
