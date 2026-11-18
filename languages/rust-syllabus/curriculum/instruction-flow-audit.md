# Instruction-flow audit — 2026-09-09

Finding: the reported opening confusion is a course defect. The learner followed the displayed next action. That action required an answer without presenting the question or explicitly directing the learner to it.

The findings below describe the initial audit. Subsequent learner feedback showed that copying prompts and directions into the attempt created a second tutorial. The current flow keeps instructions in the lesson and answers/results in the attempt; direct links preserve access to the question.

## Scope and evidence

Reviewed the README, learner workflow, supervision rules, session template, progress helper, current attempt, manifest dependencies, and all 30 lessons' entry paths, prediction prompts, starting states, exercises, assessment handoffs, and recovery instructions. M1-01 has no prerequisites. Its only attempt has no learning evidence; `labs/m1-01/` has no artifacts. No completion claim was inferred from earlier authoring commits.

This audits instruction flow. It does not validate external resource availability, lesson timing in practice, Linux behavior, or learner understanding.

## Breakdowns and corrections

| Breakdown | Evidence before this change | Correction |
|---|---|---|
| Answer requested without a question | `show_active_lesson()` printed a generic instruction; the session template contained only a supervisor-facing placeholder | Status and newly generated records include the objective and full prompt from the authored lesson; the existing unfilled M1-01 record is repaired |
| Circular navigation | All 30 **Today's path** sections sent the learner to the answer area without pointing to **Predict before reading** | Link directly to the prompt and distinguish reading instructions from reading assigned explanations |
| Unclear answer scope at the first lesson | M1-01 bundled three subjects into one sentence using unfamiliar terms | Three concrete questions, expected response length, and explicit permission to record unfamiliarity |
| Resume instruction overclaims knowledge | Every active `status` call prescribed the opening prediction; progress stores no within-lesson step | Conditional opening/resume guidance; preserve the original prediction and record the next unfinished step in Handover; README no longer promises an exact tracked step |
| Missing prediction inputs | M1-05 referenced three unspecified outcomes; M1-07, M1-14, and M1-21 required unspecified changed cases | Supply concrete enum/optional-value inputs for M1-05; explicitly obtain supervisor cases before checkpoint predictions |
| Checkpoint exercise/assessment ordering | Generic paths placed the independent check after an exercise that already constituted the check | Checkpoint-specific paths and workflow guidance require answers before hints or repairs |
| Setup instructions omitted from the main path | Generic step 3 jumped directly from prescribed reading to exercise despite conditional setup in Starting state | Step 3 now includes required setup before exercise; M1-01 no longer asks for a second session record |
| Structural checks missed usability | Existing validation required headings and valid paths but did not establish prompt delivery | Check nonempty objective/prompt sections; regression checks cover delivery across all 30 generated records and preservation on resume |

## Authoring rule

Whenever an instruction asks for an answer, show the actual question or provide a direct link with an explicit instruction to read it now. Specify any needed inputs, where the response goes, and what follows it. An independent check may require a supervisor to supply fresh cases, but that handoff must precede the request to answer.

The lesson holds the objective, questions, and directions. Start creates a worksheet with a link to the question; it does not copy the tutorial. Historical records are not regenerated on resume. Edits to a live lesson do not authorize overwriting an earlier learner response.

## Handover

The learner has since recorded the three opening predictions. Resume lesson 01 at **Prescribed reading, in order**; reading, portable experiments, lab-access planning, baseline evidence, and independent assessment remain unrecorded. The changes are agent-authored course maintenance and do not count as learner implementation or mastery. No lab resources were created.
