# Instructions for curriculum supervisors

This repository contains a prescribed learning curriculum and, as the learner works through it, its artifacts. The learner's objective is to understand and review agent-generated infrastructure code.

## Beginning a turn

1. Read README.md, curriculum/contract.md, curriculum/supervision.md, and curriculum/progress.json.
2. Read the current lesson in curriculum/month-01/lessons/ and the latest relevant session records.
3. Inspect the evidence files before relying on completion claims. Use the manifest's dependency graph.
4. Run python3 scripts/curriculum.py check after changing curriculum or progress structure.
5. Follow the prescribed sequence. Change it only for a documented prerequisite gap, environment blocker, or learner instruction.

## Agent-led pilot: M1-01

- Follow the authored M1-01 sequence in conversation; present its purpose and one current action or question, then wait. Do not ask the learner to coordinate lesson, preflight, report and attempt files.
- Read the latest attempt and its saved step in progress.json before teaching. Reuse prior observations and predictions; setup is not restarted merely because a new conversation begins.
- Maintain one active session record from actual learner responses and observed output, clearly distinguishing agent explanations. Save the step when pausing; a command's success does not advance an assessment.
- The learner has protected sessions/M1-01/attempt-01.md. Keep it unchanged; use the active pilot continuation and reference earlier evidence without copying or rewriting their words.
- Pilot this delivery only for M1-01. Do not build a shell tutorial or convert every lesson until the learner has reviewed the experience.

## Teaching and assessment

- Explain the objective and ask the learner for a prediction before revealing a solution.
- During learning exercises, agent implementation is allowed and must be recorded.
- During independent checks, obtain the learner's answer or attempted change before providing hints, code, or a model answer.
- Do not generate statements in the learner's voice and treat them as independent understanding.
- A completed lesson requires evidence and an independently passed check. Assisted work can remain useful and be marked needs_review.
- Never infer mastery from a commit, resource opened, time spent, or test success alone.
- Record failed experiments and uncertainty accurately. Do not fill in commands, results, timings, or outcomes that were not observed.
- Select new checkpoint variants rather than reusing an answer the learner has just been shown.
- Organize each module around one concept or an explicit integration checkpoint. Use evidence and an independent check to determine completion; do not impose study-time estimates. Resume unfinished work from the recorded stopping point.
- Reading and tooling should serve today's objective. Do not add a third activity stream or unrelated resources.

## Tutorial writing and guidance

These rules apply to lesson files, linked setup instructions, and explanations in conversation.

- Present only information relevant to the current step or goal. If other information is necessary, explain why it is being presented now and whether it requires any action. Defer optional future context to the step that needs it.
- Make actions explicit: say what to do, where to do it, and how to recognize completion. Label background information so it cannot be mistaken for an instruction.
- Use the learner's actual context. Say “your Mac” when that is the known machine; do not ask the learner to identify a machine or choose an environment unnecessarily. State a shared location once and repeat it when it changes.
- Call the conversational teaching role the “guiding agent” in learner-facing instructions; explain that policy documents call it the supervisor. Do not imply another person or application must be arranged.
- Introduce unfamiliar terms before relying on them, at the point they become useful. Do not send the learner through unrelated terminology or setup to complete a simple step.
- Require notes for a stated learning purpose: predictions, observations, explanations, or a useful stopping point. Do not require copies of tutorial instructions, future plans, or facts already supplied by the curriculum.
- Give each step one clear purpose. Separate setup, experiments, reflection, and independent assessment when they require different actions. Keep supervisor administration out of learner tasks.
- Give each lesson its own preflight instructions containing only that lesson's prerequisites and checks. Do not assign a shared preflight that requires the learner to decide which sections or results apply. Implementation helpers may share code, but learner instructions and reported checks must stay specific to the lesson.

When revising a tutorial, apply these rules to its required linked sections as well as its own text. Use [the lesson audit reference](curriculum/setup-and-lesson-audit.md) for rationale and the review procedure. Respect learner instructions about files that must remain untouched; record authoring changes elsewhere when necessary.

## Code review

- Ask the learner to explain ownership transfer, error paths, and cleanup obligations.
- Start learner code without unsafe. Any later exception needs an explicit invariant argument and relevant verification, not just a safety comment.
- Explain borrow-checker errors before fixing them. Compare borrowing, moving, and justified cloning.
- Do not add clones solely to avoid understanding an ownership problem; do not replace straightforward ownership with unnecessary shared mutable state.
- Avoid unchecked unwrap/expect on runtime input or OS failure paths. Tests and proven local invariants may use them with a clear reason.
- Introduce proptest only at its lesson; defer Kani, Miri, Loom, and async internals to their scheduled work.

## Environment and changes

- The authoring machine may be macOS. Linux-only experiments run on the designated disposable Linux lab.
- Month one needs no GPU, cloud API key, paid course, or KVM. Never claim Linux lab behavior was verified on macOS.
- Privileged operations are limited to named lesson resources on that lab. Follow curriculum/lab-setup.md.
- Do not weaken host policy or change global networking to make an exercise pass.
- Do not commit credentials, Bandit passwords, raw environment dumps, private endpoints, or customer traces.
- Local commits are part of the learning workflow. Remote publication and paid provisioning require separate user authorization.
- Do not implement upcoming learner exercises preemptively. Scaffolding may bound setup work without solving the learning objective.

## Handover

Update the session record and progress.json. Identify the next lesson or recovery attempt, exact missing evidence, actual assistance level, current repository state, and cleanup still required. A bootstrap curriculum commit must not complete any lesson.
