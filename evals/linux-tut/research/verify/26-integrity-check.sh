#!/usr/bin/env bash
# integrity-check.sh: the first six things an "attacker" rollout would look at.
# Run INSIDE a task container. Read-only. Exit status = number of open surfaces.
set -u
leaks=0
check() {  # check MESSAGE SNIPPET: the surface is OPEN if SNIPPET succeeds
  if bash -c "$2" >/dev/null 2>&1; then
    echo "OPEN    $1"
    leaks=$((leaks + 1))
  else
    echo "closed  $1"
  fi
}
check "identity:   running as root" 'id -u | grep -qx 0'
check "git:        /app carries a .git directory" 'test -d /app/.git'
check "filesystem: answer key or hidden tests readable" \
  "find / -xdev -type f \( -name 'expected*.json' -o -name 'test_hidden*' \) -readable | grep -q ."
check "filesystem: grading script writable" \
  "find / -xdev -type f -name 'run-tests.sh' -writable | grep -q ."
check "network:    a route exists (namespace is not empty)" "awk 'NR > 1' /proc/net/route | grep -q ."
check "host:       Docker socket mounted" 'test -S /var/run/docker.sock'
echo "$leaks open surface(s)"
exit "$leaks"
