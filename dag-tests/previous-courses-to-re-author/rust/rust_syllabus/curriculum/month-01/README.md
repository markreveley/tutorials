# Month one: explain and constrain local execution

**30 modules · concept-focused exercises · evidence-based progression**

This page maps the first curriculum stage. To do the work, use the [learner workflow](../learner-workflow.md) and the single current lesson reported by `python3 scripts/curriculum.py status`.

The endpoint is a small Rust runner plus operator-controlled Linux experiments demonstrating explicit requests, failure outcomes, bounded output, deadlines, descendant cleanup, namespace placement, resource limits, and honest lifecycle evidence. The learner can explain which guarantees were observed and where the architecture remains incomplete.

The `month-01` directory contains the foundations stage. Work through it at your own pace. The [continuing roadmap](../roadmap.md) preserves that material.

## Four milestones

| Modules | Evidence at the boundary |
|---|---|
| 01–07 | Command-result observations, product/threat survey, shell/process observations, ownership checkpoint |
| 08–14 | Reviewable Rust request/error model and tested synchronous runner |
| 15–21 | Bounded streams, direct-child deadlines, descendant experiments, structured/incomplete evidence |
| 22–30 | Linux boundary experiments, combined demonstration, property test, clean-checkout reproduction, final checkpoint |

Each module ends when its evidence and independent check are complete. Unfinished work remains a recorded gap to address before dependent modules.

## Module sequence

| Module | Concept | Type | Prerequisites |
|---|---|---|---|
| [M1-01](lessons/01.md) | Reproducible observations | standalone | None |
| [M1-02](lessons/02.md) | Claims and threat boundaries | standalone | M1-01 |
| [M1-03](lessons/03.md) | Shell input and output | standalone | M1-01 |
| [M1-04](lessons/04.md) | Process lifecycles | standalone | M1-01, M1-03 |
| [M1-05](lessons/05.md) | Rust data and control flow | standalone | M1-01 |
| [M1-06](lessons/06.md) | Ownership transfer and borrowing | standalone | M1-05 |
| [M1-07](lessons/07.md) | Checkpoint: ownership and process boundaries | checkpoint | M1-03, M1-04, M1-06 |
| [M1-08](lessons/08.md) | Borrowed return values and lifetimes | standalone | M1-06 |
| [M1-09](lessons/09.md) | Typed failure handling | standalone | M1-05 |
| [M1-10](lessons/10.md) | Execution requests and validation | sequential | M1-07, M1-08, M1-09 |
| [M1-11](lessons/11.md) | Spawn and exit outcomes | sequential | M1-04, M1-10 |
| [M1-12](lessons/12.md) | Tests of observable behavior | sequential | M1-11 |
| [M1-13](lessons/13.md) | Explicit execution context | sequential | M1-03, M1-11, M1-12 |
| [M1-14](lessons/14.md) | Checkpoint: the execution contract | checkpoint | M1-07, M1-12, M1-13 |
| [M1-15](lessons/15.md) | Ownership across threads | standalone | M1-06, M1-14 |
| [M1-16](lessons/16.md) | Concurrent pipe draining with bounded retention | sequential | M1-12, M1-15 |
| [M1-17](lessons/17.md) | Deadlines and direct-child cleanup | sequential | M1-16 |
| [M1-18](lessons/18.md) | Descendants and inherited pipes | standalone | M1-04, M1-15, M1-17 |
| [M1-19](lessons/19.md) | Event provenance | sequential | M1-17, M1-18 |
| [M1-20](lessons/20.md) | Incomplete execution histories | standalone | M1-09, M1-19 |
| [M1-21](lessons/21.md) | Checkpoint: execution under failure | checkpoint | M1-14, M1-16, M1-17, M1-18, M1-20 |
| [M1-22](lessons/22.md) | Process views in namespaces | standalone | M1-04, M1-21 |
| [M1-23](lessons/23.md) | Network namespace reachability | standalone | M1-22 |
| [M1-24](lessons/24.md) | Cgroup membership and accounting | standalone | M1-21, M1-22 |
| [M1-25](lessons/25.md) | Resource limits and their effects | sequential | M1-24 |
| [M1-26](lessons/26.md) | Service-wide descendant cleanup | sequential | M1-18, M1-24, M1-25 |
| [M1-27](lessons/27.md) | Composition of execution controls | sequential | M1-19, M1-23, M1-25, M1-26 |
| [M1-28](lessons/28.md) | Property testing against an oracle | standalone | M1-12, M1-16 |
| [M1-29](lessons/29.md) | Reproducibility from a clean checkout | sequential | M1-27, M1-28 |
| [M1-30](lessons/30.md) | Checkpoint: evidence for system guarantees | checkpoint | M1-02, M1-21, M1-27, M1-28, M1-29 |

Standalone labs can be used to make progress around an environment blocker when their prerequisites are satisfied. The default sequence remains the numbered order. Checkpoints gate later integration.

## Working through a module

M1-01 is an agent-led pilot: continue in the conversation, one step at a time. The agent maintains the record and saved step. Other modules retain their lesson/attempt flow while the pilot is evaluated. The [learner workflow](../learner-workflow.md) explains both entry paths.

## Stage completion

- The clean-checkout runner demonstrates success, nonzero exit, spawn failure, bounded output, and a direct-child timeout.
- A finite descendant case distinguishes parent termination, inherited pipes, and service/cgroup cleanup.
- Linux observations support the stated namespace and resource-limit behavior.
- Structured event histories distinguish confirmed outcomes from incomplete evidence.
- The learner independently explains selected ownership, lifecycle, authority, and evidence boundaries.
- The final report lists unsupported claims and exact prerequisites for next-month microVM work.

If a Linux experiment or understanding check is incomplete, preserve the rest of the evidence and record a bounded recovery task. The existence of these lesson documents is never a completed month.
