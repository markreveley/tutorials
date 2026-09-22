# Self-contained setup and lesson audit reference

Current coverage: the [full remaining-lesson audit](#full-remaining-lesson-audit--2026-09-10) below supersedes earlier “remaining work” notes. M1-02 through M1-30 have been revised; Linux execution remains unverified. Earlier sections preserve the history and rationale of each pass. The later [agent-led Lesson 1 pilot](#agent-led-lesson-1-pilot--2026-09-10) changes delivery and narrows M1-01's scope; its current record supersedes older resume notes.

## Why this revision exists

On 2026-09-09 the learner annotated `lab-setup.md` with `->[...]` comments. The questions were practical: how to create the required Linux environment on a Mac; whether Docker or Sprites would work; what the prerequisites and warnings meant; where to run commands; and why undefined Linux terminology appeared before instruction. The learner requested discussion first, then implementation and a committed reference for auditing other lessons.

The root problem was missing instruction, not missing learner effort. Listing requirements such as “systemd as PID 1” does not teach someone how to obtain them. A source link or instruction to consult manuals does not supply a starting state, runnable procedure, or way to recognize success. Setup details must be taught before they are required, or explicitly supplied as assisted scaffolding.

The learner's comments have been resolved into the changes below. This document preserves their intent after removing the inline annotations from the guide. It is a supervisor/author reference, not an additional learner reading assignment.

## What changed and why

| Previous gap | Implemented correction | Reason |
|---|---|---|
| Linux requirements without installation steps | Prescribed local Multipass + Ubuntu 24.04; installer, VM creation, packages, Rust, and capability checks | Provide one concrete path that fits the later service-management lessons. |
| Unclear Mac versus Linux location | Label commands by machine and directory; explain entering/exiting the VM | Prevent executing Linux or administrative commands in the wrong place. |
| Linux setup vaguely deferred | Mac preflight in M1-01; explicit setup entry at M1-04 before Linux observations | Keep the first module focused without leaving an undisclosed future prerequisite. |
| Preflight output never saved to its required artifact | Include directory creation, output redirection, JSON review, and expected Mac results | Produce the actual file the lesson requires and avoid interpreting normal Mac flags as failures. |
| Unexplained fixture invocation | M1-01 supplies guided commands, immediate status capture, expected stream text, and error recovery | Make the opening experiment executable without supplying the later independent-check answer. |
| No path for code/evidence between machines | Local Git bundles, an Ubuntu checkout, return transfer, review, and fast-forward-only integration | Preserve work without publishing the repository, transferring account credentials, or mounting Mac files into privileged experiments. |
| Dense precautions without context | Explain the dedicated VM, ordinary user, operator, and later Linux terms at their point of use | Connect each rule to the action it governs. |
| Manual references standing in for teaching | Specify Ubuntu package commands and explain how to consult a named installed manual | Reference material supports the procedure instead of becoming an unbounded prerequisite. |
| Missing failure and session-end path | Give concrete recovery entries, handover location, transfer and shutdown instructions | A learner must know what to preserve and where to resume after failure or a pause. |

The implementation updates the setup guide, M1-01's exercise, M1-04's setup entry/artifacts, the manifest, supervision instructions, README directory, and continuity records. It does not implement upcoming learner exercises or change the prerequisite order. The earlier uncommitted opening-reading/practice clarifications in the files touched here are retained. Other pre-existing lesson edits remain outside this commit's scope.

## Standard for future lesson audits

The standing tutorial rules live in [root AGENTS.md](../AGENTS.md#tutorial-writing-and-guidance), the entry point for agents working in this repository. Apply them before using the checklist below: current-step relevance, explicit actions, the learner's actual context, explained terminology, purposeful notes, one purpose per step, and a separate preflight for each lesson. A thorough checklist does not justify presenting every item to the learner at every step.

Audit from the learner's demonstrated starting point, using the manifest and actual prerequisite evidence. A topic mentioned in an earlier document is not proof it has been taught or learned. For each required action, verify:

1. **Purpose:** State what this step contributes to today's concept and whether it is reading, setup, guided practice, or independent assessment.
2. **Starting state:** Name the machine, directory, existing files, tools, and prior knowledge. Every prerequisite needs earlier evidence or a bounded setup route.
3. **Action:** Supply exact commands/clicks or an appropriately scoped learner task. Explain options, placeholders, directory changes, and shell behavior before relying on them. A setup skeleton is not a complete setup procedure.
4. **Expected result:** Say what successful execution looks like, which variations are normal, and which nonzero results are intentional. Label example output as expected, never observed.
5. **Evidence:** Name the file to create, how it is created, what the learner records, what is ignored, and what is reviewed/staged/committed. Check that a command actually produces its promised artifact.
6. **Recovery:** Give the next diagnostic or repair step for likely failures, what error to retain, and an exact resume point. “Resolve prerequisites” alone is insufficient guidance.
7. **Continuity and cleanup:** Explain what persists, how work moves between machines, which named resources must stop, and how to verify that. Preserve uncertain and failed outcomes.
8. **Assessment boundary:** Explain the learning objective and obtain a prediction before teaching. Give guided setup enough support to succeed. For an independent check, obtain an attempt before hints or code; use a fresh variant rather than repeating a worked answer.
9. **Lesson-specific preflight:** Include only the tools and checks this lesson needs, in the lesson itself or a dedicated file. Do not route the learner through a shared guide and ask them to filter sections, flags, or results. Shared implementation helpers are acceptable if each lesson presents its own complete instructions and relevant output.

Self-contained does not mean reproducing entire manuals, solving learner tasks in advance, or requiring every setup section at the start. It means the assigned path supplies every necessary step at the point it is needed. External links provide authoritative downloads and selected background; they must not conceal missing instructions.

Avoid replacing unexplained jargon with a glossary detached from the exercise. Define a term where it affects the learner's next action. Avoid asking novices to choose among several platforms unless platform selection is itself the module's concept.

## How to perform and record the remaining audit

Read this reference, the contract, supervision protocol, current progress, and the lesson's prerequisites. Trace the learner's path from entry through setup, exercise, evidence, check, and handover. Inspect supplied scripts and artifacts rather than assuming they match the prose. Use one finding per concrete gap, with this record format:

| Lesson/section | Assumed knowledge or missing step | Learner consequence | Proposed correction | Verification and remaining limits |
|---|---|---|---|---|
| Exact path and heading | What the text assumes without teaching | Where the learner gets stuck or misinterprets a result | Specific instruction or scoped scaffolding | File/source inspected, command actually tested, or explicitly pending host check |

Review proposed corrections against the module's concept and independent check. Make changes in coherent groups, preserve the learner's words, update records when the resume point changes, run `python3 scripts/curriculum.py check`, and review the Git diff. Run relevant existing tests when structural behavior changes. Do not execute future exercises to award evidence or claim that a prose audit proves Linux compatibility.

## Audit coverage and remaining work

- **Revised in this pass:** opening setup guide; M1-01 setup/fixture instructions; M1-04's Linux setup entry and inventory requirement; supervisor audit standard.
- **Not an end-to-end execution certificate:** Mac software installation, Multipass operations, Ubuntu package installation, Rust installation, and privileged Linux experiments remain unexecuted in this authoring pass. See [validation](validation.md) for the checks actually run.
- **Priority next audit:** M1-03 shell syntax and output capture; M1-04's exercise itself (fixture arguments, terminal/process coordination, `ps`, `/proc`, and exact-PID signals); M1-22–M1-27 administrative commands, evidence lifetime, and cleanup. M1-04's setup entry is revised, but its process exercise has not received the full audit.
- **Remaining lessons:** apply the same standard to all 30 modules, including artifacts, reading selections, and fresh assessment variants. No whole-curriculum pass is claimed here. Existing reading-only labels do not establish that exercise directions are sufficient.

This reference records the requested future audit method; it does not silently initiate new lessons or mark them complete.

## Current-step relevance revision — 2026-09-10

The learner found the instruction to identify “which computer” and copy a future Linux plan confusing: they have one Mac, and no Linux setup action belonged to the current step. They proposed: “only present information relevant to the current step or goal. if presenting information that falls outside of this, qualify it with why its being presented.” They also requested separate preflight instructions for each lesson, without a shared preflight requiring applicability qualifiers.

The seven rules are committed in root `AGENTS.md` so supervisors encounter them with repository instructions. `supervision.md` points to those rules, and this document holds the rationale and audit method. These are authoring instructions, not extra reading assigned to the learner.

| Lesson 1 finding | Correction | Reason |
|---|---|---|
| Step 2 required a machine declaration and future Linux plan | Removed that task and the Linux-planning exit criterion | The machine is known and copying future instructions adds no learning evidence. |
| Required reading routed through shared lab context | Put the complete Mac preflight in lesson 1 and remove its duplicate from `lab-setup.md` | The learner should not decide which parts of a general environment guide apply. |
| Inventory printed unrelated Linux capabilities | Added `scripts/m1_01_preflight.py`, reporting only platform and Python/Git/Rust/Cargo versions | Results now match this lesson's tool checks. The existing report is preserved, not regenerated. |
| Setup, output capture, reflection, and file review were mixed together | Give the exercise separate steps for tools, experiment, explanation, and starting knowledge | Each step now has a clear action and completion point. |
| Broad starting-knowledge questions lacked a stated purpose | Explain that the survey helps tailor teaching, briefly describe its terms, and say not to research unfamiliar topics | Context outside the immediate experiment now has an explicit reason and task boundary. |
| Notes repeated future plans and experiment commands | Record observations/explanations once; have the supervisor index them and maintain administrative records | Notes preserve useful evidence rather than duplicating the tutorial. |
| Learner was asked to review the lesson source as exercise output | Review actual evidence files at commit time; keep curriculum authoring separate | Learning to review a commit should concern the work actually being committed. |

This supersedes the earlier M1-01 instruction to record a Linux access plan. M1-04 still introduces Linux setup. Lesson IDs, ordering, the three existing prediction questions, resource selections, and independent-check requirements are retained. No future exercise was implemented. All remaining lessons still need the full audit, including conversion to their own preflight instructions; the shared guide remains a source for that authoring work, not the pattern to copy into new learner flows.

### Authoring handover

The learner explicitly said not to change `sessions/M1-01/attempt-01.md`. It is left untouched; this section carries revision continuity instead. The agent inspected `labs/m1-01/preflight.json` (Mac, Python 3.14.3, Git/Rust/Cargo versions present) and `labs/m1-01/baseline.md` (empty). Both learner files are preserved. The inventory is an observed file, not independent evidence of understanding.

Next learner action: M1-01 **Exercise → 2. Run the supplied program and record what happens**. Fixture observations, the learner explanation, baseline responses, and an independent check remain unrecorded. The unchanged attempt's older step-1 handover should not cause repeated reading or regeneration of a valid inventory. `progress.json` records the current resume guidance without awarding completion.

Assistance: agent-authored tutorial maintenance; no learner answer or assessment supplied. The agent does not run the learner's fixture in this revision. No VM or lesson resource was created; no lesson cleanup is required. Pre-existing changes in the contract and other lesson files, the untracked learner inventory/baseline, `.nvimlog`, and `main` are outside this authoring commit. Verification is recorded in [validation](validation.md).

## Full remaining-lesson audit — 2026-09-10

The learner requested all remaining tutorials be revised against the current-step rules, with a separate preflight per lesson. The learner also asked what “supervisor” meant. Learner-facing text now calls that role the **guiding agent**, defines it as the agent in the conversation, and separates learner responses from agent-assigned cases and recordkeeping. M1-01 receives that terminology correction only; its existing practice and independent-check scope remain intact.

### Changes common to the remaining lessons

- Each of M1-02–M1-30 links to its own complete preflight in `curriculum/month-01/preflight/`. No lesson assigns a shared applicability checklist or `scripts/preflight.py` inventory. M1-01 retains its own inline preflight.
- Every setup names the actual Mac or Ubuntu checkout, current tools and inputs, existing-work preservation, completion signal and recovery. Linux pages include their own local transfer and session-end path. Rust and administrative tools are introduced when needed, not installed during M1-04's process setup.
- `lab-setup.md` is now an agent/author environment policy reference, with old headings retained for historical links. It no longer competes with the lesson-specific procedures.
- Exercises name missing starting material and bounded inputs. Source examples are reading unless explicitly assigned to run. Optional work stays on the present concept; unavoidable future context states why it appears and whether action is required.
- Commands/results are recorded once, with pointers from the attempt. The agent maintains evidence indexing, progress and assessment. Successful execution does not substitute for a fresh independent explanation/change; inconclusive required evidence stays incomplete.
- Manifest artifacts now identify concrete source/test paths, lockfiles and event evidence. The prescribed order and prerequisite graph are unchanged; a cross-reference to the M1-02 threat model was removed from M1-13's required writing to avoid an undeclared dependency.

### Per-lesson findings and verification boundaries

All rows also receive the common changes above. “Revised” means authored and structurally reviewed, not taught, executed or independently passed.

| Lesson | Finding | Revision and reason | Verification boundary |
|---|---|---|---|
| [M1-02](month-01/lessons/02.md) | Product terms and comparison scope were implicit | Defines control plane/BYOC/on-premises, fixes the three comparison subjects and dated evidence columns, and labels unknowns. | Read-only survey; no deployment or account setup. |
| [M1-03](month-01/lessons/03.md) | Quoting/redirection and reproduction inputs were underspecified | Supplies filename/stream commands, immediate status capture, one Bandit task plus local fallback, and explicit script input. | Fixture interface inspected; shell blocks parse, SSH not operated. |
| [M1-04](month-01/lessons/04.md) | Generic Linux inventory and unspecified PID coordination | Own VM/process-only setup and inventory; two-terminal finite runs, fresh PID capture, signal/wait observations. | No VM created or process experiment run. |
| [M1-05](month-01/lessons/05.md) | A small program was assumed without a package or concrete cases | Own Cargo initialization, fixed enum/Option examples, compile-error practice and new-variant assessment. | Package/source are learner deliverables, not preimplemented. |
| [M1-06](month-01/lessons/06.md) | Ownership examples and compilation layout were unnamed | Concrete signatures for prediction; separate move/borrow/return/conflict/scoped files outside Cargo targets. | Intentional compile failures retained as learner evidence. |
| [M1-07](month-01/lessons/07.md) | Checkpoint setup and administrative tasks obscured assessment | Own shell/process/Rust preflight; agent supplies three new inputs and records results; no fictitious reading assignment. | No cases or learner answers supplied in this audit. |
| [M1-08](month-01/lessons/08.md) | Borrowed-return starting files were absent | Names independent borrowed/local-reference/owned files and compile/run locations. | Fresh interface check remains separate. |
| [M1-09](month-01/lessons/09.md) | Invalid input and IO cases lacked fixed starting data | Defines accepted range, three file contents, one absent file, and typed propagation through two functions. | No parser or expected learner explanation implemented. |
| [M1-10](month-01/lessons/10.md) | Capstone initialization and field promises were ambiguous | Supplies library setup preserving README, bounded fixture/request ranges, pure validation, and explicit unenforced fields. | No executor prebuilt; script-path assessment fits fixed arguments. |
| [M1-11](month-01/lessons/11.md) | Runner demonstration and missing-executable case were unspecified | Fixes three demo labels, checks absent path without deletion, and separates Cargo status from child status. | Source remains a learner implementation. |
| [M1-12](month-01/lessons/12.md) | Tests and deliberate defect recovery were vague | Names outcomes.rs, commands, path handling, mutation/repair, and formatter/linter setup. | No future Rust tests run by the author. |
| [M1-13](month-01/lessons/13.md) | Environment experiment risked global mutation and missing scratch paths | Controlled synthetic parent; explicit allowed marker, working/missing directories, ordinary-user unreadable copy and restoration. | No actual environment dump or permissions changed. |
| [M1-14](month-01/lessons/14.md) | Request cases and progress maintenance were mixed | Agent assigns exact fresh requests; learner traces and changes existing code; agent records capability results. | No new concept or prepared assessment answer. |
| [M1-15](month-01/lessons/15.md) | Thread/channel example lacked a bounded starting package | Standalone package, concrete owned values, joins, sender drop and debugging receive timeout. | Optional work stays on channel lifetime, not later ownership types. |
| [M1-16](month-01/lessons/16.md) | Pipe capture lacked exact tests and included later descendant concepts | Defines byte caps, dual readers, finite Emit case and outer timeout; independent case stays direct-child only. | Outer timeout is failed/incomplete evidence, never success. |
| [M1-17](month-01/lessons/17.md) | Deadline experiment omitted concrete timing and observation points | Instant, bounded polling, fresh test target and tolerant timing; records termination, wait and readers separately. | No descendant guarantee assigned yet. |
| [M1-18](month-01/lessons/18.md) | Process-group setup and identity safeguards were implicit | Python harness has fixed direct/group cases, fresh positive group ID checks and finite outer bounds. | No unsafe Rust or runner integration added. |
| [M1-19](month-01/lessons/19.md) | Event spoof test and JSON artifact generation were unspecified | Adds fixed test-only spoof source task, JSONL validation, per-run IDs and producer/path separation. | Serialization library introduced only here. |
| [M1-20](month-01/lessons/20.md) | Reducer location and synthetic-versus-observed data were ambiguous | One pure module/test path, four labelled synthetic histories, distinct outcomes and no execution/retry. | Manifest no longer offers alternative unresolvable artifact paths. |
| [M1-21](month-01/lessons/21.md) | Checkpoint input handoff and explanation evidence were unclear | Three new inputs plus bounded descendant explanation; separate observed/assisted results per capability. | No new cleanup implementation or answer supplied. |
| [M1-22](month-01/lessons/22.md) | Shared setup, privileged fallback and terminology obscured the PID view | Own checks; concrete unshare invocation, outside PID observations, privilege-dropping fallback and exact recovery. | Linux access/policy still requires live verification. |
| [M1-23](month-01/lessons/23.md) | Network claim lacked a valid control case and finite cleanup | Named namespace, empty local HTTP directory, host/client comparison, immediate statuses, timeout and exact deletion. | No bridge, NAT or global networking change. |
| [M1-24](month-01/lessons/24.md) | Shared skeleton omitted runnable launch and evidence lifetime | Concrete ordinary-user transient service; guarded membership reads, live counters, retained unit result and cleanup. | Retained unit is not assumed to retain its cgroup. |
| [M1-25](month-01/lessons/25.md) | Memory failure could count as complete while attribution was inconclusive | Fixed CPU/memory cases, outside live evidence capture, limits on workload size, incomplete status until justified. | Actual counter availability/OOM attribution unverified. |
| [M1-26](month-01/lessons/26.md) | Descendant test and runner/event entry path were unspecified | Finite tree/service timing, outside observation, fixed runner case and event-prefix artifact directory. | No fabricated terminal event or side-effect guarantee. |
| [M1-27](month-01/lessons/27.md) | Composition assumed a binary and inspectable fast-exit process | Uses existing controls, fixed demo labels, separate live Sleep placement case, namespace inode comparison and ordered cleanup. | Source changes included among required artifacts. |
| [M1-28](month-01/lessons/28.md) | Property generator/oracle and regression retention were vague | Bounds chunks/cases, independent expected prefix, deliberate defect, shrinking and reviewed regression seeds. | Proptest introduced here; pure test on Mac only. |
| [M1-29](month-01/lessons/29.md) | Clean checkout could accidentally rely on the original repository | Creates a distinct local clone, records original-path failures, transfers committed fixes, retains evidence. | Explicitly same-VM reproduction, not second-host validation. |
| [M1-30](month-01/lessons/30.md) | Next-stage reading could imply immediate KVM/provisioning work | Separates independent demonstration from a next-boundary proposal; explains why future context appears. | No microVM setup, rental, or future readiness claim. |

### Authoring handover and protected work

The pending learner/reading work was saved in local commit `b0ad9f8` before this audit. This audit is agent-implemented curriculum maintenance, not learner implementation or assessment. No capstone source, future lab solution, learner answer, installer, VM, service or namespace was created or run. The new Python inventory and regression tests are authoring/setup helpers only.

`sessions/M1-01/attempt-01.md` was not edited. Its old handover remains historical; use current progress plus the actual evidence files for resuming. The learner's saved commands/statuses and six baseline responses remain intact. Their newer, lesson-specific Mac tool inventory edit in `labs/m1-01/preflight.json` is preserved and excluded from this authoring commit, as are `.nvimlog` and the compiled `main` executable.

Next learner action remains M1-01 Exercise step 3: discuss the learner's uncertainty about the recorded exit codes and preserve the actual stdout/stderr observations still absent from the log; then obtain a fresh independent check when ready. No independent case was assigned during this audit, and no lesson/capability status was advanced. Authoring continuity is kept here and in progress, respecting the protected attempt. No lab cleanup is required from the author's actions.

Run the regression suite, structural checker and diff checks before future revisions; [validation](validation.md#remaining-lessons-and-role-clarity--2026-09-10) records this pass's actual results and Linux limitations. Re-audit any changed shared implementation helper against each dedicated preflight that uses it; do not restore a generic learner checklist.

## Agent-led Lesson 1 pilot — 2026-09-10

The learner identified a remaining design problem after the full lesson audit: clearer documents still required coordination among a lesson, report, attempt, preflight and agent, while the reason for the work remained obscure. The learner approved a one-lesson conversational pilot before building a terminal tutorial or converting the rest of the course.

### What changed and why

| Change | Reason |
|---|---|
| M1-01 opens with what is learned, its connection to the future task runner, and a completion condition | The experiment needs an understandable purpose before commands or administration. |
| The agent presents one authored step and waits | The learner gets one place to follow the lesson, while the authored sequence prevents improvising a competing curriculum. |
| Setup is a minimal inline Python check; Git appears only at the assisted save step | Supporting tools should appear when required for the current action. The optional legacy M1-01 report also stops checking Rust; existing learner reports are not rewritten. |
| Rust onboarding moves to M1-05's reading and dedicated Mac setup | Removing it from M1-01 must not create a hidden prerequisite for the first Rust program. Existing completed reading/practice is retained, not repeated. |
| Broad baseline and separate inventory/report writing are no longer M1-01 requirements | These created additional tasks without serving the command-result objective. Existing files remain unchanged as history. |
| Independent assessment focuses on command messages, reported status, and what the report establishes | File-selection/Git terminology and Rust practice are no longer competing assessment goals in this lesson. A fresh learner attempt is still required. |
| The existing helper supports an explicit agent-led delivery mode and a saved step | Status/start now resume the conversation at a validated authored heading instead of always directing the learner to the opening prediction. It is not a shell tutorial engine or an automatic assessment system. |
| attempt-02.md is the active pilot continuation | The learner protected attempt-01.md. Referencing the original observations preserves them without rewriting or duplicating answers. Only one record is actively maintained. |

The manifest's step order and lesson headings are the teaching sequence. The active attempt's step is the saved position; the agent updates it from the actual exchange, never from command success alone. The helper validates headings/step IDs and does not advance or award understanding. README, the learner workflow and root agent rules distinguish this pilot from the unchanged document-led delivery of later lessons.

The lesson title becomes “Understand a command's result.” Its existing reproducible-observations capability is retained. The numbered curriculum order and prerequisite graph are unchanged. The only later lesson content changed is the M1-05 onboarding needed to preserve that prerequisite path. No future learner exercise was implemented.

### Current learner handoff

Continue M1-01 at explain in the [active pilot record](../sessions/M1-01/attempt-02.md). The original prediction, reported statuses 0 and 7, and uncertainty about their meaning remain in the protected attempt. Do not repeat setup or Rust practice. Explain the status convention and the fixture's deliberate report, then obtain one learner response in conversation. Actual stream text is still missing; request only a focused rerun to recover that evidence after the discussion. A fresh independent check remains unattempted.

The agent inspected the protected attempt, saved inventory and baseline without changing them. The newer inventory edit, .nvimlog and main are outside this authoring change. No learner answer, fixture run, tool installation, VM, process or privileged resource was created by the authoring work; no lab cleanup is needed. Implementation assistance remains not_recorded because this pilot preparation does not establish how the earlier exercise was performed. Guided teaching is recorded separately from implementation and independent assessment.

This is an implemented delivery pilot, not a demonstrated improvement in learning outcomes. Obtain learner feedback on the conversational experience before expanding it or authoring shell tutorial software. [Authoring verification](validation.md#agent-led-pilot-verification--2026-09-10) records actual checks; Git history supplies any authoring commit ID.
