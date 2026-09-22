# Month-one capstone: a bounded task runner

The learner creates a Rust package here during M1-10. No reference implementation is supplied.

## Required end state

- A small library with a minimal command-line demonstration.
- A typed request for a fixed set of synthetic workloads; executable and argument boundaries remain explicit.
- Distinct spawn failure, nonzero exit, successful exit, and timeout outcomes.
- Explicit working directory and child environment.
- Concurrent draining of stdout and stderr while retaining at most a configured byte limit per stream.
- Direct-child deadline handling with kill-and-wait cleanup; documented limitations for descendants.
- Structured, synthetic JSONL run records with incomplete histories represented as unknown outcomes.
- Focused integration tests and a property test for the bounded buffer.
- Operator-run Linux lab scripts demonstrating cgroup ceilings, service-wide cleanup, and network namespace placement.
- Reproduction instructions, observed results, a threat-boundary diagram, and a limitations table.

## Deliberate boundaries

The Rust process does not become a privileged service, accept arbitrary remote commands, or implement authentication. The lab operator controls transient service/namespace setup. The fixture set is finite and local. Start with one workload at a time.

The service wrapper constrains the runner and its children together. It is not yet a design with the controller fully outside the workload boundary; the month-end threat model must call this out. Trusted production mediation is later work.

No async runtime, BEAM cluster, distributed queue, Cedar integration, microVM, secrets infrastructure, public endpoint, or model API is required this month.

## Suggested layout when the learner reaches M1-10

    capstone/
      Cargo.toml
      Cargo.lock
      src/lib.rs
      src/main.rs
      tests/
      README.md

Keep one package. Add modules only as the lessons require them. Use the Rust standard library first; serde_json and proptest arrive at their prescribed lessons. Any added crate needs a short reason and a pinned Cargo.lock.
