# Trustworthy Agent Infrastructure

A prescribed, evidence-producing learning path for a technical generalist who uses agents to write Rust and wants to understand, review, and supervise autonomous execution.

Start with **Start or resume a session** below. There are 30 ordered modules, each focused on a concept or an integration checkpoint. Work at your own pace and move on when the module’s evidence and independent check are complete. The existing lesson numbers identify modules, not calendar dates.

Month one's capstone is a small Linux task runner: explicit execution requests, understandable Rust ownership and errors, bounded output capture, deadlines, structured run records, and experiments with namespaces and cgroups. Operator-controlled Linux lab scripts provide the privileged setup. The final demonstration states exactly which boundaries have been tested.

The curriculum and fixtures are supplied. The learner implementation and learning evidence are intentionally unfilled. A curriculum commit is not evidence that a lesson has been completed.

## Start or resume a session

The **guiding agent** is the agent helping you in your conversation. The repository's policy documents also call that role the “supervisor.” It guides exercises, assigns independent checks, and maintains progress from your actual work; you do not need another person or separate program.

For the Lesson 1 pilot, continue here in the conversation: say “start Lesson 1” or “resume Lesson 1.” The agent explains the purpose, presents one step at a time, and saves your answers and stopping point. You use Terminal when a step calls for it; you do not manage a lesson document, lab report and attempt worksheet in parallel.

The agent reads the authored lesson and checks progress before teaching. The files remain available for inspection, but are not a second stream of learner tasks. This pilot applies only to Lesson 1; later lessons retain their documented delivery until the pilot has been reviewed.

For a read-only status display, from this repository:

    python3 scripts/curriculum.py status

For the agent: run `python3 scripts/curriculum.py check`; start an unstarted lesson with `python3 scripts/curriculum.py start M1-NN`. An agent-led lesson displays its saved conversational step. Other lessons display their lesson/attempt paths; follow their documented sequence. Starting an attempt never completes a lesson.

The [learner workflow](curriculum/learner-workflow.md) is an optional reference, not another setup assignment.

Git commits are local evidence checkpoints. Commit the implementation and session record together with a message such as:

    M1-06: demonstrate ownership transfer and shared borrowing

For incomplete work, say so in the message and record. A supervising agent must not push to a remote, publish a repository, rent infrastructure, or buy resources merely because the curriculum describes those possibilities.

## Where things live

This table is a directory, not a reading sequence. Open an item when the learner workflow or current lesson names its purpose.

| Location | Purpose |
|---|---|
| [Learner workflow](curriculum/learner-workflow.md) | Reference for file roles and resuming work |
| [Month-one index](curriculum/month-01/README.md) | All 30 lessons, dependencies, outcomes, and milestones |
| [Curriculum contract](curriculum/contract.md) | Supervisor/policy reference for module scope and evidence standards |
| [Lab setup](curriculum/lab-setup.md) | Agent/author environment policy; each lesson supplies its own preflight |
| [Resources](curriculum/resources.md) | Catalog used only for selections named under the current lesson's prescribed reading |
| [Supervision protocol](curriculum/supervision.md) | Supervisor reference; no standalone learner action |
| [Manifest](curriculum/manifest.json) | Machine-readable lesson sequence and prerequisites |
| [Progress](curriculum/progress.json) | Actual status; initially nothing is assessed |
| [Session template](templates/session.md) | Prediction, experiment, assistance, assessment, evidence |
| [Fixtures](labs/fixtures/README.md) | Small, finite workloads for the exercises |
| [Capstone contract](capstone/README.md) | What the learner builds and what remains out of scope |
| [Open questions](curriculum/open-questions.md) | Unresolved deployment and product decisions |
| [Authoring verification](curriculum/validation.md) | What was checked and what still requires the Linux lab |
| [Setup and lesson audit reference](curriculum/setup-and-lesson-audit.md) | Supervisor/author standard, rationale for setup revisions, and completed lesson-audit coverage |

## Scope beyond this month

The broader specialty remains substrate → workload identity → supervision → action gating → evidence → inference when needed. The reference library from the original specification is preserved in [the continuing roadmap](curriculum/roadmap.md). Month one draws only the material required by its lessons.

The repository is the authoritative continuity record. Git history shows changes; session records distinguish agent assistance from independent understanding. Neither a passing test nor a polished explanation written by an agent automatically establishes learner competence.
