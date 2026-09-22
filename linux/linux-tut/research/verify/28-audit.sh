#!/usr/bin/env bash
# audit.sh: the inside half of the ten-minute audit. READ-ONLY: it reads files and /proc and
# attempts three outbound TCP connections; it writes nothing. Works in minimal images (no ps, ss,
# ip or curl needed). The root may be read-only, so feed it on stdin:
#   docker exec -i NAME bash -s < audit.sh
set -u
sec() { printf '\n== %s\n' "$1"; }
st() { awk -v k="$1:" '$1 == k { print $2 }' /proc/self/status; }
cg() { cat "/sys/fs/cgroup/$1" 2>/dev/null || echo n/a; }
prune=(\( -path /proc -o -path /sys -o -path /dev -o -path /usr \) -prune -o)

sec "0 orient: who am I, on what?"
echo "id:      $(id)"
echo "os:      $(sed -n 's/^PRETTY_NAME=//p' /etc/os-release | tr -d '"'), kernel $(uname -r) $(uname -m)"
echo "box:     /.dockerenv $([ -e /.dockerenv ] && echo present || echo absent); /proc/1/cgroup $(cat /proc/1/cgroup)"
echo "pid 1:   $(tr '\0' ' ' </proc/1/cmdline)"

sec "1 running: processes (read from /proc) and listening TCP ports"
for d in /proc/[0-9]*; do
  cmd=$(tr '\0' ' ' <"$d/cmdline" 2>/dev/null | cut -c1-60) || continue
  [ -n "$cmd" ] && printf '%6s %-8s %s\n' "${d#/proc/}" "$(stat -c %U "$d" 2>/dev/null)" "$cmd"
done
while read -r _ local _ state _; do
  [ "$state" = 0A ] && echo "listening: TCP port $((16#${local##*:}))"
done < <(tail -q -n +2 /proc/net/tcp /proc/net/tcp6 2>/dev/null)

sec "2 mounted: filesystems, and where this user can write"
findmnt -rn -o TARGET,FSTYPE,OPTIONS | awk '$1 !~ /^\/(proc|sys|dev)\// { split($3, o, ","); print "  " o[1], $2, $1 }'
w=$(find / "${prune[@]}" -type d -writable -print 2>/dev/null)
echo "writable directories: $(grep -c . <<<"$w"), first few: $(head -4 <<<"$w" | tr '\n' ' ')"

sec "3 owns: privilege, and answers within reach"
echo "CapEff=$(st CapEff) CapBnd=$(st CapBnd) NoNewPrivs=$(st NoNewPrivs) Seccomp=$(st Seccomp)"
echo "setuid: $(find / -xdev -perm -4000 -type f 2>/dev/null | tr '\n' ' ')"
command -v sudo >/dev/null && echo "sudo: installed"
find / "${prune[@]}" -type f -readable \( -iname '*expected*' -o -iname '*solution*' \
  -o -iname '*answer*' -o -iname 'test_hidden*' -o -iname 'run-tests*' \) -print 2>/dev/null |
  sed 's/^/readable, answer-like: /'
find / "${prune[@]}" -name .git -type d -print 2>/dev/null | while read -r g; do
  echo "git repo ${g%/.git}: $(git -C "${g%/.git}" log --all --oneline 2>/dev/null | wc -l) commits on all refs"
done
[ -S /var/run/docker.sock ] && echo "DOCKER SOCKET MOUNTED: root on the host"

sec "4 reach: routes, DNS, three TCP connects (2 s each)"
for f in /sys/class/net/*/operstate; do  # skip DOWN devices (e.g. fallback tunnels)
  s=$(cat "$f"); i=${f%/operstate}; [ "$s" != down ] && echo "interface ${i##*/}: $s"
done
echo "IPv4 routes: $(($(wc -l </proc/net/route) - 1))"
echo "resolver: $(grep -m1 '^nameserver' /etc/resolv.conf 2>/dev/null || echo none)"
if timeout 3 getent hosts example.com >/dev/null; then echo "DNS: external names resolve"; else echo "DNS: no"; fi
for t in example.com:443 1.1.1.1:443 169.254.169.254:80; do
  if timeout 2 bash -c "exec 3<>/dev/tcp/${t%:*}/${t#*:}" 2>/dev/null; then r=OPEN; else r=closed; fi
  echo "tcp $t: $r"
done

sec "5 logs and limits"
echo "memory.max=$(cg memory.max) cpu.max=$(cg cpu.max | tr ' ' /) pids.max=$(cg pids.max)"
echo "memory.events: $(cg memory.events | tr '\n' ' ')"
echo "/var/log: $(find /var/log -mindepth 1 -maxdepth 1 -printf '%f ' 2>/dev/null)"
if [ -d /run/systemd/system ]; then echo "init: systemd, read journalctl"
else echo "init: not systemd; the main process's output is in 'docker logs' (outside)"; fi
