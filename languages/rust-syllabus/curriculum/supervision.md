# Supervision and continuity

“Supervisor” means the agent guiding the learner in the current conversation. In learner instructions use **guiding agent**, explain the role at entry, and state separately what the learner does and what the agent records. Do not imply that a second person, account, or service must be arranged.

## Sources of truth

Apply the tutorial writing rules in [AGENTS.md](../AGENTS.md#tutorial-writing-and-guidance) when teaching or revising instructions. Use the [self-contained setup and lesson audit reference](setup-and-lesson-audit.md) for the review procedure. Include only the purpose, location, action, expected result, evidence, recovery, and cleanup relevant to the current task; do not turn the authoring checklist into repetitive learner paperwork. Verify prerequisites against evidence and supplied files. Keep setup guidance distinct from independent assessment; a requirement list or manual link alone is not a runnable tutorial.

The authored lesson files prescribe work. manifest.json indexes them and their dependencies. progress.json records actual lesson and capability status. Session records and artifact history substantiate those claims.

An agent reading this repository must distinguish these layers. The existence of a lesson file describes intended learning. It does not demonstrate that learning happened.

## Delivering the M1-01 pilot

For the agent-led lesson, use this procedure instead of directing the learner to a worksheet:

1. Read the current attempt, saved step and earlier evidence. The step is a navigation marker, not a mastery claim.
2. Briefly explain what is being learned, why it contributes to reviewing the future task runner, and what counts as finished. On resuming, do not repeat a full introduction.
3. Present only the current question or action from the authored sequence. Wait for the learner's reply/output before moving on; answer detours, then return to the saved step.
4. Record the learner's actual response once. Attribute agent explanations and implementation separately. Never fill in missing command output from the fixture's expected behavior.
5. Maintain the active attempt and its step in progress.json. Do not advance merely because a command succeeds. Preserve failed/incomplete checks and all protected files.
6. Run the independent check only after guided work: assign a fresh concrete case, obtain an attempt before hints, and assess the actual explanation and result.
7. Handle evidence indexing, local save/commit and handover as agent administration. The learner reviews actual work; they do not maintain a separate lab report or preflight inventory.

This is a one-lesson pilot, not a shell tutorial implementation or a change to the delivery of every lesson. For the current learner, attempt-02.md continues the protected attempt-01.md; preserve prior work and use the latest record for the resume point.

## Starting a lesson

The following document-led procedure continues to apply to other lessons.

1. Read AGENTS.md, the curriculum contract, progress, and the lesson.
2. Inspect prerequisite session evidence. Checkpoints gate subsequent integration work.
3. Identify the module’s concept and designated lab. Keep the exercise focused on that concept, and let the learner pause and resume as needed.
4. Run the start command to create the attempt worksheet linked to the lesson. If creating it manually from templates/session.md, replace every placeholder. Keep instructional text in the lesson; use the attempt for learner answers, observations, and assessment records.
5. Ask the lesson's prediction question and preserve the learner's actual response before teaching. Direct the learner to the lesson’s actual question before asking for an answer; the attempt links to that section. Do not copy the tutorial into the worksheet. Supply any concrete cases requested by the prompt before asking for a prediction, without hints or solutions. Obtain the prediction before teaching the topic or running the exercise.
6. Guide the prescribed exercise. Implementation can be agent-assisted, but the learner should explain changes before accepting them.

For reading assignments that contain commands or code, specify whether the learner should only read or also run the examples. Any assigned or optional practice must name its machine, working directory, files to retain or commit, and assessment role. Keep these directions in the lesson. A source's example commands do not silently become curriculum requirements.

Do not require the learner to re-confirm already authorized, bounded lab work. New paid resources, remote publication, or host changes outside the lab are separate decisions.

## Independent assessment

Set a fresh variant of the lesson's check. Allow documentation lookup where the lesson permits it, but do not provide the solution, generate the learner's explanation, or repair their attempt before recording the result.

Use these results:

| Result | Meaning |
|---|---|
| not_attempted | No learner answer or independent change was obtained |
| assisted | A hint or implementation help was needed during the check |
| passed | The learner explained or changed the unfamiliar case and reconciled it with observed behavior |
| needs_review | The explanation contradicted evidence or missed the required boundary |

Record the concrete answer or a faithful quotation, observed outcome, and assessor rationale. If a hint was needed, teach the gap and try a new variant in a later attempt. Do not retroactively relabel the assisted answer independent.

## Updating progress

Lesson status is one of not_started, in_progress, needs_review, blocked, or completed. Keep completed for lessons whose exit evidence and independent check are both satisfied.

Each attempt stores its session path, date, assistance, assessment result, and evidence paths. The start script fills an unassessed attempt; the supervisor and learner fill actual results at the end.

Capability status is separate: not_assessed, introduced, practiced_with_assistance, demonstrated_independently, or needs_review. Set evidence to the attempt records that support the claim. A checkpoint may downgrade a prior capability to needs_review without rewriting history.

Example of a completed attempt entry, to adapt only after observing the work:

    {
      "session": "sessions/M1-06/attempt-01.md",
      "date": "YYYY-MM-DD",
      "assistance": "agent_implemented",
      "independent_check": "passed",
      "evidence": ["labs/m1-06/README.md", "labs/m1-06/"]
    }

The assistance field describes the learning exercise, not the independent check. Valid values are not_recorded, independent, hints, or agent_implemented. The independent_check field separately records the assessment.

Do not insert a commit's own hash into files that same commit contains. Use the lesson ID in the commit message; a subsequent record may refer to an earlier hash. Commit messages and Git history provide the immediate association.

## Closing the session

- Compare observed results with exit criteria and the original prediction.
- Record help received and unfinished work.
- Remove only the namespace/unit/process resources created by the current lesson. Record anything still running.
- Review staged files for secrets and accidental raw captures.
- Update progress; run the curriculum checker.
- Commit the artifact and session record locally. If Git identity or commit permissions prevent this, leave the files intact and record the reason.
- Leave the next lesson ID or exact recovery task in the session's handover.

## When blocked

Environment failure is not a failed concept assessment. Mark the affected lesson blocked, record a minimal reproduction, and select a ready standalone lesson from the manifest if useful. Do not mark the skipped lab completed using a diagram, video, simulated output, or an agent's knowledge.

At a checkpoint, use one unfamiliar variation per required capability rather than a comprehensive reimplementation. Keep assessment focused on the concepts named by the checkpoint. Additional failures become clearly identified recovery attempts.
