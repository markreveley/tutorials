# Curriculum contract

## Direction

Learn to explain and enforce the boundaries around autonomous execution: what runs, who owns its resources, how failure is represented, which authority it receives, and which evidence supports the result. Build one evolving system, supported by small experiments that isolate individual concepts.

## Concepts and order

- Each module names a central concept, its prerequisites, a focused exercise, and evidence that demonstrates understanding. Reading and setup serve that concept.
- Integration checkpoints combine previously studied concepts; they do not introduce an unrelated topic.
- Study duration is up to the learner. A module may span multiple sessions or attempts. Resume from the recorded stopping point.
- Completion requires the stated evidence and an independently passed check. Time spent is not a completion requirement.
- Checkpoints are M1-07, M1-14, M1-21, and M1-30. M1-29 covers reproduction from a clean checkout.
- Optional extensions remain optional and introduce no hidden prerequisites.
- When setup or debugging prevents progress, preserve a reproduction and use the module's recovery instructions.
- A learner may test out of familiar material by producing the same independent evidence. An agent may not skip a module solely because the learner or agent has read its resource.

The directory name `month-01` identifies the first curriculum stage; it does not impose a calendar deadline.

## Lesson types

Standalone labs include their own starting material but may have conceptual prerequisites. Sequential lessons modify a previous capstone milestone. Checkpoints assess unfamiliar variants and consolidate work. Each type ends with a reviewable commit, including incomplete experiments when necessary.

## Agent-led Lesson 1 pilot

By learner instruction, M1-01 now focuses on interpreting command outcomes. Setup is inline and minimal; Rust onboarding moves to M1-05, Git is assisted session saving, and the broad baseline survey is no longer a required artifact. Earlier work remains preserved. The independent check tests the command-result concept, not Rust practice or Git terminology.

The agent presents one step at a time from the authored sequence, records actual responses and help, and saves a resume step. The learner is not required to maintain multiple reports or worksheets. The active session record and its evidence satisfy the recording requirements below; no duplicate narrative or word target is imposed on this pilot. Lesson order and independent-assessment standards otherwise remain unchanged.

## Evidence

Each session records the objective, prediction, selected reading, commands or procedure, actual observations, artifact paths, help received, independent check, and unresolved questions. Keep explanations concise: approximately 150–300 words is sufficient for an ordinary session.

A completed lesson has:

1. The required artifact and its reproduction instructions.
2. Observed evidence for every exit criterion, including relevant negative cases.
3. A learner-authored explanation or independent modification.
4. An assessment result of passed, with the assessor's reason.
5. Updated progress and a local commit when Git identity is available.

Machine validation checks structure and references, not truth. Supervising agents must inspect evidence. Assisted implementation is permitted; assisted assessment is marked assisted and revisited with a fresh variant. Never conflate exposure, successful implementation, and independent understanding.

## Resource policy

The original resource choices remain the reference library. Month one assigns exact selections rather than whole-book completion. Additional sources are primary manuals needed for the prescribed exercises and are identified in resources.md.

Read the assigned selections needed for the module’s concept. Optional work should deepen that concept. Linux Journey and Bandit continue later; finishing either site is not a month-one prerequisite.

Reading a source does not require executing every example it contains. The lesson must explicitly identify any follow-along practice, where to run it, and whether its files are required evidence. Following a worked example, with or without agent help, is separate from the independent check.

## Product and security boundaries

- One local, finite workload at a time; no real model calls or customer data.
- The Rust runner executes fixed fixture requests directly, without an implicit shell.
- An operator-controlled lab script configures namespaces and transient systemd services. The Rust runner itself does not gain sudo or an unrestricted privileged API.
- The design demonstrates selected behavior on a documented Linux host. It does not establish production isolation, complete mediation, resistance to hostile host administrators, or a tamper-proof audit trail.
- CPU resource quotas, memory ceilings, identity, networking restrictions, and syscall restrictions are distinct mechanisms. Name which one a test exercises.
- Namespaces and cgroups use the host kernel. BEAM process supervision and workload identity will not be presented as substitutes for a security boundary.
- Store only synthetic data in committed evidence. Keep raw captures in ignored scratch/ or artifacts/raw/ until reviewed.

## Standing rules

1. One prescribed lesson at a time. Previously learned concepts may be used together.
2. Depth follows the product's critical path and the prerequisite evidence.
3. Every session produces a reproducible artifact, a useful experiment, or an explicit incomplete-work record.
4. Maintain a public-compatible portfolio; use sanitized examples when partnership work is private. Publication is a separate action.
5. No certification preparation unless a target role specifically requires it.
6. Perform the M1-02 market and threat-boundary survey before deeper virtualization investment.
7. Reassess on evidence at checkpoints; retain the original plan and explain any revision.
