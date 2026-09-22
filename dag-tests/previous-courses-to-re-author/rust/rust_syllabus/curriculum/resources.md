# Month-one resources

This page is a catalog, not a reading list to complete in order. Open only the resource and selection named under the current lesson's **Prescribed reading, in order** heading. Verification dates and other lesson mappings provide context and require no learner action.

Links and page titles were checked on 2026-09-08. This is the selected month-one reading list, not a fresh audit of every resource in the original long-term specification. Each module assigns the selections needed for its concept.

Original resources are retained. Additions are primary documentation needed to make the labs executable, plus prerequisite Rust Book chapters and sources for the required market survey.

The systemd manual text is authored by the systemd project and served here through man7. The freedesktop HTML endpoints were unavailable to the authoring browser; the mirrored manuals and upstream source were checked. Use the installed host's manual for version-specific details. A reachable documentation page does not establish that a hosted lab, SSH exercise, or product deployment is available to your account.

No paid course, purchased book, model API, or GPU is required this month. Linux Journey browser exercises are optional conveniences; local exercises provide the required evidence.

## git

[Git tutorial](https://git-scm.com/docs/gittutorial)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Making changes; viewing history. Local commit workflow only.
- Lessons: M1-01, M1-29.

## journey

[Linux Journey](https://labex.io/linuxjourney)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Command Line, Text-Fu, Processes, Permissions, Network Basics; lesson-specific selections only.
- Lessons: M1-03, M1-04, M1-13, M1-23.

## bandit

[OverTheWire: Bandit](https://overthewire.org/wargames/bandit/)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Initial login and early file-discovery exercises; never commit credentials or solutions.
- Lessons: M1-03.

## book1

[The Rust Book: Getting Started](https://doc.rust-lang.org/book/ch01-00-getting-started.html)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Installation if needed, Hello World, Hello Cargo.
- Lessons: M1-05, M1-29. Opening Rust onboarding moved out of the M1-01 pilot; earlier completed practice is retained.

## book3

[The Rust Book: Common Programming Concepts](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

- Origin: prerequisite addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Variables, types, functions, and control flow; small examples only.
- Lessons: M1-05.

## book4

[The Rust Book: Understanding Ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Ownership, references and borrowing, string slices.
- Lessons: M1-06.

## book6

[The Rust Book: Enums and Pattern Matching](https://doc.rust-lang.org/book/ch06-00-enums.html)

- Origin: prerequisite addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Enum variants, Option, and match.
- Lessons: M1-05, M1-09, M1-10, M1-20.

## book9

[The Rust Book: Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

- Origin: prerequisite addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Recoverable errors with Result and propagation with question-mark.
- Lessons: M1-09, M1-10.

## book10

[The Rust Book: Generic Types, Traits, and Lifetimes](https://doc.rust-lang.org/book/ch10-00-generics.html)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Read the overview; concrete lifetime selection is linked separately.
- Lessons: Optional preview/reference; not required this month.

## lifetimes

[The Rust Book: Validating References with Lifetimes](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Preventing dangling references, annotations in signatures, and elision.
- Lessons: M1-08.

## book11

[The Rust Book: Writing Automated Tests](https://doc.rust-lang.org/book/ch11-00-testing.html)

- Origin: prerequisite addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Assertions, Result in tests, and integration-test organization.
- Lessons: M1-12, M1-20.

## book15

[The Rust Book: Smart Pointers](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Optional preview of Box/Rc/Drop; deeper coverage remains later.
- Lessons: Optional preview/reference; not required this month.

## book16

[The Rust Book: Fearless Concurrency](https://doc.rust-lang.org/book/ch16-00-concurrency.html)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Threads, move closures, joins, channels; selected Send/Sync discussion.
- Lessons: M1-15, M1-16.

## command

[Rust std::process::Command](https://doc.rust-lang.org/std/process/struct.Command.html)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: arg/args, current_dir, env/env_clear, spawn, stdout/stderr.
- Lessons: M1-10, M1-11, M1-13, M1-16, M1-19.

## child

[Rust std::process::Child](https://doc.rust-lang.org/std/process/struct.Child.html)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: wait, try_wait, kill, and lifecycle obligations.
- Lessons: M1-11, M1-16, M1-17.

## commandext

[Rust Unix CommandExt](https://doc.rust-lang.org/std/os/unix/process/trait.CommandExt.html)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: process_group only; do not implement pre_exec hooks.
- Lessons: M1-18.

## procstatus

[proc_pid_status(5)](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Name, State, Pid, PPid, Uid, Gid, NSpid, NoNewPrivs, and Seccomp fields as assigned.
- Lessons: M1-04.

## signal

[signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Signal dispositions and the standard signal table; TERM/KILL first.
- Lessons: M1-04, M1-17.

## kill

[kill(2)](https://man7.org/linux/man-pages/man2/kill.2.html)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Process IDs versus process groups and permission/error semantics.
- Lessons: M1-18.

## namespaces

[namespaces(7)](https://man7.org/linux/man-pages/man7/namespaces.7.html)

- Origin: original primary-source selection.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Namespace overview, types, and handles in /proc.
- Lessons: M1-22.

## unshare

[unshare(1)](https://man7.org/linux/man-pages/man1/unshare.1.html)

- Origin: original primary-source selection.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: PID/mount/user namespace flags; fork and mount-proc.
- Lessons: M1-22.

## netns

[ip-netns(8)](https://man7.org/linux/man-pages/man8/ip-netns.8.html)

- Origin: original primary-source selection.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Named namespace lifecycle, exec, and cleanup.
- Lessons: M1-23.

## netnsconcept

[network_namespaces(7)](https://man7.org/linux/man-pages/man7/network_namespaces.7.html)

- Origin: original primary-source selection.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: What networking state is isolated.
- Lessons: M1-23.

## cgroup

[Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)

- Origin: original primary-source selection.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Basic usage, CPU interface, memory interface, and cgroup.events; do not read the whole document.
- Lessons: M1-24, M1-25.

## systemdrun

[systemd-run(1)](https://man7.org/linux/man-pages/man1/systemd-run.1.html)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Transient services, service type, properties, wait/pipe/collect behavior.
- Lessons: M1-24, M1-26, M1-27, M1-29.

## systemdresources

[systemd.resource-control(5)](https://man7.org/linux/man-pages/man5/systemd.resource-control.5.html)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: CPUQuota, MemoryMax, and TasksMax; compare installed-version documentation.
- Lessons: M1-25.

## systemdexec

[systemd.exec(5)](https://man7.org/linux/man-pages/man5/systemd.exec.5.html)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: User, WorkingDirectory, NoNewPrivileges, NetworkNamespacePath, and RuntimeDirectory.
- Lessons: M1-27.

## systemdkill

[systemd.kill(5)](https://man7.org/linux/man-pages/man5/systemd.kill.5.html)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: KillMode, KillSignal, and the control-group mode.
- Lessons: M1-26.

## seccomp

[Seccomp BPF](https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html)

- Origin: original primary-source selection.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Introductory boundary discussion only this month; filter construction comes later.
- Lessons: M1-22.

## serdejson

[serde_json](https://docs.rs/serde_json/latest/serde_json/)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Typed serialization/deserialization; use the library to encode JSON correctly.
- Lessons: M1-19.

## proptest

[Proptest: Introduction](https://proptest-rs.github.io/proptest/intro.html)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Introduction, basic usage, failure cases and shrinking through the book navigation.
- Lessons: M1-28.

## clippy

[Clippy Lints](https://rust-lang.github.io/rust-clippy/master/index.html)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Look up only warnings encountered; introduce pedantic as warnings, not an unreviewed blanket gate.
- Lessons: M1-12.

## pythonproc

[Python subprocess: Subprocess management](https://docs.python.org/3/library/subprocess.html)

- Origin: addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Popen start_new_session, poll, wait, and finite harness construction in M1-18.
- Lessons: M1-18.

## e2b

[E2B: Open Source](https://e2b.dev/open-source)

- Origin: survey addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Find explicit deployment model statements; record the source date.
- Lessons: M1-02.

## e2bsecurity

[E2B: Security](https://e2b.dev/security)

- Origin: survey addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Distinguish vendor-managed BYOC from self-hosting and documented trust boundaries.
- Lessons: M1-02.

## sprites

[Sprites Overview](https://docs.sprites.dev/)

- Origin: survey addition.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Document the hosted service's stated scope; do not infer customer-hardware support from a VM abstraction.
- Lessons: M1-02.

## firecracker

[Firecracker: getting started](https://github.com/firecracker-microvm/firecracker/blob/main/docs/getting-started.md)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Prerequisites and host/guest model for the survey and month-two preparation; no boot exercise this month.
- Lessons: M1-02, M1-30.

## jailer

[Firecracker: jailer](https://github.com/firecracker-microvm/firecracker/blob/main/docs/jailer.md)

- Origin: original.
- Verified: 2026-09-08; page content/title retrieved.
- Selection: Jailer responsibilities, namespace placement, and privilege reduction for month-two planning.
- Lessons: M1-30.

## Verification and substitution rules

Recheck a changing resource at lesson time if its location or content differs. Record the actual title, URL, date, selected section, and any substitution in the session note. Do not label a resource dead based solely on an access error.

For primary manuals, a supported local man page is an acceptable version-matched source. For a temporarily unreachable reading, retain its role and use a verified official mirror or locally installed copy. Do not replace the prescribed conceptual objective with a preferred unrelated course.

The survey links are starting points, not prefilled conclusions. The learner records current evidence and distinguishes explicit claims from inference and unknowns.
