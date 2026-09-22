#!/usr/bin/env bash
# probe.sh [HOST_PORT] [PEER_IP:PORT] -- from inside a sandbox: what can this box reach?
set -u
host_port=${1:-8000}; peer=${2:-}
echo "== interfaces (fallback tunnel devices hidden) and routes"
ip -br addr | grep -v '@NONE'; ip route
gw=$(ip route | awk '/^default/ {print $3; exit}')  # no default route? assume .1 of the subnet
[ -n "$gw" ] || gw=$(ip route | awk '/proto kernel/ {split($1, a, "[./]"); print a[1] "." a[2] "." a[3] ".1"; exit}')
echo "== targets"
try() {  # try LABEL URL [curl options...]: any HTTP answer counts as reachable
  local label=$1 url=$2 code rc v; shift 2
  code=$(curl -sS -o /dev/null -m 5 --connect-timeout 3 -w '%{http_code}' "$@" "$url" 2>/dev/null)
  rc=$?
  case $rc in
    0)  v="REACHABLE (HTTP $code)" ;;
    7)  v="no: refused, rejected or no route (exit 7)" ;;
    28) v="no: dropped or timed out (exit 28)" ;;
    *)  v="no (curl exit $rc)" ;;
  esac
  printf '%-34s %s\n' "$label" "$v"
}
if getent ahosts example.com >/dev/null; then v="REACHABLE (external names resolve)"; else v="no"; fi
printf '%-34s %s\n' "DNS for external names" "$v"
try "internet https://example.com" https://example.com/
try "internet by IP 1.1.1.1" http://1.1.1.1/
try "internet over IPv6" https://example.com/ -6
if [ -n "$gw" ]; then try "host gateway $gw:$host_port" "http://$gw:$host_port/"
else printf '%-34s %s\n' "host gateway" "no: no interface but lo"; fi
try "metadata 169.254.169.254" http://169.254.169.254/
if [ -n "$peer" ]; then try "neighbour $peer" "http://$peer/"; fi
