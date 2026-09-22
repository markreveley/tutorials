# M1-01 — Establish the lab and an honest baseline — attempt 01

- Date: 2026-09-08
- Lesson: [Open lesson](../../curriculum/month-01/lessons/01.md)
- Environment: pending
- Implementation assistance: not_recorded
- Independent check: not_attempted
- Lesson status: in_progress

**Instructions:** [Resume lesson at Exercise step 1](../../curriculum/month-01/lessons/01.md#exercise)

## Prediction before reading or implementation

[Question](../../curriculum/month-01/lessons/01.md#predict-before-reading)

**Your response:**

1 - success or fail, and then a separate channel for an error log that is sometimes used for other information
2 - my guess is yes, but total guess that it would be inherited
3 - i am extremely new to rust, but my assumption would be that be would assume ownership of the String object and a would no longer be usable


## What you read or consulted

I read through the git reference including the noted chapters
i worked through the rust book through hello_world and hello_cargo, running everything

## Work and observations

i ran all commands listed in the rust tutorial
i ran:
python3 labs/fixtures/workload.py exit --code 0
echo $?
0
python3 labs/fixtures/workload.py exit --code 7
echo $?
7

## Evidence

## Learner explanation

I don't know what the codes 0 and 7 indicate, but i know that they were assigned to be returned (I assume on success) when 'exit --code x' was run each time workload.py was called

## Independent check

- Variant assigned:
- Learner answer or modification:
- Hints or assistance during the check:
- Observed result:
- Assessor result and concrete rationale:

## Exit criteria

## Cleanup and commit

- Resources created: No lab, process, namespace, service, or remote resources.
- Resources removed or still running: None.
- Staged files reviewed: The curriculum authoring change was reviewed and committed separately; this session record and its progress entry contain no lesson output, raw capture, or credentials.
- Intended commit message: `M1-01: record navigation pause (incomplete)`.
- Commit result, or reason files remain uncommitted: This record and the in-progress entry form an incomplete-work continuity checkpoint; Git history supplies the commit identifier.

## Handover

- Next lesson or recovery attempt: Continue M1-01 attempt 01 at [Exercise step 1](../../curriculum/month-01/lessons/01.md#exercise), following the revised Mac preflight instructions. The learner reports completing the Git reading and working through Hello, World!/Hello, Cargo! above; do not send them back to the start of that reading.
- Exact remaining gap: Mac inventory, exit fixture observations, baseline, independent check, evidence review, progress close, and lesson commit. Learner-reported Rust practice is separate from the independent Python fixture check; no independent assessment has occurred.
- Evidence to inspect next: The prediction in this record; then `labs/m1-01/preflight.json` and `labs/m1-01/baseline.md` after they are created.
- Changes to the plan, with reason: The learner paused before instruction to request clearer navigation. Curriculum usability was corrected first; lesson order and completion state did not change.
- Current repository state: Concept-based module changes are in `10e4cc3`. The current authoring changes and the existing opening-reading/practice clarifications in touched files are grouped for the requested local setup/audit commit; Git history supplies its identifier. Pre-existing changes in the contract and other lesson files, plus untracked `.nvimlog` and `main`, are excluded. M1-01 remains incomplete; no required M1-01 lab artifacts exist.
- Assistance and cleanup for this audit: Agent implemented the authoring changes; lesson implementation assistance remains not_recorded and the independent check remains not_attempted. No lab resources were created; no lab cleanup is required. The older commit notes above describe the earlier navigation pause.

<details>
<summary>Supervisor notes: curriculum revisions</summary>

- Before making the opening prediction or running the lesson exercise, the learner identified that cross-document references did not say which sections required action or where the learner was in the workflow.
- The curriculum navigation and lesson action labels were revised in a separate authoring change. No M1-01 reading, preflight, fixture run, or concept explanation was completed by this documentation work.
- On 2026-09-09, the learner reported that both status and this record requested a prediction without the question. The agent audited the 30 lesson entry paths and corrected prompt delivery, resume guidance, and missing-case handoffs. See [instruction-flow audit](../../curriculum/instruction-flow-audit.md). This was agent-implemented curriculum maintenance; no learner response, reading, exercise, or assessment was supplied or observed.
- Authoring validation: curriculum check, status inspection, three regression tests covering all 30 lesson starts plus resume/empty-prompt behavior, and diff whitespace checks passed. The initial regression run failed on a temporary-path alias in test setup; that setup was corrected. Details are in [authoring verification](../../curriculum/validation.md#instruction-flow-verification--2026-09-09). These checks are not lesson evidence.
- Follow-up wording feedback: The learner requested removal of redundant permission to read questions and a concrete explanation of what to record after reading. The agent revised those instructions and nearby worksheet prompts. The learner’s three prediction answers were present before these edits and were preserved exactly. No reading time, experiment result, or assessment was inferred from them.

- The learner reported that the attempt file duplicated the lesson’s instructions. The agent removed tutorial text from the attempt template and current record, made the lesson the sole instruction sequence, clarified that the two files stay open side by side in the editor, and retained the learner’s answers exactly. Reading, experiments, and assessment remain unrecorded. Curriculum validation, the three updated regression tests, and diff whitespace checks passed.

- At the learner’s request, the agent removed study-time estimates and mandatory elapsed-time tracking, named the central concept of every module, and updated the manifest, checker, template, and supervision rules. Module order and evidence requirements remain in place. The four regression tests and curriculum check passed; this authoring work did not assess the learner or create lab resources. Next: M1-01 prescribed reading.

- Corrected the reading-log instruction to ask for assigned sections finished reading, with a stopping point for partial reading. This is an agent-authored wording correction; no completed reading or assessment was reported.

- The learner asked where the Rust Book file/code examples belong and whether they are assessed. The agent specified optional practice on the Mac in ignored `scratch/m1-01/rust-book/`, separate from the independent Python fixture check. The lesson now includes Hello, World! explicitly to match the catalog and support Hello, Cargo! No practice files were created or run by the agent, and no learner reading or execution result was inferred. Next: continue the assigned Rust reading, with the optional practice described in the lesson.

</details>

## Setup revision handover — 2026-09-09

- Learner request: discuss inline setup comments first, then implement the agreed changes and commit a reusable explanation/instruction reference for auditing other lessons.
- Authoring assistance: agent implemented the setup guide, M1-01 instructions, M1-04 setup entry/artifact requirement, and [audit reference](../../curriculum/setup-and-lesson-audit.md). No learner explanation or independent answer was generated. Lesson assistance remains not_recorded and the independent check remains not_attempted.
- Evidence inspected: learner reading/practice statements above; Rust example source/project files exist under ignored `scratch/m1-01/rust-book/`. Their presence is not independent evidence of execution or mastery. Required `labs/m1-01/` inventory and baseline are absent.
- Resume: M1-01 Exercise step 1 on the Mac. Linux setup is explicitly scheduled before M1-04's exercise. Future authoring audits should begin with the priority sections in the audit reference; they have not been completed by this revision.
- Environment and cleanup: no VM, installer, privileged Linux operation, or learner exercise was run by the agent. Authoring verification is recorded in [validation](../../curriculum/validation.md). No learner lab resource needs cleanup.
