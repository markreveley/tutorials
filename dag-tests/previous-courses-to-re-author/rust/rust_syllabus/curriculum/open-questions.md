# Open questions

These are unresolved requirements, not completed research findings.

| Question | Resolve by | Evidence required |
|---|---|---|
| Does the prescribed local Ubuntu VM meet the current Linux lesson's requirements? | Create it in M1-04; check each later lesson's own preflight when reached | Only the current lesson's tools and observed capabilities; no M1-01 Linux planning task |
| Is the customer's host administrator trusted? | M1-02 initial assumption; revisit before confidential computing | Explicit threat model and customer requirement |
| What does sovereign deployment mean for the product? | M1-02 | Control of hardware, updates, keys, telemetry, data location, and recovery |
| Which existing offerings document installation on customer hardware? | M1-02 | Dated primary-source comparison; unknowns distinguished from negative findings |
| How does the product relate to Fly.io's existing Sprites branding and service? | M1-02 | Clarify whether the term names that service, an integration, or a distinct product |
| Is KVM available on the intended next-stage host? | Before a future microVM implementation lesson | That future lesson's host check; M1-30 identifies this prerequisite but does not assign setup |
| Does the required virtualization stack support the needed attestation and future GPU arrangement? | Before committing to that architecture | Version-specific support evidence and a small compatibility experiment |
| Will the control plane actually use BEAM? | Before scheduling deep OTP work | Partnership architecture decision |
| Which code and evidence may be public? | Before remote publication | User/partnership decision and sanitized examples |
| Which measurable product promises matter first? | M1-02 and M1-30 | Chosen invariants, acceptance examples, and known limits |

Prescribed environment: the learner's Mac, with a local Multipass Ubuntu 24.04 VM created at M1-04. Each lesson has its own preflight. Neither the instructions nor this default are evidence that the VM has been created or that its experiments have passed.
