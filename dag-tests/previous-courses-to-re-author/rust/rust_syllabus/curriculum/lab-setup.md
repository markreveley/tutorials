# Lab environment policy

## How to use this guide

This is an agent/author reference, not a shared learner preflight. Each lesson supplies its own complete setup instructions and relevant checks. Do not assign portions of this guide for the learner to filter.

M1-01 has an inline Mac preflight. M1-02 through M1-30 each link to their own file in month-01/preflight/. The first Linux setup is [M1-04 preflight](month-01/preflight/04.md), which explains the VM, installation, local transfer, process tools, evidence, and shutdown.

## Prescribed baseline

Use the learner's Mac for portable work. Linux-only work uses the local Multipass Ubuntu 24.04 VM named syllabus-m1, ordinary user ubuntu, and repository /home/ubuntu/syllabus. A VM is software running on the existing Mac, not another physical computer the learner must obtain.

Install only the current lesson's tools. M1-04 needs process tools, not Rust, namespaces, or cgroup administration. The Rust checkpoint supplies its Ubuntu installation when needed. Network and service lessons check their own capabilities at their point of use. No GPU, KVM, cloud account, paid provisioning, or customer data is needed this month.

The default gives the service lessons a full Ubuntu system. An alternative requires a documented environment blocker or learner instruction and its own bounded setup; do not silently substitute a container for a service-manager experiment. Platform rationale is not learner homework.

## Install Rust

The lesson that needs Rust supplies its installation steps. Do not send the learner to a general tool inventory or install later tools during the process-lifecycle lesson. Installer review is assisted setup, never independent understanding evidence.

## Create the Linux lab on your Mac

The authoritative learner procedure is [M1-04 preflight](month-01/preflight/04.md). This heading remains so historical references resolve. Do not maintain a competing installation recipe here.

## Resume and preserve Linux work

Each Linux lesson's own preflight includes entry, local Git-bundle transfer, review, fast-forward-only integration, and shutdown. Bundles carry committed history, not uncommitted work. Work in one checkout at a time; preserve both histories on divergence. No remote publication or credential copying is authorized.

## Privileged labs, M1-22 onward

“Operator” means the learner or guiding agent issuing that lesson's named administrative commands with sudo inside syllabus-m1. It is a role in the experiment, not another person or service. Workloads run as ubuntu; the Rust runner never gains sudo or an unrestricted privileged interface.

Allowed resources are the lesson's uniquely named syllabus-m1- namespaces/services, its scratch files, and fixed finite fixtures. System-manager setup uses sudo systemd-run with User=ubuntu. The user service manager is not an interchangeable setup path. Do not alter host-wide security policy, routes, firewall rules, shared cgroups, or arbitrary resources.

Teach only the control used today. A namespace changes a resource view; a cgroup accounts for and limits process resources; a service manager supervises a named job. Do not imply any one of these establishes a complete security boundary.

## Bounded setup skeleton for the learner to complete

This heading is retained for historical links, not assigned setup. M1-24 supplies a concrete finite service observation. M1-25 adds resource limits, M1-26 observes descendant cleanup, and M1-27 composes the already-tested controls. Do not assign an outline in place of those procedures.

For author review: require exact executable paths and fixed arguments, ordinary workload identity, fresh resource names, finite outer bounds, outside observation, and cleanup limited to this run. A wrapper must reject arbitrary commands and must not use a broad kill or namespace deletion.

Retain unit results until inspection, but do not assume that retaining a unit retains its empty cgroup. Capture membership/counters while present. A vanished counter is missing evidence; repeat a bounded case or leave it inconclusive. See the [systemd-run manual](https://man7.org/linux/man-pages/man1/systemd-run.1.html) and [kernel cgroup documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html).

## If the host refuses an operation

Preserve the exact failed command, error with secrets removed, and relevant version. Diagnose the current lesson's failed check. Do not ask for a machine-wide capability dump or make the learner assess unrelated future requirements.

Do not disable AppArmor, change kernel security defaults, weaken permissions, or add unrestricted sudo. M1-22 explicitly describes a narrowly privileged setup that drops workload identity back to ubuntu. Other unsupported required operations remain environment blockers until a permitted equivalent is documented.

An environment blocker is not a failed concept assessment. Select an evidence-ready standalone lesson only via the manifest and record the reason. Never replace Linux evidence with Mac output, simulation, or an agent's explanation.

## Cleanup

Capture evidence first, stop only the exact owned service/processes, confirm descendants are gone, then delete only the exact named namespace. Record any resource still running. Stop the VM after transferring reviewed work; shutdown is not evidence that the cleanup implementation worked.

Preserve learner artifacts and incomplete attempts. Do not delete the VM or temporary reproduction checkout before its work is safely preserved.

## Verification limits of this authored curriculum

The authoring pass checks structure, supplied fixture interfaces, source documentation and helper behavior. It does not execute future learner exercises or certify Linux behavior. Expected output is guidance, not an observed transcript. See [authoring verification](validation.md) and [the lesson audit reference](setup-and-lesson-audit.md).
