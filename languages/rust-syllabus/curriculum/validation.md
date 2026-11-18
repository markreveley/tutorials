# Authoring verification

Checked on 2026-09-08.

- Thirty lesson documents contain the prescribed objective, today's ordered action path, starting state, reading selection, exercise, artifacts, exit criteria, independent check, recovery, and optional extension.
- The original authoring pass checked study-time estimates. Those estimates and their validation rules have since been removed at the learner’s request.
- The prerequisite graph contains no unknown, forward, or cyclic dependencies.
- Local Markdown links and resource references pass the repository checker.
- All assigned external source URLs and titles were retrieved during authoring; resources.md records provenance and access caveats. Hosted exercises and product features were not independently operated.
- Python source parses successfully.
- Portable fixture checks covered successful/nonzero exits, separate stream contents, bounded high output, synthetic environment output, finite sleep/tree/CPU/memory modes, and rejection of out-of-range workload parameters.
- The progress helper was tested in a temporary copy: unmet prerequisites are rejected, starting a lesson awards no mastery, repeated starts resume without overwriting, unsupported completion is rejected, and recovery attempts preserve earlier records.
- The bootstrap progress record began with 30 not-started lessons and zero assessed capabilities. For current learner state, run `python3 scripts/curriculum.py status`; this authoring note is not a live status display.

The authoring machine is macOS on arm64. No Linux namespace, cgroup, systemd, Firecracker, or learner-capstone result is claimed by these checks. Those results must be observed on the designated lab as the learner completes the lessons.

The scripts check structural consistency and artifact existence. They cannot establish that a learner's explanation was independent or correct; that requires the recorded assessment and review of its evidence.

## Instruction-flow verification — 2026-09-09

The [instruction-flow audit](instruction-flow-audit.md) records the scope and findings. `python3 scripts/curriculum.py check` passed after the changes, and `status` displayed the three M1-01 questions along with conditional resume guidance. `git diff --check` passed.

`python3 -m unittest discover -s scripts -p 'test_*.py'` passed three tests: prompt/objective delivery for all 30 lessons in temporary copies, preservation of an existing learner response on resume, and rejection of an empty prompt before attempt creation. The first test run failed because the temporary test root used a macOS symlink path while the path guard resolves paths. Resolving the test root fixed the test setup; the repository path guard was preserved.

These are authoring checks. No learner exercise or Linux experiment was run, and no learner progress or capability was awarded.

## Lesson and worksheet separation — 2026-09-09

Later learner feedback superseded the prompt-copying approach above. Instructions now appear only in the lesson, ordered for reading from top to bottom. The attempt contains answer/result fields and links to the lesson; status directs the learner there.

The curriculum checker and diff whitespace check passed. The three updated regression tests passed, covering links to each of the 30 lesson prompts without copied tutorial text, preservation on resume, and rejection of empty prompts. M1-01's existing learner answers were preserved. No lesson exercise or independent assessment was performed.

## Concept-based modules — 2026-09-09

At the learner’s request, study-time estimates, total-hour targets, and mandatory elapsed-time tracking were removed. Manifest version 2 replaces budget fields with each module’s concept focus. The checker validates that focus against the lesson, alongside the existing dependency and evidence rules. Optional historical elapsed-time observations remain readable.

The curriculum check and diff whitespace check passed. All four regression tests passed, including completion with evidence and an independent pass but no time fields, and rejection of completion without evidence or an independent pass. Finite fixture durations and process/resource limits remain experiment controls. No Linux experiment or independent learner assessment was run.

## Self-contained setup revision — 2026-09-09

The [setup and lesson audit reference](setup-and-lesson-audit.md) records the learner feedback, changes, audit standard, and remaining scope. M1-01 now saves its Mac inventory and supplies guided fixture commands. M1-04 explicitly enters the Ubuntu setup path and retains a separate Linux inventory; its manifest artifact list matches the lesson.

Actual authoring checks:

- `python3 scripts/curriculum.py check` passed for all 30 modules, including dependencies, local links, and progress structure.
- `python3 -m unittest discover -s scripts -p 'test_*.py'` passed all four existing regression tests.
- `git diff --check` passed.
- The local Git bundle procedure was exercised in two temporary repositories on the Mac using synthetic empty commits: initial `HEAD` export/import into `lab-work`, Linux-role commit transfer back to the Mac-role branch, and a subsequent Mac-role commit transfer back to `lab-work`. Both round-trip head comparisons and fast-forward merges passed. These repository names indicate workflow roles only; no Linux machine participated. Temporary repositories remain at `/tmp/syllabus-bundle-check.9PNmTZ` and contain no learner evidence or repository history.
- Inspected `scripts/preflight.py` and `labs/fixtures/workload.py` to match the documented inventory fields, stream text, and status behavior. Inspected the learner's existing Rust practice file paths without treating their presence as proof of execution or mastery.
- Consulted official Multipass installation, launch and transfer references, the Rust Book installation chapter, Python's macOS download page, Docker's VM documentation, and Sprites' services documentation. The setup guide links the relevant sources.

Not executed: Mac installers, Multipass launch/shell/transfer, Ubuntu package installation, Rust installation, Linux inventory, or privileged namespace/systemd/cgroup experiments. The bundle test verifies Git mechanics, not VM transport or Linux compatibility. Expected output in the guide remains an expectation to check on the learner's environment. No learner lesson or independent assessment was completed by this authoring work.

## Lesson 1 relevance and dedicated preflight — 2026-09-10

The [current-step relevance revision](setup-and-lesson-audit.md#current-step-relevance-revision--2026-09-10) records the learner's rules and how lesson 1 was revised. Rules live in root `AGENTS.md`; the preflight instructions now live directly in lesson 1, with a dedicated version-report command. The three prediction questions, assigned reading selections, lesson order, and independent-check requirements remain intact. The future Linux-plan task and completion criterion were removed at the learner's request.

Actual authoring verification:

- `python3 scripts/curriculum.py check` passed for all 30 modules.
- `python3 -m unittest discover -s scripts -p 'test_*.py'` passed all four existing regression tests.
- `git diff --check` passed.
- `python3 scripts/m1_01_preflight.py` ran successfully on the Mac and printed JSON containing only `os`, `architecture`, `python`, `git`, `rust`, and `cargo`. No output was written to learner evidence files. Linux capability flags and future-setup notes are absent from this command.
- SHA-256 checks before and after editing confirmed that `sessions/M1-01/attempt-01.md`, `labs/m1-01/preflight.json`, and the empty `labs/m1-01/baseline.md` were unchanged. The attempt was explicitly excluded at the learner's request; authoring handover is in the audit reference.

No installer, VM operation, learner fixture run, or independent assessment was performed. This pass revised lesson 1; the remaining lessons' dedicated preflights and full relevance audits are still outstanding.

## Remaining lessons and role clarity — 2026-09-10

This pass revises M1-02–M1-30 and clarifies the guiding-agent role in M1-01 and the entry/policy documents. The [audit record](setup-and-lesson-audit.md#full-remaining-lesson-audit--2026-09-10) gives per-lesson findings and the reasons for each correction.

Actual authoring checks:

- `python3 scripts/curriculum.py check` passed for all 30 modules, local links/anchors, dependencies and progress structure.
- `python3 -m unittest discover -s scripts -p 'test_*.py'` passed nine tests: the four existing start/resume/completion tests plus dedicated-preflight routing, manifest/commit artifact alignment, shell-block syntax, and two mocked M1-04 inventory cases. The shell test invokes `bash -n` only; it does not execute the printed commands. Mocked Linux fields are test inputs, not Linux observations.
- `python3 scripts/m1_04_preflight.py` ran on the Mac and honestly reported Darwin, no Linux distribution/ps version, and unreadable /proc. It printed to the terminal only; no learner inventory was overwritten. The report omits Rust, namespaces, systemd, cgroups and KVM because M1-04 does not need them.
- `git diff --check` passed. The protected attempt and baseline have no diff; the learner's separate inventory edit remains outside the authoring changes.
- Inspected the supplied finite fixture interface and existing resource selections. Rechecked [Multipass installation](https://canonical.com/multipass/docs/latest/how-to-guides/install-multipass/), [Cargo initialization](https://doc.rust-lang.org/cargo/commands/cargo-init.html), [Bandit login](https://overthewire.org/wargames/bandit/bandit0.html), [unshare](https://man7.org/linux/man-pages/man1/unshare.1.html), [ip-netns](https://man7.org/linux/man-pages/man8/ip-netns.8.html), [systemd-run](https://man7.org/linux/man-pages/man1/systemd-run.1.html), [execution properties](https://man7.org/linux/man-pages/man5/systemd.exec.5.html), [resource controls](https://man7.org/linux/man-pages/man5/systemd.resource-control.5.html), [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), and [Proptest](https://docs.rs/proptest/latest/proptest/). The obsolete non-latest Multipass URL returned 404; the current linked installation page was retrieved. The freedesktop systemd HTML endpoint returned 403, so the project-authored manual mirror was used. A Rust Command page fetch failed; its existing resource link is retained, not claimed freshly verified.

Not executed: software installers, VM creation/transfer, Bandit login, future Rust exercises/tests, namespaces, local HTTP experiment, cgroups, services or clean-checkout demo. Installed Ubuntu-version option support, permission behavior, service/counter lifetimes and the full end-to-end learner path must still be observed during those lessons. Existing Git-bundle mechanics were tested in the earlier pass above; this pass does not claim a new transport run. No learner completion, independent pass, or mastery was inferred.

## Agent-led pilot verification — 2026-09-10

Scope: M1-01's purpose and conversational sequence, saved-step display/validation in the existing helper, a protected-record continuation, entry/agent policy, and moving opening Rust onboarding to M1-05 without losing its setup instructions. Other lessons have not been converted to agent-led delivery.

Verification commands for this pass:

- `python3 scripts/curriculum.py check`: all 30 lesson structures, concept mappings, dependencies, local links and progress validate.
- `python3 scripts/curriculum.py status`: reports agent-led M1-01, the active attempt-02 record and “Explain the observed result,” not a direction to restart the prediction or maintain multiple worksheets.
- `python3 -m unittest discover -s scripts -p 'test_*.py'`: fourteen tests cover existing start/completion rules, dedicated preflights and shell syntax, plus agent-led start state, exact-step resume without mutation, missing-heading/invalid-step rejection, the narrowed M1-01/Rust-onboarding placement, and removal of Rust checks from the optional legacy M1-01 report.
- `git diff --check` and protected-file SHA-256 comparisons: whitespace and preservation checks.

The initial structural check found the new continuation's link to this pass's not-yet-written audit section. Adding the planned audit/verification records resolved that authoring-order failure; no learner output was changed to make validation pass.

No new learner fixture, Rust program, installer, VM or Linux experiment is run for this pilot preparation. Existing command results are learner-reported evidence, not author-observed executions. No independent check, mastery or lesson completion is awarded. The conversational teaching experience still needs learner feedback; passing authoring checks cannot validate its effectiveness.
