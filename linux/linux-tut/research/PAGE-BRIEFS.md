# Page briefs — linux-tut

One brief per page. The brief fixes the page's job, its spine, the eval connections it must make,
and which source notes (`research/sources/<id>.json`) it leans on. Authors have latitude in how to
teach, none in provenance (see AUTHORING.md). "Sources:" lists note ids — read them before writing;
cite only what they verify. Titles/paths are fixed by `assets/nav-data.js`.

Recurring teaching devices (use them across pages so the course feels like one thing):

- **The running example: `wordfreq-bench`.** A toy agentic benchmark used all course long; the
  real, tested files live in `research/wordfreq-bench/` (read its README first). Task: "fix the
  bug in `/app/wordfreq.py` so the tests pass." Pieces: the task repo `/app`; user `agent`
  (uid 1001 — Ubuntu 24.04 images already have `ubuntu` at 1000); hidden tests + `expected.json` +
  `run-tests.sh` in `grader/`; an oracle solution; a deliberately **sloppy** image
  (`wordfreq-bench:sloppy`: git history with the fix on a branch, grader world-readable in the
  image, solution deleted in a later layer, agent is root) and a **hardened** one
  (`wordfreq-bench:hardened` + `run-hardened.sh` + grade-from-outside `grade.sh`); and
  `gen_results.py`, which prints a deterministic 192-line `results.jsonl`
  (`{"task","model","epoch","exit_code","passed","stderr_tail","duration_s"}`). Both images are
  already built on this machine. Use these files **verbatim** — quote them, run them, never fork
  the design; pages borrow whichever piece they need (page 5 greps the log; page 6 dissects
  `run-tests.sh`; page 8 hides the answer key; page 22 walks the Dockerfile; page 23 is
  `run-hardened.sh`; page 26 attacks the sloppy build; page 28 audits both). If you find a bug in
  the example, fix it in `research/wordfreq-bench/` and say so in your report.
- **The five audit questions** (from the ten-minute audit): *what is running? what is mounted
  (and is it read-only)? who owns what? what can it reach? where are the logs?* When a page
  answers one of them, say so explicitly ("this is audit question 2").
- **Symptom → layer tables.** Wherever possible end a section with a table mapping what you'd see
  in a transcript/log to what it means (e.g. exit 137 → SIGKILL → OOM or timeout kill).

---

## Start

### 00 · Orientation: why Linux, for evals  (`pages/00-orientation.html`)
Job: convince the reader that Linux is not background knowledge for agentic evals but part of the
measuring instrument, and give the map of the course.
Spine: (1) An agentic eval, physically: harness on a host → N sandboxes (containers/VMs) → a model
issuing shell commands → a grader inspecting the final state. ASCII diagram. Almost all of it is
Linux. (2) Evidence that the field runs on this: SWE-bench's move to Docker for reproducibility;
Terminal-Bench's task anatomy; Inspect's sandbox abstraction; OSWorld's VMs; HumanEval's 2021
gVisor sandbox. (3) Three ways Linux ignorance corrupts a score, each with a verified incident:
*infrastructure failure scored as model failure* (OOM/timeout/env drift; Anthropic post, SWE-bench
Docker rationale), *environment leaks the answer* (SWE-bench git-history issue; METR), *environment
lets the agent out* (o1 system card Docker API). (4) The competence target: the ten-minute audit
and its five questions; how the modules map onto them (table: question → module → pages).
(5) What this course is not (sysadmin cert prep). (6) How to work: type everything; labs.
Pointer to Linux Journey as supplementary drill (only if the note confirms it's live).
Sources: swe-bench-docker, swe-bench-git-leak, terminal-bench, inspect-sandbox, osworld-env,
humaneval-sandbox, o1-docker-incident, metr-reward-hacking, anthropic-agent-evals, linux-journey.
Lab: light — run `docker run --rm -it ubuntu:24.04 bash`, poke around with 5 commands, record
what you don't understand in the output; you'll return to this list at page 28.

### 01 · Lab setup: a Linux box you can break  (`pages/01-lab-setup.html`)
Job: get a Mac user two labs. **Container lab**: Docker Desktop (or OrbStack/Colima — mention as
alternatives without claims about them), `docker run -it --name lt-lab ubuntu:24.04 bash`,
installing the course's tools (`procps iproute2 curl dnsutils jq less man-db file tree psmisc
libcap2-bin util-linux findutils`; note `unminimize`/man pages absent in minimal images — verify
by running), creating the `learner` non-root user, start/stop/rm, "it's disposable: break it".
**VM lab**: needed for systemd, firewalls, root-level namespace work. Options: a small cloud VPS
over SSH, or a local VM (Lima/Multipass/UTM — name them, link them, no unverified claims). Basic
`ssh user@host`, keys in one paragraph. Explain honestly what Docker Desktop on a Mac is: a Linux
VM running containers (so the kernel you see in the container is that VM's kernel — `uname -a`).
Why not just use the Mac's terminal: BSD userland vs GNU, no /proc, no namespaces → Appendix E.
A "lab hygiene" card: name things, clean up, never paste secrets.
In eval work: this is the same loop you'll use to debug a task image: `docker run -it <image> bash`.
Sources: docker-run, docker-storage (only if needed), apt-dpkg. Mostly executed mechanics.
Lab: build the lab; verify with a checklist of commands and expected output shapes.

## Module 1 · The shell

### 02 · The shell and the command line  (`pages/02-shell-and-commands.html`)
Job: a mental model of what happens between pressing Enter and output appearing.
Spine: terminal vs shell vs program; anatomy of a command line (command, options, arguments;
short/long flags; `--`); how the shell finds a program (`PATH`, `type`, `which`, `command -v`;
builtins and *why* `cd` must be a builtin); the exit status (`$?`, 0 = success, `&&`/`||`);
interactive vs non-interactive shells and startup files — the punchline: a harness running
`bash -c "…"` reads none of your `.bashrc`, so PATH/aliases/venv activation differ from an
interactive session; `bash --login -c` and explicit PATH as remedies; history/tab-completion/
Ctrl-C/Ctrl-D in one card. Alpine: `sh` is BusyBox ash — `bash: not found`.
In eval work: (a) "command not found" (127) in a transcript is usually a PATH/shell-mode problem,
not a missing install; (b) every agent tool call is a non-interactive shell invocation — what that
implies (no aliases, no prompts, state like `cd` may not persist between calls depending on the
harness: Inspect `bash` tool runs each call fresh vs `bash_session` — cite note).
Sources: bash-manual, posix-shell, inspect-sandbox, alpine.

### 03 · Files and the filesystem tree  (`pages/03-files-and-the-tree.html`)
Job: the single-rooted tree, where things live and why, and what a "file" really is.
Spine: one tree, no drive letters; absolute vs relative paths, `.`/`..`/`~`; the FHS tour as a
table (dir → what lives there → why an evals engineer looks there): `/etc /var/log /tmp /home
/root /usr /opt /proc /sys /dev /run`; /usr-merge symlinks as seen in `ls -l /`; core commands
`ls -la`, `cp -r`, `mv`, `rm -r`, `mkdir -p`, `touch`, `cat`, `less`, `file`, `stat`, `tree`, `find`
(name/type/mtime/-newer/-user/-perm) — `find` gets real depth because "what did the agent change?"
is a find question (`find / -xdev -newer /tmp/marker -type f`); inodes, hard links, symlinks
(diagram: directory entry → inode → data); deleted-but-open files; dotfiles; "everything is a
file" preview (`/dev/null`, `/proc`).
In eval work: state-based grading is "inspect the tree after the agent exits"; a marker file +
`find -newer` gives you the agent's footprint; symlinks as a grading hazard (agent replaces
expected output file with symlink to something else; graders should resolve and check type).
Sources: fhs, hier-7, inode-7, coreutils.

### 04 · Streams, pipes, and redirection  (`pages/04-streams-pipes-redirection.html`)
Job: file descriptors as the model behind `>`, `2>&1`, `|`.
Spine: every process starts with fds 0/1/2 (diagram, show `ls -l /proc/self/fd`); redirection is
the shell rewiring fds before exec; `>` `>>` `<` `2>` `2>&1` and why order matters (worked, run
both orders); `&>`; `/dev/null`; pipes connect stdout→stdin, stderr bypasses (demonstrate);
pipeline exit status and `pipefail` (`false | true; echo $?`); `tee`; here-docs/here-strings (the
way agents and Dockerfiles write files); `$(…)` command substitution; buffering caveat (output
order interleaving between stdout/stderr when captured separately; `python -u`/`stdbuf` mention
only if verified by running); SIGPIPE in `yes | head` as a teaser to page 10.
In eval work: harness exec APIs return stdout and stderr separately (Inspect ExecResult) — a
grader or log that records only stdout sees an empty string when the tool failed; agents that
`cmd 2>/dev/null` hide the evidence from themselves; `cmd | tee log` masks cmd's failure without
pipefail → "tests passed" when pytest crashed. Output-size limits (Inspect's exec output limit —
cite) and why `| head`/`| tail` matter to an agent.
Sources: bash-manual, posix-shell, coreutils, inspect-sandbox, signal-7 (SIGPIPE).

### 05 · Text-fu: reading logs at scale  (`pages/05-text-fu.html`)
Job: the small toolkit that lets you interrogate 10,000 rollouts from the terminal.
Spine: the pipeline philosophy (filter → extract → aggregate); `grep` (-i -v -c -n -r -l -E -o,
-A/-B/-C); `cut`, `tr`, `sort` (-n -r -k -t -u), `uniq -c` and why it needs sort; the
`sort | uniq -c | sort -rn` idiom; `wc -l`; `head`/`tail`/`tail -f`; `sed` for substitution and
line ranges only (`s///`, `-n '5,10p'`, `-i` and the macOS difference → App. E); `awk` for
columns and sums only (`{print $2}`, `-F`, `$3>10`, `{s+=$2} END{print s}`); `jq` for JSONL
(`.field`, `select()`, `-r`, `-c`, `-s` + `group_by`/`length`/`add`); `xargs` basics and the
`-0`/`find -print0` safety pair; `LC_ALL=C sort` for reproducible ordering. Regex only as far as
needed; send to Appendix D.
Worked example (must be real): generate a ~200-line `results.jsonl` for wordfreq-bench with a
Python one-liner (fixed seed), then answer in order: pass rate per model; most common exit codes
among failures; which tasks never pass; median-ish duration; grep the stderr tails for `Killed`,
`Permission denied`, `command not found` and count by category. Show every command and output.
In eval work: this *is* first-pass error analysis on agent transcripts (link sibling course
page 04 error analysis); when to stop and open pandas (rule of thumb: more than one join or any
statistics → Python).
Sources: coreutils, jq-manual; mostly executed mechanics.

### 06 · Shell scripts under thirty lines  (`pages/06-shell-scripting.html`)
Job: write and, more importantly, *read* the small bash scripts that glue eval environments
together (entrypoints, `run-tests.sh`, setup scripts) — and know when to stop.
Spine: shebang + executable bit (126 if missing); variables and **quoting** (the word-splitting
demo with a filename containing a space; `"$var"`, `"$@"`); `$(…)`; exit codes as the control flow
(`if cmd; then`, `&&`, `||`, `[[ ]]` vs `[ ]`, `-f -d -z -n`); `for`/`while read -r`; functions
briefly; **strict mode** `set -euo pipefail` — what each does, and `set -e`'s documented exceptions
(so the reader trusts it appropriately); `trap … EXIT` for cleanup; `mktemp`; ShellCheck as the
non-negotiable linter (show a buggy script, shellcheck's actual output, the fix); the thirty-line
rule and the Python `subprocess.run([...], capture_output=True, text=True, timeout=…, check=False)`
equivalent, with list-args vs `shell=True` injection note. Worked example: dissect `research/wordfreq-bench/grader/run-tests.sh` line by line (timeout, both streams to
files, JSON result line, exit with the tests' status, trap cleanup) — it is shellcheck-clean; then show a broken
variant without status propagation that 'passes' everything.
In eval work: a test script without `set -e`/explicit exit propagation returns the status of its
LAST command (e.g. `echo done`) → every rollout "passes"; graders must key off something the
script cannot accidentally produce; read every task's `run-tests.sh` for this bug (Terminal-Bench
task anatomy — cite).
Sources: bash-manual, shellcheck, coreutils (timeout, mktemp), terminal-bench.

## Module 2 · Identity & permissions

### 07 · Users, groups, and root  (`pages/07-users-groups-root.html`)
Job: who a process "is", and why the agent should not be root.
Spine: the kernel knows numbers (uid/gid), names are a lookup; `id`, `whoami`, `getent passwd`;
`/etc/passwd` fields, `/etc/shadow`, `/etc/group`; root = uid 0 and what it bypasses; system/
service accounts and `nologin`; creating users (`useradd -m -s /bin/bash agent`, `usermod -aG`,
`passwd -l`), `su - user`, `sudo` (what it is, `sudo -l`, NOPASSWD, why minimal images don't have
it — verified by running); processes inherit credentials; numeric-uid gotcha across container/host
boundaries: a bind-mounted file owned by uid 1000 on the host shows up as whoever is 1000 in the
container (or a bare number) — demo with `ls -ln`. Docker's default user is root (cite) and
`USER`/`--user`.
In eval work: (a) agent-as-root means every file-permission protection in the box is void —
answer keys, test files, the grader's scripts; (b) but many task images need root to `apt install`
— the design tension and the standard resolution (install at build time, run as non-root; or
grade outside the box); (c) Inspect's `user` parameter on exec/bash tool (cite) lets the harness
run agent commands as one user and scoring commands as another.
Sources: credentials-7, sudo, docker-security, dockerfile, inspect-sandbox, capabilities-7.

### 08 · Permissions and ownership  (`pages/08-permissions.html`)
Job: read `-rwxr-x---` fluently, predict access decisions, and use that to protect an answer key.
Spine: the `ls -l` anatomy; three classes × three bits; the decision procedure — exactly one class
is consulted (worked surprise: owner with `---` denied though others have `r--`); octal (link
App. C); `chmod` symbolic and numeric; `chown user:group` (root only); **directories**: r = list,
w = create/delete, x = traverse — deleting a file is a directory write (worked: read-only file
deleted by its non-owner in a writable dir); path traversal needs x on every ancestor (so
`chmod 700 /opt/grader` protects everything beneath); sticky bit and `/tmp` (1777); setuid
(`/usr/bin/passwd`), why it's a privilege-escalation surface, `find / -perm -4000` as an audit
command; umask (022 → 644/755; link App. C); root bypass (CAP_DAC_OVERRIDE, cite). Brief: ACLs
exist (`+` in ls) — know the sign, skip the detail.
Worked case (real, run as non-root `agent`): wordfreq-bench layout — `/app` owned by agent;
`/opt/grader` root:root 700 holding hidden tests + expected output; show agent's `cat` and `ls`
fail with exact errors; then show three ways the protection silently fails: tests copied in with
world-readable perms *and* parent dir 755; agent is root; agent can `sudo`. End with the stronger
design: don't put the key in the box at all (forward-link page 26).
In eval work: ImpossibleBench's finding on read-only/hidden tests (cite exact numbers from note);
permission errors in transcripts (`Permission denied` vs `Operation not permitted` — EACCES vs
EPERM: the first is mode bits, the second is privilege/capability — verify by running both).
Sources: chmod-umask, inode-7, credentials-7, capabilities-7, impossiblebench.

## Module 3 · Processes

### 09 · Processes: what is running  (`pages/09-processes.html`)
Job: audit question 1. The process tree as the model.
Spine: program vs process; PID, PPID, the tree (`ps -ef --forest`, `pstree -p`); fork → exec →
wait → exit (diagram), what is inherited (fds, env, cwd, credentials, limits); `ps aux` columns
and STAT codes (cite); `top`/`htop` reading the header; `pgrep`/`pkill`; `/proc/PID/` tour
(`cmdline`, `cwd`, `exe`, `fd/`, `status`, `environ`) — "ps is just a /proc reader"; foreground/
background/`&`/`jobs`/`nohup`/`disown`; daemons; zombies and orphans, and who reaps them (PID 1);
what `ps` shows inside a container (tiny tree, PID 1 is your command) vs on the host — teaser for
page 20.
In eval work: agents start servers in the background (`python -m http.server &`, `npm start &`)
and harnesses differ on what happens to them when the tool call returns; leftover processes
between rollouts are shared state (cite Anthropic clean-environment wording); a grader that needs
the agent's server running must check the process, not the agent's claim; `ps -ef --forest` is the
first command of the ten-minute audit.
Sources: fork-exec-wait, proc-5, procps, pid1, anthropic-agent-evals.

### 10 · Signals, exit codes, and timeouts  (`pages/10-signals-exit-codes.html`)
Job: decode how things end. The most transcript-relevant page in the course.
Spine: signals as asynchronous notifications; the working set (INT, TERM, KILL, HUP, QUIT, STOP/
CONT, SEGV, PIPE, CHLD) with numbers and default actions (cite); `kill`, `kill -9`, `pkill`,
Ctrl-C/Ctrl-Z mapping; catchable vs not (KILL/STOP); graceful shutdown protocol TERM → wait →
KILL, as implemented by `timeout -k`, `docker stop` (10 s, cite), systemd (90 s, cite); exit
status encoding: 0–255, 126, 127, 128+N → 130, 137, 139, 143; `timeout` and its 124/137 (cite,
and run each); `trap` in bash; the **PID 1 problem** in containers: your app as PID 1 ignores
TERM unless it handles it, doesn't reap zombies → `docker stop` hangs 10 s then KILLs (137);
`--init`/tini and exec-form ENTRYPOINT as the fix (cite; demo both, real timings).
Centerpiece table: *exit code seen in log → what happened → where to look next* for 0, 1, 2,
124, 125, 126, 127, 130, 137, 139, 143 (then link Appendix B for the long version).
In eval work: 137 is the great ambiguity — OOM kill, harness timeout kill, or `docker stop`;
each means something different for scoring (infrastructure failure vs agent too slow vs normal
teardown) and you disambiguate with `memory.events`/`State.OOMKilled` (page 12), harness logs, and
timing; rollouts that died by timeout should be reported separately from wrong answers; Inspect's
tool timeout behaviour as seen by the model (cite).
Sources: signal-7, coreutils, bash-manual, pid1, docker-run, systemd, inspect-sandbox.

### 11 · Environment variables and secrets  (`pages/11-environment-and-secrets.html`)
Job: how configuration and secrets flow into processes, and every place they leak.
Spine: env is a per-process array of strings copied at fork/exec (cite) — children inherit,
parents never see changes (demo: `export` in a subshell/script doesn't affect caller; why
`source` exists); `env`, `printenv`, `export`, `VAR=x cmd` one-shot form, `env -i`; conventional
variables (PATH, HOME, USER, LANG/LC_ALL, TZ, PWD, SHELL, TERM, http_proxy family → page 18);
locale/TZ as reproducibility hazards (sort order, date output); where env comes from in a
container (Dockerfile ENV, `-e`, `--env-file`, compose `environment`). **Leak surfaces**, each
demonstrated for real: `/proc/PID/environ` (same-user and root can read; it's the *initial* env —
cite), `ps e`/cmdline args world-readable (cite), `docker inspect` Config.Env (cite), image history
for ENV/ARG (cite), shell history, logs/tracebacks that dump env, core dumps. Mitigations ladder:
don't put the secret in the sandbox at all (proxy the API call from outside — how Inspect's model
calls stay on the host; agent-bridge note, cite) → scoped/short-lived key → file with 0400 owned by
a different user → never as CLI arg.
In eval work: the agent runs *inside* the environment with a shell: anything in its env, or
readable by its uid, is part of its observation space — API keys, grader config, the expected
answer passed as `EXPECTED=…` to a checker process running as the same user; spending/abuse risk
from leaked provider keys; an audit is `env`, `cat /proc/1/environ | tr '\0' '\n'`, and
`docker inspect` from outside.
Sources: fork-exec-wait, proc-5, docker-logs-inspect, dockerfile, inspect-sandbox, sudo (env_reset).

### 12 · Resources, limits, and the OOM killer  (`pages/12-resources-and-limits.html`)
Job: know when the box, not the model, failed.
Spine: the four resources (CPU, memory, disk, PIDs/fds) and the tool for each: `nproc`, `uptime`/
load average (what it counts — cite), `top`; `free -h` and the *available* column (cite);
`df -h` vs `du -sh` (+ the deleted-open-file discrepancy from page 3), `df -i` inodes; per-process
rlimits `ulimit -a` (soft/hard, inherited — cite) vs per-group cgroup limits (preview of page 21):
read `/sys/fs/cgroup/memory.max`, `memory.current`, `memory.events`, `cpu.max`, `pids.max` from
inside a limited container (real output from `docker run --memory 256m --cpus 1.5 --pids-limit 100`);
**what each exhaustion looks like** (run each for real): memory → `Killed`, exit 137,
`oom_kill 1` in memory.events, `OOMKilled: true`; CPU cap → nothing dies, everything is slow
(throttling counters in cpu.stat) → timeouts; disk full → `No space left on device` (ENOSPC);
pids → `fork: retry: Resource temporarily unavailable`; fds → `Too many open files`.
Caveat: `free`/`nproc`/`top` inside a container may report the HOST's totals, not the cgroup
limit (verify by running with --memory and show the discrepancy) — programs that size themselves
from these (parallel test runners, JVMs historically) overshoot and get killed.
In eval work: an under-provisioned sandbox converts capable-model rollouts into failures and the
score drops for reasons unrelated to the model; concurrency (N sandboxes on one host — Inspect
max_sandboxes note, SWE-bench resource guidance, cite) changes per-sandbox resources and therefore
scores → resource settings are part of the eval's reported configuration (link sibling course
page 19 reproducibility); report OOM/timeout counts next to pass rates.
Sources: oom, rlimits, proc-5, procps, docker-run, inspect-sandbox, swe-bench-docker.

### 13 · Services, init, and logs  (`pages/13-services-and-logs.html`)
Job: audit question 5 (where are the logs) plus how long-running software is supervised on a real
machine vs in a container.
Spine: boot in one paragraph → PID 1 → systemd; units and `systemctl status|start|stop|restart|
enable|disable`, `list-units --type=service --state=running`, `--failed`; reading a unit file
(ExecStart, User, Restart, Environment, WorkingDirectory — a 12-line annotated example of a
service that runs an eval worker); journald and `journalctl -u/-f/-b/-p/--since/-k`, persistence
(cite); classic text logs in `/var/log` (what's typically there on Ubuntu: syslog or journal-only,
auth.log, dpkg.log, apt/history.log — verify by running what exists in a container and cite the
rest), `dmesg`/kernel ring buffer — where OOM kills are recorded at host level; log rotation in one
paragraph. **Containers are different**: usually no systemd, no journald, PID 1 is the app, logs =
stdout/stderr captured by the runtime → `docker logs`, json-file driver, no rotation by default
(cite). Decision table: "I'm on a VM" vs "I'm in a container" → where to look for what.
`/var/log/apt/history.log` and `dpkg.log` as a forensic record of what an agent installed.
VM-lab only for the systemd parts: output shown must be quoted from docs or described, unless
the author can genuinely run systemd (Docker Desktop cannot, reliably) — do not fabricate output.
In eval work: harness workers and sandbox hosts are services — when 5% of rollouts fail at 03:00
you need `journalctl --since`; the host's kernel log is the only place some sandbox deaths are
recorded; transcripts + container logs + host logs are three different evidence streams (sibling
course page 26 observability).
Sources: systemd, docker-logs-inspect, oom, apt-dpkg.

## Module 4 · Storage & software

### 14 · Mounts and filesystems  (`pages/14-mounts-and-filesystems.html`)
Job: audit question 2. The mount table as a model; read-only as an integrity tool.
Spine: one tree, many filesystems grafted at mount points (diagram); `findmnt` (tree; `-T path`;
`-o TARGET,SOURCE,FSTYPE,OPTIONS`), `mount` with no args, `/proc/self/mountinfo` as ground truth
(cite); `lsblk`, `df -hT`; mount options that matter: `ro`, `nosuid`, `nodev`, `noexec`; pseudo-
filesystems proc/sysfs/devtmpfs/tmpfs/cgroup2; tmpfs (RAM-backed, counts against memory — cite;
demo filling a tmpfs in a memory-limited container → OOM or ENOSPC, show which really happens);
bind mounts (a directory appearing in two places; how Docker volumes/`-v` are implemented); overlayfs
(lower/upper/merged, copy-up, whiteouts — cite; show the `overlay` line for `/` inside a container
and explain it); what a container's mount table looks like, annotated line by line (real output);
"is it read-only?" — `findmnt -O ro`, `touch` test, `EROFS` "Read-only file system" error vs
"Permission denied" (different layer: mount vs mode bits vs capability).
In eval work: read-only mounts are the strongest in-box protection because root inside the
container can't `chmod` its way around them (without CAP_SYS_ADMIN to remount — cite); typical
layout: tests/reference data mounted `ro`, `/app` writable, `/tmp` tmpfs; but readable ≠ safe —
read-only protects against *tampering*, not *reading* (answer keys need absence, not `ro`); a
writable bind mount from the host is a hole in the sandbox wall (cite Docker warning); shared
volumes between concurrent rollouts = cross-contamination.
Sources: mounts, overlayfs, docker-storage, oom (tmpfs charging), capabilities-7.

### 15 · Packages and reproducible environments  (`pages/15-packages-reproducibility.html`)
Job: how software gets into the box, and why "same Dockerfile" ≠ "same environment".
Spine: what a package manager does (repos, index, dependency resolution, install scripts);
apt workflow: `apt-get update` (why a fresh image fails without it — real error), `install -y
--no-install-recommends`, `DEBIAN_FRONTEND=noninteractive` and the tzdata prompt hang, `apt-cache
policy`, `dpkg -l`, `dpkg -S`, `dpkg -L`, the lock error (cite/real); `apt` vs `apt-get` in
scripts (cite); Alpine `apk add --no-cache`, musl vs glibc wheels (cite); Python layer: PEP 668
error (real text), venvs (activation = PATH edit), `pip install -r`, `pip freeze`, hashes (cite).
**Drift**: the three moving parts — base image tag (mutable; pin by digest, cite), distro repo
(only current versions; old pins vanish; snapshot.debian.org / snapshot.ubuntu.com, cite), PyPI
(unpinned transitive deps). Worked demo: `docker inspect --format '{{index .RepoDigests 0}}'
ubuntu:24.04`, `FROM ubuntu@sha256:…`; `dpkg -l | wc -l` + `pip freeze` as an environment
fingerprint you can diff between two builds (show a real diff, e.g. debian:bookworm-slim vs
ubuntu:24.04 or before/after an install).
In eval work: SWE-bench's Docker move was precisely about environment drift changing test
outcomes (cite exact wording); a benchmark whose images rebuild differently next month is a
different benchmark — publish image digests with results; agents with network access `pip
install`/`apt install` their way to different environments per rollout (nondeterminism + a
supply-chain surface), and without network hit install errors you must recognize in transcripts;
the build-time vs run-time network distinction (build with network, run without).
Sources: apt-dpkg, pip-repro, alpine, dockerfile, swe-bench-docker.

## Module 5 · Networking for sandboxes

**Division of labour (see AUTHORING.md addendum §6):** the sibling course *Networking for LLM Evals* teaches the
concepts. These four pages summarise a concept in a sentence or two, link to the matching lesson there, and spend
their words on the Linux side: reading the box's network state, namespaces, Docker networks, enforcement, probing.

### 16 · Addresses, interfaces, and routes  (`pages/16-addresses-and-routes.html`)
Job: first half of audit question 4: what network am I on?
Spine: an IP address names an interface, not a machine; IPv4 dotted quad, CIDR prefix (link App.
C), network vs host part; private ranges (cite RFC 1918), loopback 127/8, link-local 169.254/16
(cite); `ip addr` annotated (lo, eth0, state, inet, scope), `ip link`; the routing table: `ip
route`, default gateway, `ip route get 1.1.1.1` as "which way would a packet go"; NAT in one
diagram: container 172.17.0.2 → docker0 bridge → host → internet, and why the outside sees the
host's address (cite Docker masquerade); veth pairs as the cable between container and bridge
(cite); IPv6 exists — recognise `inet6`, `::1`, don't go deeper, but note egress rules must cover
it or be disabled. What this looks like under `--network none` (only `lo`) vs default bridge vs
user-defined network (real output all three). ifconfig/netstat: legacy; recognise them in
transcripts (agents often try them, get 127).
In eval work: knowing the sandbox's address and gateway tells you what is *adjacent*: other
rollouts' containers on the same bridge, the host's services on the gateway address, the cloud
metadata service at 169.254.169.254 (cite — credentials exposure); the o1 incident began with
the model looking at its network neighbourhood (cite precisely).
Sources: rfc1918, iproute2, netfilter (bridge/NAT/none), cloud-metadata, o1-docker-incident.

### 17 · Ports, sockets, TCP and UDP  (`pages/17-ports-and-sockets.html`)
Job: second half of "what is running" and "what can it reach": who is listening, who is connected.
Spine: a port names a process's endpoint on an address; socket = (proto, local addr:port, remote
addr:port); TCP vs UDP in a small table (cite); port ranges + privileged ports (cite);
`ss -tulpn` annotated (real output with a python http.server running); **bind address matters**:
`127.0.0.1:8000` (this namespace only) vs `0.0.0.0:8000` (every interface → reachable from the
bridge/neighbours) — demo between two containers on one network; `nc -zv host port`, `curl`,
bash `/dev/tcp` trick when no tools are installed (cite bash manual; verify works in ubuntu,
not in Alpine/ash); **symptom table**: `Connection refused` (reached host, nothing listening —
RST) vs hang/`timed out` (dropped — firewall or no route) vs `No route to host`/`Network is
unreachable` (routing) vs `Name or service not known` (DNS, next page) — produce each for real;
each container has its own localhost (network namespace) — why `localhost:5432` from the app
container doesn't reach the db container, and why compose service names do (cite); published
ports `-p 8080:80` and `-p 127.0.0.1:8080:80` (host-side exposure; Docker bypassing host firewall
INPUT rules — cite).
In eval work: multi-container tasks (app + db) fail in transcripts with exactly these symptoms;
the grader probing the agent's service must handle "not listening yet" (retry with deadline) vs
"bound to 127.0.0.1 inside the container" when the grader connects from outside; services on the
HOST bound to 0.0.0.0 (databases, Docker API on 2375, harness dashboards) are reachable from
sandboxes via the gateway — `ss -tulpn` on the host is part of the audit (o1 incident: exposed
Docker API; cite).
Sources: tcp-udp, iproute2, bash-manual (/dev/tcp), netfilter, docker-compose, o1-docker-incident.

### 18 · DNS, HTTP, and TLS  (`pages/18-dns-http-tls.html`)
Job: the three layers between "a hostname" and "a response", and how to tell which one broke.
Spine: name resolution path: app → libc resolver → nsswitch (`files dns`) → `/etc/hosts` →
`/etc/resolv.conf` nameserver (cite); `getent hosts` (what apps see) vs `dig`/`dig +short` (DNS
only) and reading dig's status/ANSWER/SERVER lines (cite); Docker's resolv.conf on default bridge
vs 127.0.0.11 embedded DNS on user-defined networks (cite; real output); Ubuntu's 127.0.0.53 stub
on VMs. HTTP in one screen via `curl -v` annotated line by line (real output: DNS → connect → TLS
→ request `>` → response `<`), status classes (cite), the flags you'll use (`-sS -f -L -o -I
--max-time`), **curl exit codes as a layer decoder** table 6/7/28/35/60/22 (cite; produce each for
real). TLS: what the certificate proves (cite RFC 8446 goals), the trust store
(`ca-certificates`; the fresh-image failure — real error), `-k` is not a fix, clock skew breaks
TLS. Proxies: `http_proxy`/`HTTPS_PROXY`/`NO_PROXY` semantics and case rules (cite), what a
CONNECT tunnel is, 407/403 from a proxy, interception requires installing the proxy CA (cite).
In eval work: the standard controlled-egress design is "no direct route + an allowlisting proxy"
— you must recognise its signatures in transcripts (403 from proxy on pip install; works for
pypi.org, fails for github.com); DNS is an egress channel even when HTTP is blocked (cite if note
supports) — check whether the sandbox can resolve arbitrary names; agents given a web tool vs
agents with raw network are different threat models; HTTPS failing with certificate errors in a
minimal image is an environment bug, not a model failure.
Sources: dns, curl, tls-http, netfilter.

### 19 · Firewalls and egress control  (`pages/19-firewalls-and-egress.html`)
Job: finish audit question 4: prove, from inside, what the box can reach — and know how the
outside enforces it.
Spine: why egress is the question for sandboxes (answer keys on GitHub — cite SWE-bench/TB if
notes support; exfiltration; abuse); the enforcement menu from strongest/simplest to most
flexible: **no network** (`--network none`, only `lo` — cite; real demo) → **internal network**
(`docker network create --internal`; containers talk to each other, not out — cite; real demo) →
**internal network + allowlisting proxy container** (diagram; compose sketch with `internal: true`
network + a proxy service on both networks; keep the proxy config minimal and generic) → **host
firewall rules** (nftables model: tables/chains/hooks/policy; default-deny output/forward with
`ct state established,related accept` + explicit allows; DROP vs REJECT symptom difference;
Docker's DOCKER-USER chain — all cited, shown as config quoted/adapted from docs, not as
executed output, unless run on a real VM). IPv6 and DNS as the two classic holes. **The
five-command reachability probe** run from inside a sandbox (the page's centerpiece; real output
under `none`, `--internal`, and default bridge, side by side): `ip -br addr; ip route` →
`getent hosts example.com` → `curl -sS -m 5 -o /dev/null -w '%{http_code}\n' https://example.com`
→ `curl -m 3 http://<gateway>:<port>` (host services) → `curl -m 3 http://169.254.169.254/`
(metadata) → neighbour container by IP. Package it as a ≤30-line shellcheck-clean `probe.sh`
that prints a verdict per target.
In eval work: report the network policy as part of the eval config; "pass rate" under open
network and under no network are different measurements (the agent may fetch the fix) — if notes
support it cite the specific incidents; test the policy from inside as a CI check of the
environment itself (an environment eval); Inspect's default compose `network_mode` (cite exactly
what the note says).
Sources: netfilter, iproute2, curl, dns, cloud-metadata, inspect-sandbox, docker-compose,
swe-bench-git-leak / terminal-bench (only if they support the GitHub-answer point).

## Module 6 · Containers & isolation

### 20 · Namespaces: what a container really is  (`pages/20-namespaces.html`)
Job: dissolve the word "container" into kernel features the reader can inspect.
Spine: the claim: there is no container object in the kernel — a container is an ordinary
process started with (a) namespaces = a restricted *view*, (b) cgroups = a restricted *budget*,
(c) a different root filesystem, (d) reduced privileges (cite namespaces(7)/OCI). Namespaces
table (cite exact). Build one by hand in a `--privileged` lab container (real output):
`unshare --pid --fork --mount-proc bash` → `ps aux` shows PID 1; `--uts` + `hostname`; `--net` →
`ip addr` shows only a DOWN `lo` (cite); `--mount` + a private tmpfs; `ls -l /proc/self/ns`,
`lsns`; same-namespace test by inode number (cite); `nsenter -t PID -a` = what `docker exec` does
(cite docker exec wording). Root filesystem: chroot (and why it's not a security boundary — cite
exact wording) → pivot_root. User namespaces: root inside ≠ root outside, uid_map (cite) — and
that Docker by default does *not* use them (container root = host uid 0 — cite) unless rootless/
userns-remap. **What is NOT namespaced**: the kernel itself (`uname -r` same in every container
and the host VM — real), kernel version/bugs, time (mostly), many /proc and /sys values — hence
"shared kernel" and hence page 24.
In eval work: `docker exec` debugging = entering namespaces; "what can the agent see?" is a
namespace question, answerable with `lsns`/`/proc/PID/ns` from the host; `--pid=host`,
`--network=host`, `--privileged` in a task's compose file each delete one wall — grep task
definitions for them; PID-namespace teardown (PID 1 exit kills everything — cite) is why
container rollouts clean up processes reliably where bare-metal ones leak.
Sources: namespaces-7, pid1, mounts (chroot/pivot_root), oci, docker-run, docker-security.

### 21 · Cgroups, capabilities, and seccomp  (`pages/21-cgroups-capabilities-seccomp.html`)
Job: the other three walls: budgets, split-up root, and the syscall filter.
Spine: **cgroups v2** — the hierarchy as a filesystem at `/sys/fs/cgroup` (cite), `/proc/self/
cgroup`, controllers; memory.max/high/current/peak/events, cpu.max ("quota period" — cite) and
cpu.stat throttling, pids.max; map each Docker flag to the file it writes (real: start container
with `--memory 256m --cpus 1.5 --pids-limit 100`, read the three files inside); what enforcement
feels like (recap page 12: kill vs throttle vs EAGAIN). **Capabilities** — root split into units
(cite), the ones worth knowing (table from note: NET_RAW, NET_ADMIN, NET_BIND_SERVICE,
DAC_OVERRIDE, CHOWN, SETUID, KILL, SYS_ADMIN "the new root", SYS_PTRACE, SYS_MODULE, SYS_CHROOT,
MKNOD), reading `CapEff` from `/proc/self/status` + `capsh --decode` (real, default container vs
`--cap-drop ALL` vs `--privileged`), Docker's default set (cite exact list), why root-in-container
can't `mount` or `ip link set` (real error: `Operation not permitted` = EPERM, callback to page 8).
**seccomp** — a per-process syscall allowlist/filter (cite), Docker's default profile (cite exact
current wording/number), `Seccomp:` and `NoNewPrivs:` lines in status; **no_new_privs** — setuid
binaries stop granting privilege (cite; demo if feasible). AppArmor/SELinux: one paragraph, name
`docker-default` (cite). Summary diagram: the four walls around a container process and the
command that inspects each.
In eval work: these are the knobs of a sandbox *policy*; each has an eval-validity side (memory
limits → OOM-as-failure) and an integrity side (capabilities → can the agent remount the read-only
tests? with SYS_ADMIN yes); an agent that needs `ping`/`tcpdump` for a networking task needs
NET_RAW — dropping ALL breaks the task, so the policy must be derived per task family; record the
policy with results.
Sources: cgroups-7, oom, capabilities-7, seccomp-nnp, apparmor-docker, docker-security, docker-run.

### 22 · Docker for eval environments  (`pages/22-docker-for-evals.html`)
Job: working Docker fluency, organised around the lifecycle of a task environment: build → run →
drive → inspect → reset.
Spine: architecture in one diagram: CLI → daemon (dockerd/containerd/runc — cite OCI note) →
containers; image vs container (class vs instance); **images & layers** (cite overlayfs/storage
notes): `docker pull`, `images`, `history`, tags vs digests; **Dockerfile** for wordfreq-bench,
annotated (FROM pinned, RUN apt same-layer rule — cite, COPY, WORKDIR, `useradd agent`, USER,
exec-form CMD and why — cite); build cache behaviour in two sentences (cite); **run**: `--rm -it`,
`-d` + `exec`, `--name`, `-e`, `-u`, `-w`, `-v`/`--mount … readonly`, `--tmpfs`, `--read-only`,
`--network`, `--memory --cpus --pids-limit`, `--init` (each one line, cite semantics; real demo of
the important ones); **inspect**: `ps -a`, `logs`, `inspect --format`, `exec`, `cp`, `diff`
(`docker diff` as "what did the agent change" — real output), `stats`; **reset**: containers are
cheap — a fresh container per rollout is the reset mechanism; anonymous/named volumes persist and
are the exception (cite); **compose**: a 25-line `compose.yaml` for a two-service task (default +
db), service-name DNS, `internal: true` (cite), `docker compose up -d / exec / down -v`. Docker
exit codes 125/126/127 (cite). Docker Desktop on a Mac is a VM — performance/paths caveats in one
callout. Secrets: never ENV/ARG (cite), `docker history` demo showing a leaked ARG for real.
Layers keep deleted files: the COPY-then-rm demo (use the verified R5 extra_finding; re-run it).
In eval work: per-rollout fresh container = independence between samples (link sibling course
statistics pages — correlated failures break the error bars); image digest in the results file;
`docker diff` + `docker logs` + exit code as the minimal post-mortem of any rollout; the deleted-
file-in-layer trap is solution leakage through the image (forward to page 26).
Sources: docker-run, dockerfile, docker-storage, docker-compose, docker-logs-inspect, overlayfs, oci.

### 23 · Locking down a container  (`pages/23-hardening-containers.html`)
Job: turn a default `docker run` into a defensible sandbox, knob by knob, knowing what each knob
costs the task.
Spine: start from the threat list for an agent sandbox (tamper with grader; read the key; reach
the network; exhaust the host; escape to host; persist between rollouts). Then the hardening
ladder, each rung = flag → what it blocks → how to verify from inside → what legitimate task
behaviour it breaks: non-root `--user` (+ files owned appropriately); `--cap-drop ALL` (+ add back
per task); `--security-opt no-new-privileges`; `--read-only` + `--tmpfs /tmp` (+ writable `/app`
volume) — real error when writing elsewhere; `--network none`/internal; `--memory/--cpus/
--pids-limit` (fork-bomb containment — describe, cite pids.max; do NOT run a fork bomb on the
author machine without `--pids-limit 50` in a throwaway container; safe demo OK); never
`--privileged`, never mount `/var/run/docker.sock` (cite root-equivalence wording; o1 incident as
the real-world exposed-daemon case), no host bind mounts writable, no `--pid=host`/`--network=
host`; rootless Docker / userns-remap as the daemon-level upgrade (cite, incl. limitations).
Assemble: the full hardened `docker run` line and the equivalent compose service (cap_drop,
security_opt, read_only, tmpfs, mem_limit, pids_limit, user, init — cite compose keys), run
wordfreq-bench in it for real, then run an "inside-out verification" script (≤30 lines,
shellcheck-clean) that checks each property from inside (`id -u`, CapEff all zeros, NoNewPrivs 1,
root fs ro, only `lo`, memory.max set, pids.max set) and prints PASS/FAIL per line — real output.
Caveat box: all of this still shares the host kernel → page 24; Docker docs' own framing of the
four security areas (cite).
In eval work: hardening is a *measurement* decision as much as a security one — each rung can
change task solvability, so re-validate the oracle solution under the hardened policy (Terminal-
Bench oracle-solution practice — cite); ship the verification script as an environment self-test
that runs before every eval.
Sources: docker-security, docker-run, docker-compose, seccomp-nnp, capabilities-7, oom,
o1-docker-incident, terminal-bench.

### 24 · The isolation ladder: containers, gVisor, microVMs  (`pages/24-isolation-ladder.html`)
Job: choose an isolation technology from a threat model instead of from habit.
Spine: the shared-kernel fact and why it is the crux (every container syscall lands in the one
host kernel; attack surface = the whole syscall interface minus seccomp) — cite Firecracker
paper's argument; the ladder as one ASCII figure with three columns (container / gVisor / microVM)
showing where the app's syscalls go: host kernel directly → Sentry (userspace kernel, Go) +
Gofer → guest kernel → KVM + tiny VMM (cite gVisor & Firecracker notes; numbers only as
verified, with site-vs-paper distinctions); Kata and Cloud Hypervisor placed on the ladder in a
sentence each (cite); full VMs (OSWorld — cite) as the top rung and when you need them anyway
(GUI, other OSes, kernel-level tasks); costs going up the ladder (startup, memory, density,
compatibility, need for KVM/bare metal or nested virt — cite kvm note), so the ladder is a
trade-off curve, not a ranking. **The four boundaries** as the organising checklist — isolation
(code execution stays in), egress (network), tenancy (rollouts/customers don't see each other),
secrets (what's inside the box, incl. snapshots) — table: boundary × how each rung addresses it ×
the one check that would show it failing. **Snapshots**: filesystem vs memory snapshots, why
evals love them (fast identical reset; fork N rollouts from one state), and the two cautions from
the Firecracker docs (uniqueness/entropy on clone; secrets in memory captured) — cite exactly.
AISI's sandboxing taxonomy (T0–T2 / H0–H3 / N0–N2 per the note; the levels live in the repo's Technical Guidance PDF, not the
blog) and their stated reasons for k8s/Proxmox providers (cite exactly; AISI does NOT make the shared-kernel argument — cite
Firecracker/gVisor for that; do not repeat the PDF's wrong claim about compose's default network mode); the o1
system card incident (Sept 2024 card only; o1-preview) — quote OpenAI's exact framing from the note: the card says
its infrastructure does NOT rely on container-to-host isolation or the VM boundary for security, and never says
what it does rely on. Do not claim 'the VM boundary held'. Pair with gVisor's 'a sandbox is not a substitute for
a secure architecture' (cite). Choosing: a short decision guide keyed on *who wrote the code
that runs* and *what is on the host/network worth stealing*, ending with "a reward-hacking agent is
an adversarial guest; a threat model that assumes cooperative guests does not cover it."
In eval work: isolation choice also affects *measurement* (gVisor syscall compatibility/perf can
change task outcomes — cite compat note; VM boot time changes throughput and cost per rollout);
Inspect makes the sandbox a config choice (cite providers list) — the portable skill is the
provider interface: exec with argv/stdin/cwd/env/user/timeout → exit code + both streams, plus
file read/write (cite).
Sources: gvisor, firecracker, kata-ch, kvm, oci, aisi-sandboxing, o1-docker-incident, osworld-env,
inspect-sandbox, humaneval-sandbox.

## Module 7 · Linux in eval harnesses

### 25 · How harnesses drive a sandbox  (`pages/25-how-harnesses-use-linux.html`)
Job: connect everything so far to the actual interface between an eval harness and a Linux box.
Spine: the universal loop (diagram): harness creates sandbox → copies files in → model emits tool
call → harness `exec`s it in the sandbox → returns stdout/stderr/exit code (truncated) to the
model → … → scorer execs checks / reads files → teardown. **Inspect in depth** (cite everything):
SandboxEnvironment exec signature and ExecResult; read_file/write_file; docker provider and its
default compose; the `default` service convention; per-sample compose projects; `bash()` tool
(timeout, user) vs `bash_session`; limits (output limit, time/working limits, max_sandboxes);
files/setup; scorer access; cleanup flags and how to `docker exec` into a live sample for
debugging. A minimal but complete Inspect task for wordfreq-bench (~40 lines Python + compose.yaml)
— syntax-checked against the docs note; mark clearly if not executed. **Terminal-Bench** (cite):
task directory anatomy, tmux-driven terminal, tests run after the agent, oracle solution; Harbor.
**SWE-bench** (cite): three image layers, patch-apply-and-test grading, resource guidance. Each
harness decision re-read as a Linux concept from an earlier page (table: harness feature → Linux
mechanism → course page): exec-per-call ↔ non-interactive shell (p2); stdout/stderr split (p4);
timeout ↔ signals/137 (p10); user param ↔ uid (p7); compose network_mode ↔ netns (p19/20); limits
↔ cgroups (p21); tmux ↔ TTY/interactive programs (p27).
In eval work: reading a new benchmark = finding these five things in its repo: the image
definition, the exec path, the timeout/limits, the network policy, where grading runs (inside or
outside the box, before or after the agent exits). Agent bridge / external agents in the sandbox
and what that does to network policy (cite).
Sources: inspect-sandbox, terminal-bench, swe-bench-docker, aisi-sandboxing.

### 26 · Environment integrity: where cheating lives  (`pages/26-environment-integrity.html`)
Job: the specialty page. Every integrity failure in an agentic eval is a Linux fact: something
was readable, writable, reachable, or still running that shouldn't have been.
Spine: define reward hacking / environment integrity briefly (link sibling course pages 11, 21–22);
the **leak/tamper taxonomy as Linux surfaces** — table: surface → published incident (cited) →
the check → the fix: (1) *git history* — SWE-bench issue (exact number/date/commands from note);
`git log --all`, reflog, tags, unreachable objects (cite Pro Git); fix = build repo from exported
tree, verify with `git count-objects -v`/`git log --all | wc -l`; real demo on a toy repo. (2)
*image layers* — deleted-in-later-layer files (cite; callback page 22). (3) *filesystem* — tests/
answers readable or writable by agent uid; METR examples of modified tests/scorer (cite);
ImpossibleBench numbers on read-only/hidden tests (cite exactly). (4) *process & env* — grader
running in the same PID namespace/uid (readable `/proc/PID/environ`, cmdline, call-stack tricks
per METR — cite). (5) *network* — reference solution public on GitHub/PyPI; open egress. (6)
*the harness/host* — exposed Docker API (o1 — cite), writable host mounts. (7) *state across
rollouts* — shared volumes, reused containers (Anthropic wording — cite).
**Design principles** derived from the taxonomy: grade outside the box, after the agent exits, on
artifacts copied out or on a fresh container; held-out tests never enter the sandbox (Terminal-
Bench practice — cite exactly what the note supports); least privilege (non-root, ro mounts);
default-deny egress; fresh environment per rollout; small trusted core (scorer, policy, logging)
readable in one sitting. **Measuring it**: report cheat rate alongside pass rate; spontaneous vs
elicited cheating measure different things (model propensity vs environment weakness — frame as
the course's analytical distinction, cite METR/ImpossibleBench where they support it); a detector
can miss → cheat rate is a lower bound; red-team your own environment: run an "attacker" rollout
whose instruction is to find the answer without solving the task, and treat any success as an
environment bug. Use the 2606.08960 lead ONLY if its note verifies it.
Worked red-team of wordfreq-bench (real): a deliberately sloppy build (tests in image at 644,
full git history, agent root, open network) → enumerate, from inside, five ways to obtain a pass
without fixing the bug — described at checklist level ("the expected output is readable at …") —
then the fixed build and the same checks failing. Keep altitude per AUTHORING.md Safety section.
Sources: swe-bench-git-leak, git-internals, metr-reward-hacking, impossiblebench, terminal-bench,
o1-docker-incident, anthropic-agent-evals, overlayfs, dockerfile, reward-hack-sandbox-policies.

### 27 · Reading terminal transcripts  (`pages/27-reading-terminal-transcripts.html`)
Job: error analysis for terminal agents: classify what went wrong in a rollout from its commands,
outputs, and exit codes — and separate model failures from environment failures.
Spine: what a transcript contains (tool call argv/script, stdout, stderr, exit code, duration,
truncation markers) and what it doesn't (the screen state, background processes, the filesystem);
a **field guide** of recurring Linux-level patterns, each as: what you see → mechanism (page link)
→ whose fault → fix. Must include (produce each real snippet in Docker): `command not found` 127
(PATH/non-login shell/not installed/Alpine); `Permission denied` 126 vs EACCES on files;
`Operation not permitted`; interactive prompt hang → timeout (apt tzdata, `git commit` opening an
editor, `ssh` host-key prompt, `sudo` password, `rm -i`, pagers: `git log`/`man`/`less` waiting for
a keypress — `GIT_PAGER=cat`, `PAGER=cat`, `-y`, `DEBIAN_FRONTEND`); `Could not get lock
/var/lib/dpkg/lock-frontend`; `externally-managed-environment`; `No space left on device`;
`Killed`/137; `Temporary failure in name resolution` / curl 6/7/28/60; `Read-only file system`;
state not persisting between tool calls (`cd`, `export`, venv activate) under exec-per-call
harnesses; background server dies when the call returns; heredoc/quoting mangling when a model
writes files via `echo`/`cat <<EOF` (unquoted EOF expanding `$vars`; demonstrate `<<'EOF'`);
truncated output hiding the error line; timezone/locale differences; TTY-less behaviour (`not a
tty`, programs changing output when piped — `ls` columns, colours, progress bars) and why
Terminal-Bench uses tmux (cite). Then the **triage procedure**: exit code → last stderr lines →
duration vs timeout → environment counters (OOM, disk) → reproduce by `docker exec`ing the same
argv as the same user. **Failure accounting** (addendum §4): every scheduled rollout ends in exactly one recorded outcome; show a small
invented run reported three ways (correct/scheduled, correct/completed, completed/scheduled) and why dropping
infrastructure failures biases conditional quality when hard tasks fail more. A coding scheme for failure categories: model-capability / model-Linux-
fluency / environment-defect / harness-defect / integrity-violation, and why the second and third
must be separated before you report a score (cite Anthropic post on infra noise; Terminal-Bench
failure analysis if the note has it). Practice: three short annotated transcripts (constructed for
wordfreq-bench but with REAL command output), reader classifies, solutions in details.
Sources: terminal-bench, anthropic-agent-evals, inspect-sandbox, apt-dpkg, pip-repro, curl,
bash-manual; mostly executed mechanics. Link sibling course pages 04–05 (error analysis).

### 28 · Capstone: the ten-minute audit  (`pages/28-ten-minute-audit.html`)
Also (addendum): end with a *design-and-defend* section modelled on the networking course's readiness review
(`../../networking/networking-tut/pages/23-readiness-review.html`): a design brief (a team's agentic benchmark with
named environment problems), the artifacts to bring (environment diagram with trust boundaries, sandbox policy,
rollout record schema incl. exit code/OOM/timeout fields, one reproduced incident report with evidence → hypothesis →
next discriminating test, measurement policy for infra failures and cheating), and an observable readiness rubric
(Explain / Diagnose / Design / Measure / Communicate: 'ready enough' vs 'practice more if…').
Job: assemble the course into one timed procedure and one portfolio-grade artifact.
Spine: the scenario (you're handed shell access to a benchmark's task container/VM and asked "can
we trust scores from this?"); the procedure as five blocks, ~2 minutes each, each with 3–6
commands, what to look for, and the eval-validity question it answers: (0) orient: `id; hostname;
cat /etc/os-release; uname -r; cat /proc/1/cgroup; ls -la /.dockerenv` — VM or container? who am
I? (1) running: `ps -ef --forest`, `ss -tulpn`, `systemctl --failed` if systemd; (2) mounted:
`findmnt`, `findmnt -O ro`, `df -hT`, writable-dir sweep `find / -xdev -writable -type d`, tmpfs;
(3) owns: `ls -la / /app /opt`, setuid sweep, `sudo -l`, capabilities `grep Cap /proc/self/status`,
NoNewPrivs/Seccomp, files readable by the agent uid that mention test/expected/solution/answer,
`git log --all | head`; (4) reach: the five-command probe from page 19; (5) logs & limits:
`/var/log`, `journalctl` or `docker logs` from outside, `cat /sys/fs/cgroup/{memory.max,cpu.max,
pids.max}`, `memory.events`. Provide `audit.sh` (this one may exceed 30 lines — say why, keep it
≤80, shellcheck-clean, read-only operations only) printing a one-page report; run it for real
against (a) the sloppy wordfreq-bench build and (b) the hardened one from pages 23/26 and show
both reports. Then the **write-up template** — findings → validity impact → fix → residual risk —
with a filled example. The outside-the-box half: `docker inspect` fields (Privileged, CapDrop,
ReadonlyRootfs, NetworkMode, Mounts, Memory, User, Env), image history, digest. Closing: where to
go next (Appendix G checklist; sibling evals course; Inspect docs; Linux Journey if verified);
what you can now claim in an interview, concretely.
Sources: everything prior; cite sparingly here (defaults only). Mostly executed mechanics.

## Appendices (kicker "Appendix X"; labs optional; shorter, more tabular)

### A · The working set of commands  (`appendices/a-command-reference.html`)
~70 commands grouped by the five audit questions + text + docker, each: one-line purpose, the 2–3
forms used in the course, page link. Include a "not installed in minimal images → package name"
column (ps → procps, ip/ss → iproute2, dig → dnsutils/bind9-dnsutils, ping → iputils-ping, etc.
— verify each package name with `dpkg -S`/`apt-file`-style checks in ubuntu:24.04).

### B · Exit codes and signals  (`appendices/b-exit-codes-signals.html`)
Full tables: shell/POSIX codes, timeout's, Docker's, curl's most common, signal numbers/defaults,
128+N arithmetic; Python `subprocess` returncode negative-N convention (verify by running:
`-9`), and how Docker/Inspect report the same death. All cited or executed.
Sources: bash-manual, posix-shell, coreutils, signal-7, docker-run, curl.

### C · Binary, octal, and CIDR math  (`appendices/c-binary-octal-cidr.html`)
The math mini-lesson: bits and place value; why octal maps to rwx (3 bits); worked chmod numbers
both directions; umask as bit-clearing (not subtraction — show the case where subtraction gives
the wrong answer); special bits' fourth digit; IPv4 as 32 bits; prefix length → mask → network/
broadcast/host count, worked for /8 /12 /16 /24 /28; "is 172.20.5.9 private?" worked via the /12;
Python `ipaddress` stdlib to check answers. Pencil-recomputable.

### D · Regular expressions  (`appendices/d-regex.html`)
Literals, `.`, classes, anchors, quantifiers, groups, alternation; BRE vs ERE (`grep` vs `grep -E`)
vs PCRE/Python differences that bite; greedy matching; quoting regexes from the shell; ten worked
patterns for log work (exit codes, IPs, timestamps, `Traceback`, JSON field extraction caveat →
use jq). All examples run for real.

### E · macOS vs Linux  (`appendices/e-macos-vs-linux.html`)
For the reader's daily friction: zsh vs bash; BSD vs GNU userland table (sed -i, date, stat,
readlink -f, grep -P, xargs, find, base64, `ls --color`); no /proc, no `ip`/`ss`, no namespaces/
cgroups (Docker Desktop = Linux VM); case-insensitive filesystem; Homebrew `coreutils` g-prefixed;
line endings; architecture (arm64 vs amd64 images, `--platform`, emulation slowness → eval
timeouts on Apple Silicon — verify wording against Docker docs if cited, else describe as executed
observation). macOS-side behaviour must be verified by actually running on this Mac (it is one).

### F · Man pages and getting help  (`appendices/f-getting-help.html`)
`man` sections (1,2,5,7,8 — why `signal(7)` vs `kill(1)` vs `kill(2)`), reading a SYNOPSIS, searching
within `less`, `man -k`/`apropos`, `--help`, `help` for builtins, `type`, `info` (mention), man7.org
as the canonical online copy, `tldr` (mention), why minimal images have no man pages and what to
do; how to read `docker <cmd> --help`. How this course cites: what `[signal(7)]` means.

### G · Skills checklist and portfolio labs  (`appendices/g-skills-checklist.html`)
Written LAST by the editor (not a page author): per-module "deep enough when…" self-tests using
`ul.checklist`, interview-style questions with answers in `details.solution`, and five portfolio
lab specs (e.g. "audit a public benchmark's task image and publish the write-up"; "hardened
sandbox + inside-out verification script"; "reachability probe as CI for an eval environment";
"git-history leak detector for task repos"; "transcript failure-mode coder over a public
Terminal-Bench/Inspect log").
