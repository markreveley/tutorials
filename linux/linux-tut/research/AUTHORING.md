# Authoring Guide — linux-tut

This is the binding contract for every page in the course. Read all of it before writing.
The course is a sibling of `../../evals/evals-tut` ("Understanding LLM Evals") and shares its
engine, voice, and provenance discipline. Where this guide is silent, imitate that course
(a good model page: `../../evals/evals-tut/pages/11-evaluating-agents.html`).

## The course in one paragraph

**Linux for Evals Engineers** teaches Linux to someone who wants to be employable doing AI
evaluation work — especially *agentic* evals, where the thing under test is a model acting inside
a Linux sandbox. Every agentic benchmark is, physically, a pile of Linux boxes: containers or VMs
that get built, reset, driven by a harness, and graded. The environment is part of the measuring
instrument, so an evals engineer who cannot read that environment cannot vouch for the score.
The course's competence target (the "ten-minute audit"): *dropped into an unfamiliar Linux box as
root, within ten minutes you can say what is running, what is mounted and whether it is
read-only, who owns what, what the box can reach over the network, and where the logs are* —
and you can explain why each answer matters for the validity of an eval.

This is **not** a sysadmin course. Scope is decided by one question: *does an evals engineer
need this to build, debug, audit, or harden an eval environment, or to read an agent's terminal
transcript?* In scope: shell, text processing, users/permissions, processes/signals, resources,
logs, mounts, packages/reproducibility, networking for sandboxes, namespaces/cgroups, Docker,
isolation technologies, harness–sandbox interfaces, environment integrity. Out of scope: kernel
building, boot loaders, desktop Linux, RAID/LVM, mail servers, Kubernetes operations, advanced
routing, shell scripting beyond ~30 lines (past that the course says: use Python).

## The audience

A working technical person (software engineer, technical PM, career-changer with some Python)
on a **Mac**, who has opened a terminal and run `cd`, `ls`, `git`, `pip`, but has never
administered a Linux machine, never thought about file descriptors, signals, mounts, or
namespaces, and has no networking background. Every piece of jargon gets defined at first use.
They have ideally read the sibling evals course but do not need to have: define eval terms
briefly at first use too (the glossary has them).

## Target platform

- **Ubuntu 24.04 LTS** (and Debian 12 where identical) is the reference system: GNU coreutils,
  bash, apt, systemd, cgroup v2, iproute2. Output shown in pages must be what Ubuntu 24.04 prints.
- Mention **Alpine** (BusyBox, musl, `apk`, `ash` not bash) where the difference bites — many
  task images are Alpine-based and agents trip on it.
- The reader is on macOS; when a command behaves differently on macOS/BSD say so briefly and
  link `../appendices/e-macos-vs-linux.html`.
- The reader's lab (page 1) is a disposable Docker container for most pages, and a real VM for
  the pages that need a kernel of one's own (systemd, firewalls, namespaces as root).

## The cardinal rule: provenance

Two kinds of statement, two standards.

**1. Mechanics you can run.** How a command behaves, what a file contains, what an error looks
like. Standard: **you ran it.** Every command and every line of output shown in a page must have
been executed by you in a real Linux container (Docker is available on this machine — see
"Verifying commands" below) and the output pasted from the real run (trimmed with `…` where
long; hostnames/IDs may be tidied). Never write terminal output from memory. If something cannot
be run in a container (systemd, nftables on a VM), it must instead be backed by a verified source
note and the page must not show invented output — describe, or show output quoted from docs.

**2. Facts about the world.** Defaults ("Docker grants these 14 capabilities by default"),
guarantees ("SIGKILL cannot be caught"), numbers, history, incidents ("agents recovered fixes
from git history in SWE-bench"), positions, and quotes. Standard: **traces to a verified source
note in `research/sources/*.json`.** Rules:

1. If the note marks a claim `confirmed`, you may state it, with the verified specifics, and cite it.
2. If marked `corrected`, use ONLY the corrected version.
3. If marked `unverifiable`, do not state it as fact. Omit it or flag it explicitly.
4. Never add numbers, defaults, version facts, or incident details from your own memory. If it's
   not in the notes and you can't run it, it's not in the course. If you badly need a fact that
   is missing, you may fetch the primary source yourself (man7.org, docs.kernel.org,
   docs.docker.com, inspect.aisi.org.uk, arXiv, RFCs), verify it, and **append a claim to the
   relevant source note** (same JSON shape) before citing it.
5. General explanatory material (what a process is, how a pipe connects two programs, what
   binary is) needs no citation. Specific defaults, limits, guarantees, and empirical findings do.

## Citations

- Inline: superscript link right after the claim:
  `<a class="cite" href="https://man7.org/linux/man-pages/man7/signal.7.html" title="signal(7), Linux man-pages">[signal(7)]</a>`
- Short tag conventions: man pages as `[name(section)]` e.g. `[capabilities(7)]`; kernel docs as
  `[Kernel: cgroup-v2]`; Docker docs as `[Docker: run]`, `[Docker: security]`; others as listed in
  the `tag` field of each source note (e.g. `[Bash Manual]`, `[POSIX]`, `[FHS]`, `[Inspect]`,
  `[Terminal-Bench]`, `[SWE-bench]`, `[gVisor]`, `[Firecracker]`, `[METR]`, `[RFC 1918]`).
  Use the `tag` and `url` from the source note verbatim so tags are consistent site-wide.
- End of page: a `.srcbox` listing every source cited on the page with full citation and link.

## Page template

Every page uses exactly this skeleton. Pages live in `pages/` (appendices in `appendices/`);
asset paths are `../assets/...`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PAGE TITLE · Linux for Evals Engineers</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<div class="layout">
  <aside class="sidebar" data-nav></aside>
  <div class="content">
  <main class="page">

    <p class="kicker">Module N · Module Name</p>
    <h1>Page title in sentence case</h1>
    <p class="lede">One or two sentences: what this page teaches and why an evals engineer should care. Readable on its own.</p>

    <!-- body -->

    <div class="lab"> … </div>

    <div class="srcbox">
      <span class="label">Sources for this page</span>
      <ul>
        <li>signal(7), Linux man-pages project. <a href="https://man7.org/linux/man-pages/man7/signal.7.html">man7.org/…/signal.7.html</a></li>
      </ul>
    </div>

  </main>
  </div>
</div>
<script src="../assets/nav-data.js"></script>
<script src="../assets/glossary-data.js"></script>
<script src="../assets/wiki.js"></script>
</body>
</html>
```

Notes:
- Sidebar and prev/next links are injected by `wiki.js` — do not write them by hand.
- Page titles, filenames, and module names are fixed by `assets/nav-data.js`. Do not rename.
  The kicker for appendices is `Appendix X`.
- Give every `h2`/`h3` an `id` (kebab-case) so anchors work.
- HTML-escape `<`, `>`, `&` inside `<pre>`/`<code>` (`2&gt;&amp;1`, `&lt;&lt;EOF`). This course is
  full of them; an unescaped `<` silently eats text.

## Components (use them, don't invent new ones)

- `<div class="keyidea"><span class="label">Key idea</span> …</div>` — the one takeaway of a section. ≤1 per major section.
- `<div class="evals"><span class="label">In eval work</span> …</div>` — **the course's through-line.**
  Plum box tying the Linux concept to evaluation practice: what breaks in a benchmark when this
  goes wrong, what an agent does with it, what you'd check in an audit. **Every page has at
  least one, most have two or three.** These must be concrete ("a harness that captures only
  stdout will log an empty string when `pytest` crashes to stderr, and the grader scores a
  harness bug as a model failure"), never vague ("this is important for evals").
- `<div class="callout"><span class="label">Background / Example / Why this matters</span> …</div>` — blue, neutral asides.
- `<div class="warn"><span class="label">Caveat</span> …</div>` — amber, limitations and caveats.
- `<div class="pitfall"><span class="label">Pitfall</span> …</div>` — red, mistakes practitioners actually make.
- `<div class="card">…</div>` — grouped material, e.g. a worked example or checklist.
- `<div class="diagram">ASCII diagram</div>` — monospace, preserved whitespace; ≤72 cols. Use real ASCII art for process trees, fd plumbing, network paths, isolation layers.
- Terminal sessions: `<pre class="term"><code><span class="p">$</span> command
<span class="o">output line</span></code></pre>` — `.p` is the prompt (`$` for a normal user, `#` for root),
  `.o` wraps output, `.c` wraps an inline `# comment`, `.hl` highlights the part of the output the prose
  talks about. Plain `<pre><code>` (light) is for file contents and scripts.
- `<div class="lab"><span class="label">Lab</span> …</div>` — hands-on exercises (see Labs below), with
  `<details class="solution"><summary>Solution</summary> … </details>` for answers.
- `<div class="math">…</div>` — display math (Appendix C only, realistically). Variables italic; `<span class="plain">` for words; Unicode operators.
- `<kbd>Ctrl</kbd>+<kbd>C</kbd>` for keys.
- Tables for enumerable comparisons; explain implications in prose around them.

## Labs

Linux is learned with fingers. Every course page (not necessarily appendices) ends — just before
the srcbox — with one `.lab` box containing **3–6 exercises** that:
- are runnable in the page-1 lab environment (say which: "container lab" or "VM lab");
- start with a setup one-liner if needed;
- escalate: first reproduce what the page showed, then predict-then-verify ("before running it,
  write down what you expect `echo $?` to print"), and last an **eval-flavoured task** ("the
  harness reports the agent's test run 'passed' with empty output; find out which stream pytest's
  error went to");
- have a `<details class="solution">` with the real commands and real output, verified by you.

## Verifying commands (Docker)

Docker Desktop is running on the authoring machine (aarch64, cgroup v2). Images already pulled:
`ubuntu:24.04`, `debian:bookworm-slim`, `alpine:3.20`. Conventions so parallel authors don't collide:

- One-shot: `docker run --rm ubuntu:24.04 bash -c '…'`.
- Named containers: prefix with `lt-<your-page-number>-`, and always remove them when done
  (`docker rm -f`). Never touch containers/images you didn't create. Never `docker system prune`.
- Need tools? `apt-get update && apt-get install -y --no-install-recommends procps iproute2 …` inside the container.
- Need privileges for namespace/mount demos? `--privileged` or `--cap-add SYS_ADMIN` on a
  throwaway container is fine. Remember Docker Desktop's Linux is a VM: host-level things
  (systemd, the VM's own nftables) are not representative — don't show them as verified output.
- A non-root prompt (`$`) in a page means you ran it as a non-root user (`useradd -m learner`, `su - learner`)
  or the distinction is immaterial. Permission demos MUST really be run as non-root: root bypasses permission checks.
- Keep a record: save the exact commands+output you relied on to `research/verify/<page-file-stem>.txt`.

## Glossary terms

First meaningful mention of a glossary concept on a page gets marked:
`<span class="term" data-g="exit-status">exit status</span>`
— dashed underline with hover tooltip. Mark only the first mention per page. Use ONLY slugs from
the canonical list below. Don't mark words inside headings, lede paragraphs, links, `<pre>`, or `<code>`.
Aim for 6–15 marked terms per page.

### Canonical glossary slugs

Shell: `shell`, `terminal`, `bash`, `command`, `argument`, `option-flag`, `path-variable`, `absolute-path`, `relative-path`, `working-directory`, `home-directory`, `exit-status`, `stdin`, `stdout`, `stderr`, `file-descriptor`, `pipe`, `redirection`, `here-document`, `glob`, `quoting`, `variable-expansion`, `command-substitution`, `shebang`, `script`, `strict-mode`, `shellcheck`, `regex`, `grep`, `sed`, `awk`, `jq`, `jsonl`, `xargs`, `man-page`, `builtin`, `alias`, `tty`, `pager`, `interactive-prompt`, `tmux`, `ssh`, `gnu-coreutils`, `busybox`, `posix`

Files & storage: `filesystem`, `fhs`, `root-directory`, `inode`, `hard-link`, `symlink`, `dotfile`, `everything-is-a-file`, `device-file`, `dev-null`, `proc-filesystem`, `sysfs`, `tmp-directory`, `mount`, `mount-point`, `bind-mount`, `read-only-mount`, `tmpfs`, `overlayfs`, `volume`, `block-device`, `disk-usage`

Identity & permissions: `user`, `uid`, `gid`, `group`, `root-user`, `sudo`, `passwd-file`, `shadow-file`, `permission-bits`, `octal-mode`, `chmod`, `chown`, `umask`, `setuid`, `sticky-bit`, `least-privilege`, `privilege-escalation`, `service-account`

Processes & system: `process`, `pid`, `parent-process`, `fork-exec`, `daemon`, `zombie-process`, `orphan-process`, `pid-1`, `init`, `systemd`, `unit`, `journal`, `syslog`, `dmesg`, `signal`, `sigterm`, `sigkill`, `sigint`, `sighup`, `timeout`, `job-control`, `background-process`, `environment-variable`, `secret`, `load-average`, `oom-killer`, `rlimit`, `nice`, `cpu-time`, `wall-clock-time`, `memory-rss`, `swap`, `kernel`, `system-call`, `user-space`, `strace`

Packages & reproducibility: `package-manager`, `apt`, `dpkg`, `repository`, `dependency`, `version-pinning`, `lockfile`, `reproducible-build`, `base-image`, `distribution`, `debian`, `ubuntu`, `alpine`, `musl-glibc`, `pip`, `virtual-environment`

Networking: `ip-address`, `ipv4`, `ipv6`, `cidr`, `subnet`, `private-address-range`, `network-interface`, `loopback`, `localhost`, `routing-table`, `default-gateway`, `nat`, `port`, `socket`, `tcp`, `udp`, `listening-socket`, `bind-address`, `dns`, `resolver`, `hosts-file`, `http`, `tls`, `certificate`, `proxy`, `egress`, `ingress`, `firewall`, `default-deny`, `allowlist`, `nftables`, `iptables`, `bridge-network`, `veth`, `packet-capture`, `icmp`, `metadata-service`

Containers & isolation: `container`, `image`, `layer`, `dockerfile`, `docker`, `docker-daemon`, `docker-socket`, `docker-compose`, `registry`, `image-digest`, `tag`, `entrypoint`, `namespace`, `pid-namespace`, `mount-namespace`, `network-namespace`, `user-namespace`, `uts-namespace`, `cgroup`, `capability`, `seccomp`, `no-new-privileges`, `apparmor`, `privileged-container`, `rootless`, `container-escape`, `chroot`, `oci`, `runc`, `container-runtime`, `gvisor`, `microvm`, `firecracker`, `hypervisor`, `kvm`, `virtual-machine`, `snapshot`, `attack-surface`, `threat-model`, `trust-boundary`, `isolation`, `tenancy`

Evals: `eval`, `benchmark`, `agent`, `harness`, `sandbox`, `environment`, `trajectory`, `transcript`, `tool-call`, `bash-tool`, `task-image`, `verifier`, `scorer`, `oracle-solution`, `held-out-tests`, `reward-hacking`, `environment-integrity`, `solution-leakage`, `test-tampering`, `git-history-leak`, `flaky-test`, `nondeterminism`, `reset`, `rollout`, `infrastructure-failure`, `inspect`, `terminal-bench`, `swe-bench`, `state-based-evaluation`, `outcome-based-evaluation`, `error-analysis`, `failure-mode`

## Voice

- Plain, direct, confident. Second person where natural ("when you `exec` into the task container…").
- Teach **derived rules, not memorized ones**: always show *why* a mechanism exists so the reader
  can re-derive behaviour when their situation breaks the pattern. ("Use `2>&1`" is a memorized
  rule; "a process has numbered output channels, the harness only captured channel 1, and the
  error went to channel 2" is a derived one.) Prefer the underlying model (file descriptors,
  the process tree, the mount table, the routing table) over lists of flags.
- **Few commands, deeply.** The working set for the whole course is ~70 commands (Appendix A).
  Don't tour every flag; teach the three you'll use and how to find the rest (`man`, `--help`).
- Anticipate the entry-level reader's confusion explicitly ("If you're wondering why `cd` isn't a program…").
- Numbers and defaults are precious: give the actual value and cite it, not "a small default".
- No hype, no filler, no history lectures beyond what explains a present-day quirk.
- En-dashes/em-dashes fine; section headings in sentence case.
- Each page: roughly 1,300–2,300 words of body prose (appendices may be shorter or more tabular),
  at least one diagram or fully worked terminal example, at least one pitfall or caveat box,
  at least one `.evals` box, one `.lab`.
- Cross-link generously to other pages (relative hrefs), appendices, and — where the sibling
  course covers the eval concept in depth — to it, e.g.
  `<a href="../../../evals/evals-tut/pages/11-evaluating-agents.html">Understanding LLM Evals, page 11</a>`
  (from `pages/`; that relative path is correct for the repo layout).

## Quality bar for examples

Worked examples are fully worked and **real**: a reader who types what the page shows, in the lab
from page 1, sees what the page shows. Scripts must pass `shellcheck` (installed at
`/opt/homebrew/bin/shellcheck`) unless the page is deliberately showing a bug — then say what
shellcheck reports. Python snippets: stdlib only, runnable as shown.

## Safety

The course teaches defensive environment engineering: building, auditing, and hardening
sandboxes, and recognising how agents have gamed environments in published incidents. Describe
integrity failures at the level published sources do, framed as things to check and close.
Don't write container-escape exploit walkthroughs; "a mounted Docker socket gives root on the
host — here is how to check that you haven't mounted one" is the right altitude.

## Addendum (2026-09-21): conventions adopted from the sibling networking course

A second sibling now exists: **Networking for LLM Evals** at `../../networking/networking-tut`
(from `pages/`: `../../../networking/networking-tut/pages/<file>`). The course owner singled out
its evals-first presentation as the model. Adopt these, on every page:

1. **Check your understanding.** Every course page has, just before the `.lab`, one
   `<div class="check"><span class="label">Check your understanding</span> <p>scenario question</p>
   <details class="solution"><summary>Reveal the reasoning</summary> … </details></div>`.
   The question is an *eval scenario that requires judgment*, not recall — in the style of
   "A new runner improves 'accuracy' by dropping all samples that time out. What would you ask in
   review?" The reasoning names what to establish, what evidence would discriminate between
   causes, and how it bears on the reported score. (The lab stays: labs are fingers, the check is judgment.)
2. **Discuss / Navigate / Design.** The course's abilities are framed the way a job uses them:
   *discuss* (explain the mechanism and its effect on a score in plain language), *navigate*
   (investigate from inside the environment, find the last thing that worked, bring evidence),
   *design* (choose and defend an environment policy). `.evals` boxes should make clear which
   ability they serve where natural; don't force the labels.
3. **Evidence vs hypothesis.** When diagnosing, separate what was observed from what is
   supposed, and name the next *discriminating* test. Never present a plausible cause as proven.
4. **Failure accounting.** Infrastructure outcomes are observations about the *run*, not about
   the model. Wherever a page touches failures (timeouts, OOM, network, permissions), say how the
   outcome should be recorded and what it does to the denominator: report `correct / scheduled`,
   `correct / completed`, and `completed / scheduled` as different quantities; never drop
   infrastructure failures silently; decide the primary metric before looking at results.
5. **Depth triage.** Be explicit about what to *learn to use*, what to merely *recognize*, and
   what to *leave to a specialist role* — a short table or sentence where a topic is deep
   (capabilities, nftables, systemd, overlayfs internals, IPv6).
6. **Division of labour with the networking course.** It teaches networking *concepts* (the
   request journey, DNS, TCP, TLS, HTTP, streaming, latency, concurrency, timeouts and retries,
   proxies, cloud networks, containers, Kubernetes, diagnostic method). This course's Module 5
   stays on the **Linux side**: the commands that read the box's network state, network
   namespaces, Docker networks, firewalls and egress enforcement, the reachability probe.
   Summarise a concept in a sentence or two, link to its lesson, and spend the words on what that
   course does not do. Lesson files: `01-request-journey`, `02-addresses-and-ports`,
   `03-ip-and-routing`, `04-dns`, `05-transport`, `06-tls`, `07-http`, `08-streaming`,
   `09-latency-and-throughput`, `10-concurrency-and-limits`, `11-timeouts-and-retries`,
   `12-proxies-and-load-balancers`, `13-cloud-networks`, `14-containers`, `15-kubernetes`,
   `16-inference-and-locality`, `17-diagnostic-method`, `18-observability`, `19-local-lab`,
   `20-incident-practice`, `21-design-an-eval-system`, `22-boundaries-and-validity`,
   `23-readiness-review` (all `.html`). Its claims are not our sources: link, don't cite.
7. **Honest finish line.** No promises of employment; describe observable skills.
