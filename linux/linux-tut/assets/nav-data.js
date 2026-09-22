// Site map: drives sidebar nav, search, and prev/next links.
// Paths are relative to the site root.
window.SITE = { title: "Linux for Evals Engineers", sub: "a course in environments" };

window.NAV = [
  {
    module: "Start",
    pages: [
      { n: "", path: "index.html", title: "Course Home",
        kw: "home overview syllabus modules how to use" },
      { n: "0", path: "pages/00-orientation.html", title: "Orientation: Why Linux, for Evals",
        kw: "why linux agentic benchmarks sandbox environment instrument ten minute test introduction" },
      { n: "1", path: "pages/01-lab-setup.html", title: "Lab Setup: A Linux Box You Can Break",
        kw: "docker container vm mac macos ubuntu debian install practice disposable ssh" },
    ],
  },
  {
    module: "Module 1 · The Shell",
    pages: [
      { n: "2", path: "pages/02-shell-and-commands.html", title: "The Shell and the Command Line",
        kw: "bash prompt command argument option flag path which type builtin exit status" },
      { n: "3", path: "pages/03-files-and-the-tree.html", title: "Files and the Filesystem Tree",
        kw: "fhs directories ls cp mv rm find inode hard link symlink etc var tmp home absolute relative path" },
      { n: "4", path: "pages/04-streams-pipes-redirection.html", title: "Streams, Pipes, and Redirection",
        kw: "stdin stdout stderr file descriptor pipe redirect 2>&1 tee here document dev null" },
      { n: "5", path: "pages/05-text-fu.html", title: "Text-Fu: Reading Logs at Scale",
        kw: "grep sed awk sort uniq cut wc head tail jq jsonl xargs regex log analysis" },
      { n: "6", path: "pages/06-shell-scripting.html", title: "Shell Scripts Under Thirty Lines",
        kw: "bash script shebang set -euo pipefail quoting variables loops conditionals shellcheck python" },
    ],
  },
  {
    module: "Module 2 · Identity & Permissions",
    pages: [
      { n: "7", path: "pages/07-users-groups-root.html", title: "Users, Groups, and Root",
        kw: "uid gid passwd shadow id whoami sudo su root non-root useradd service account" },
      { n: "8", path: "pages/08-permissions.html", title: "Permissions and Ownership",
        kw: "rwx chmod chown octal umask setuid setgid sticky bit directory execute answer key" },
    ],
  },
  {
    module: "Module 3 · Processes",
    pages: [
      { n: "9", path: "pages/09-processes.html", title: "Processes: What Is Running",
        kw: "pid ppid ps top htop fork exec proc pstree daemon zombie orphan background" },
      { n: "10", path: "pages/10-signals-exit-codes.html", title: "Signals, Exit Codes, and Timeouts",
        kw: "sigterm sigkill sigint kill timeout 124 137 143 126 127 pid 1 init trap grace period" },
      { n: "11", path: "pages/11-environment-and-secrets.html", title: "Environment Variables and Secrets",
        kw: "env export printenv api key secret proc environ inheritance leak docker inspect" },
      { n: "12", path: "pages/12-resources-and-limits.html", title: "Resources, Limits, and the OOM Killer",
        kw: "cpu memory free df du load average ulimit rlimit oom killed 137 nproc disk full" },
      { n: "13", path: "pages/13-services-and-logs.html", title: "Services, Init, and Logs",
        kw: "systemd systemctl journalctl unit service var log syslog dmesg boot daemon" },
    ],
  },
  {
    module: "Module 4 · Storage & Software",
    pages: [
      { n: "14", path: "pages/14-mounts-and-filesystems.html", title: "Mounts and Filesystems",
        kw: "mount findmnt df read-only ro bind mount tmpfs overlayfs proc sys block device lsblk" },
      { n: "15", path: "pages/15-packages-reproducibility.html", title: "Packages and Reproducible Environments",
        kw: "apt dpkg apt-get install pin version snapshot pip lockfile hashes base image digest drift alpine apk" },
    ],
  },
  {
    module: "Module 5 · Networking for Sandboxes",
    pages: [
      { n: "16", path: "pages/16-addresses-and-routes.html", title: "Addresses, Interfaces, and Routes",
        kw: "ip address cidr subnet private range rfc1918 ip addr ip route gateway nat loopback interface" },
      { n: "17", path: "pages/17-ports-and-sockets.html", title: "Ports, Sockets, TCP and UDP",
        kw: "port socket tcp udp ss listening 0.0.0.0 127.0.0.1 localhost bind nc connection refused timeout" },
      { n: "18", path: "pages/18-dns-http-tls.html", title: "DNS, HTTP, and TLS",
        kw: "dns dig resolv.conf hosts curl -v http status tls certificate ca proxy https" },
      { n: "19", path: "pages/19-firewalls-and-egress.html", title: "Firewalls and Egress Control",
        kw: "firewall nftables iptables default deny egress allowlist proxy network none metadata reachability test" },
    ],
  },
  {
    module: "Module 6 · Containers & Isolation",
    pages: [
      { n: "20", path: "pages/20-namespaces.html", title: "Namespaces: What a Container Really Is",
        kw: "namespace pid mount net user uts ipc unshare nsenter lsns chroot pivot_root container shared kernel" },
      { n: "21", path: "pages/21-cgroups-capabilities-seccomp.html", title: "Cgroups, Capabilities, and Seccomp",
        kw: "cgroup v2 memory.max cpu.max pids.max capabilities cap_sys_admin seccomp no_new_privs apparmor" },
      { n: "22", path: "pages/22-docker-for-evals.html", title: "Docker for Eval Environments",
        kw: "docker image layer dockerfile run exec volume bind mount read-only network none memory cpus compose" },
      { n: "23", path: "pages/23-hardening-containers.html", title: "Locking Down a Container",
        kw: "non-root user cap-drop read-only no-new-privileges pids-limit docker socket privileged hardening checklist" },
      { n: "24", path: "pages/24-isolation-ladder.html", title: "The Isolation Ladder: Containers, gVisor, MicroVMs",
        kw: "gvisor firecracker microvm kvm hypervisor kata shared kernel isolation egress tenancy secrets snapshot threat model" },
    ],
  },
  {
    module: "Module 7 · Linux in Eval Harnesses",
    pages: [
      { n: "25", path: "pages/25-how-harnesses-use-linux.html", title: "How Harnesses Drive a Sandbox",
        kw: "inspect sandbox exec bash tool terminal-bench tmux swe-bench docker images compose harness timeout user" },
      { n: "26", path: "pages/26-environment-integrity.html", title: "Environment Integrity: Where Cheating Lives",
        kw: "reward hacking git history leak answer key test tampering held-out tests network egress cheat rate" },
      { n: "27", path: "pages/27-reading-terminal-transcripts.html", title: "Reading Terminal Transcripts",
        kw: "error analysis trajectory command not found permission denied hang interactive prompt pager apt lock infrastructure failure" },
      { n: "28", path: "pages/28-ten-minute-audit.html", title: "Capstone: The Ten-Minute Audit",
        kw: "audit checklist what is running mounted owns reach logs fresh vm root capstone" },
    ],
  },
  {
    module: "Appendices",
    pages: [
      { n: "A", path: "appendices/a-command-reference.html", title: "The Working Set of Commands",
        kw: "cheat sheet command reference quick lookup" },
      { n: "B", path: "appendices/b-exit-codes-signals.html", title: "Exit Codes and Signals",
        kw: "exit status table 0 1 2 124 125 126 127 128 130 137 139 143 signal numbers" },
      { n: "C", path: "appendices/c-binary-octal-cidr.html", title: "Binary, Octal, and CIDR Math",
        kw: "binary octal bits chmod 755 umask 022 subnet mask prefix length host count" },
      { n: "D", path: "appendices/d-regex.html", title: "Regular Expressions",
        kw: "regex pattern anchors character class quantifier grep -E basic extended" },
      { n: "E", path: "appendices/e-macos-vs-linux.html", title: "macOS vs Linux",
        kw: "bsd gnu sed -i date stat readlink brew zsh bash differences darwin" },
      { n: "F", path: "appendices/f-getting-help.html", title: "Man Pages and Getting Help",
        kw: "man --help info apropos tldr sections synopsis reading documentation" },
      { n: "G", path: "appendices/g-skills-checklist.html", title: "Skills Checklist and Portfolio Labs",
        kw: "self assessment interview deep enough job employable portfolio projects" },
    ],
  },
  {
    module: "Reference",
    pages: [
      { n: "", path: "glossary.html", title: "Glossary",
        kw: "terms definitions vocabulary" },
      { n: "", path: "bibliography.html", title: "Annotated Bibliography",
        kw: "sources citations man pages papers documentation references" },
    ],
  },
];
