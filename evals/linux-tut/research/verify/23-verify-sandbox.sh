#!/usr/bin/env bash
# Inside-out check of a hardened sandbox. Run INSIDE the box: exits 0 only if every line is PASS.
# Usage (read-only root, so feed it on stdin): docker exec -i NAME bash -s < verify-sandbox.sh
set -u
fails=0
check() { # check DESCRIPTION COMMAND...
  local desc=$1; shift
  if "$@" >/dev/null 2>&1; then echo "PASS  $desc"; else echo "FAIL  $desc"; fails=$((fails + 1)); fi
}
status() { awk -v k="$1:" '$1 == k { print $2 }' /proc/self/status; }
cg() { cat "/sys/fs/cgroup/$1"; }

check "not root (uid $(id -u))"               test "$(id -u)" -ne 0
check "effective capabilities empty"          test "$(status CapEff)" = 0000000000000000
check "bounding set empty"                    test "$(status CapBnd)" = 0000000000000000
check "no_new_privs set"                      test "$(status NoNewPrivs)" = 1
check "root filesystem mounted read-only"     findmnt -n -O ro /
check "/etc, /usr, /home not writable"        bash -c '[ ! -w /etc ] && [ ! -w /usr ] && [ ! -w /home ]'
check "/tmp writable"                         touch /tmp/.probe
check "/app writable"                         touch /app/.probe
check "no route off the box"                  test "$(wc -l </proc/net/route)" -le 1
check "memory limit set ($(cg memory.max))"   test "$(cg memory.max)" != max
check "pids limit set ($(cg pids.max))"       test "$(cg pids.max)" != max
check "cpu limit set ($(cg cpu.max))"         bash -c '! grep -q "^max" /sys/fs/cgroup/cpu.max'
check "no Docker socket in the box"           test ! -e /var/run/docker.sock
check "no grader directory in the box"        test ! -e /opt/grader
rm -f /tmp/.probe /app/.probe
echo "$fails check(s) failed"
exit "$((fails > 0))"
