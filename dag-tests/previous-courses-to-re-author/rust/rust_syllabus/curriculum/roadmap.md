# Continuing roadmap

Month one is the first 30 sessions of one integrated path. Later material is preserved here as a resource and capability map; it is not yet a timed lesson prescription.

| Stage | Capability | Retained resources and conditional depth |
|---|---|---|
| Month one | Explain, execute, observe, and constrain a local process | Selected Linux Journey and Bandit, Rust Book ownership/errors/lifetimes/concurrency, primary Linux and Rust manuals, initial proptest |
| Remaining foundations | Explain the host/guest boundary and boot an isolated workload | Firecracker design/jailer/docs, Fly engineering, cgroups v2, namespaces, seccomp; compare Cloud Hypervisor and Kata; WireGuard and eBPF basics; continue Linux Journey/Bandit |
| Rust follow-through | Review concurrent interfaces and know tool limits | Rust Book smart pointers/Send/Sync/async; Kani, Miri, Loom when a specific verification question warrants them; Rust for Rustaceans only for API design |
| Distributed execution | Model retries, delivery, ownership of work, and recovery | DDIA second edition, Rust Maelstrom challenge, selected Jepsen and Marc Brooker; MIT 6.5840 and TLA+ as budgeted extensions |
| Workload identity | Bootstrap trust, issue authority, rotate credentials, and recover from compromise | SPIFFE/SPIRE, Secret Colors on-ramp, Real-World Cryptography as an addition; capability security; attestation/SEV-SNP/TDX and proxy re-encryption at the depth the threat model requires |
| Supervision | Recover and bound concurrent work | Elixir in Action or Designing Elixir Systems with OTP if the architecture chooses BEAM; BEAM Book internals only when operational needs justify them |
| Action gating | Enforce permissions outside the untrusted workload | Cedar as the implementation spine, OPA comparison, Guardrails for Agentic AI as supporting material once availability is confirmed; Anthropic architecture readings |
| Evidence and evaluation | Correlate events, analyze errors, and measure task quality | Observability Engineering, Learning OpenTelemetry, current GenAI conventions, Langfuse/Phoenix and Collector/ClickHouse comparison, Husain/Shankar materials and Evals for AI Engineers |
| Short model-literacy module | Interpret post-training and benchmark claims | About one week of bounded lessons on SFT, RLHF/DPO, RL with verifiable rewards, and evaluation limits; no deep ML track |
| Inference, when required | Serve and measure a customer's model workload | AI Engineering, Stas Bekman's open book, Geiping's 2026 seminar, vLLM and SGLang; GPU rental only with a concrete budget and authorization |

The paid evals course remains conditional on having live traces and a reason to spend the money. Certification prep remains excluded. Later resource links, versions, availability, and selected sections must be reverified when those lessons are authored; this document does not claim a fresh audit of the full original bibliography.
