# M1-01 — Understand a command's result — attempt 02

- Date: 2026-09-10
- Delivery: agent-led pilot continuation
- Environment: learner's Mac
- Implementation assistance: not_recorded
- Independent check: assisted — code-23 explanation needed teaching on the limits of a reported status
- Lesson status: in_progress
- Current step: explain — [Explain the observed result](../../curriculum/month-01/lessons/01.md#explain-the-observed-result)

This is the single active agent-maintained record. The learner answers in conversation, not in a second worksheet. [Attempt 01](attempt-01.md) is protected and unchanged; this continuation does not imply a failed or repeated independent check.

## Evidence carried forward

- The learner's original prediction, reported fixture invocations/statuses 0 and 7, and explanation expressing uncertainty remain in attempt-01.md. Refer there rather than copying the answers.
- The saved [Mac inventory](../../labs/m1-01/preflight.json) reports Python 3.14.3 and Git 2.49.0. It was inspected, not regenerated; no setup commands were rerun.
- The earlier [baseline](../../labs/m1-01/baseline.md) and Rust reading/practice are preserved. They are not requirements of this pilot and need not be repeated.
- The earlier command log did not contain actual stdout/stderr text. The learner's focused code-7 rerun below supplies that missing observation; the protected earlier log remains unchanged.

## Conversation and observations

The learner agreed to pilot an agent-led, sequential Lesson 1 after identifying unclear purpose and excessive document coordination. The agent authored the delivery change and resumed from the existing explanation gap. No new fixture execution or learner answer has been obtained during authoring.

The agent explained the success/nonzero convention, the fixture's deliberately selected status, and `echo $?` displaying that status. Asked whether a message on stderr alone establishes failure, the learner replied: "i would look at the error code on stdout".

This answer looks beyond stderr, but leaves the distinction between the original program's exit status and `echo` printing that status unresolved. Do not treat it as demonstrated understanding or simply reject the word stdout: `echo` does print through its own stdout. The learner briefly asked about model selection, then requested continuation.

On resuming, the agent clarifies that the Python program returns an exit status separately from its messages; the shell exposes that status as `$?`, and `echo $?` prints it through echo's own stdout. The term exit code includes success as well as failure. The current guided question is: if `echo $?` were omitted, would the Python program still have an exit status? The learner's response is pending. This is guided teaching, not an independent check; no new fixture execution was observed.

Before answering the guided question, the learner asked what happens when there is no previous command, what an exit status is, how it is emitted, what `$?` means, and how the status reaches it. The agent explains normal process termination through the OS, the shell collecting termination information through wait/waitpid and retaining the numeric status, and parameter expansion before echo executes. Agent-only diagnostic: `zsh -f -c 'print -r -- "$?"'` printed `0`; this is a shell-initialization check, not a learner fixture run or learning evidence. Startup commands can change the initial value. No learner explanation or assessment result is inferred from these questions. Remain at explain until the learner can distinguish the status from displaying it.

The learner then said "ok proceed with lesson". The agent supplied the commands for one focused code-7 rerun to recover missing stream text. This is guided observation using a previously worked value, not a fresh independent check.

The learner pasted these commands and terminal output. The shell prompt and its unrelated account details are omitted; command indentation is normalized.

```sh
cd /Users/mark/dev/repos/repos_private/syllabus
python3 labs/fixtures/workload.py exit --code 7
echo $?
```

```text
synthetic stdout
synthetic stderr
7
```

Agent review: the pasted result matches the fixture's exit-mode source and requested status. It is learner-supplied terminal evidence, not an agent rerun or proof of understanding. Asked which displayed lines were printed by Python and which by echo, the learner answered: "first two python, last echo". This correctly identifies the source of the displayed lines in guided practice. The agent confirms this and proceeds to a fresh check; this response alone does not establish the limits of the status report or complete the lesson.

## Independent check

- Assigned case: use the same fixture's exit mode with code 23, different from the worked values 0 and 7.
- Original prompt: before running anything, provide the commands to run this case and display its exit status, together with predicted output.
- Pre-run prediction: not supplied. The learner instead provided commands with their execution output. Do not reconstruct a prediction from an already observed result.
- Learner commands and actual output, with unrelated shell prompts/account details omitted:

```text
python3 labs/fixtures/workload.py exit --code 23
synthetic stdout
synthetic stderr
echo $?
23
```

- Learner explanation before hints:

> they tell me that workload.py can be passed an exit flag and then a --code flag and any following number will be the exit code that the program will emit on completion
> i'm not sure what they don't prove, but potentially that any number would be accepted as an exit code

- Review: the learner correctly identifies the deliberately chosen report and raises a valid limit of testing one value, but overgeneralizes acceptance to any number and has not explained reported outcome versus verified task outcome. The fixture source bounds --code to integers 0 through 125. Pre-run prediction remains absent. Neither the uncertainty nor the successful commands establish the required boundary.
- Assistance: commands, execution and the quoted explanation were obtained before hints. The agent now supplies the range correction and explains reported status versus independently verified useful work, using a hypothetical backup as an example. Case 23 is therefore assisted, not independently passed. Preserve this result when assigning a later fresh case.
- Guided recovery question: if --code changed from 23 to 0, what would change and what would still not be established? No further run is requested. After the learner explains the boundary, use a fresh case with prediction obtained before execution.

### Guided recovery response

The learner answered:

> it would change the exit code emitted by the program. it would still not affect the fact that this exit code is arbitrary and not reporting the result of real work
> would incorrect reporting of exit codes indicate a bug, race condition, or...?

Agent review: this correctly explains the fixture's chosen status versus a real task outcome after teaching. It is guided recovery evidence, not a retroactive independent pass for case 23. The agent answers the follow-up by distinguishing a violation of documented status meaning (a bug), possible causes such as ignored errors or timing-dependent concurrent work, a narrower documented promise such as request acceptance, and accidentally observing another command's status. These are hypothetical explanations, not diagnoses or observed failures. No new fixture run or independent case is assigned in this exchange.

## Exit evidence still needed

- Independent application of the reported-status boundary; guided explanations of printed lines and the fixture's arbitrary report are now recorded.
- An independently passed check, including the missing pre-run prediction evidence; case-23 commands/result are already recorded.
- Agent review of the evidence, actual exercise assistance, and local session save.

## Handover

- Guided recovery at explain now has a correct learner response. The learner's follow-up about incorrect status reporting is answered; continue with any clarification or a fresh independent case next, using a code other than 0, 7 or 23 and obtaining prediction before execution. No new case is assigned yet. Preserve case 23 as assisted; do not relabel the guided response independent.
- The code-7 output and correct guided identification of its printed lines are recorded. Do not repeat setup, baseline questions, Rust reading, or stream-recovery runs. The independent check and the limits of the status report still require learner evidence.
- No lesson or capability completion has been awarded. No learner code, VM, installer, running fixture or Linux resource was created by the agent; no lab cleanup is required.
- Authoring scope and rationale: [agent-led pilot revision](../../curriculum/setup-and-lesson-audit.md#agent-led-lesson-1-pilot--2026-09-10). Test results belong in authoring verification, not learner evidence.
- Repository at pilot handoff: tutorial/workflow/helper changes are agent-authored; the learner's existing inventory edit, .nvimlog and compiled main remain separate. The protected attempt, inventory and baseline are not edited by the pilot. Git history identifies any local authoring commit.
- Current conversation handoff: only this active record and progress note are updated, uncommitted. The protected attempt and existing learner files remain untouched; no model configuration change was requested or made.
