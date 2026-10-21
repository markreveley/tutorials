# NEXT

State on 2026-10-20 at hand-off. The course is complete at the level the brief
asked for: 16 lessons (15 numbered plus the readiness review), three
appendices, six labs with 37 tests, reference implementations, a verified
transcript, and source checks. Everything below is optional extension, not
unfinished work.

- **Downstream-KL scoring (lesson 14, section "The extension the 2026 debate
  asks for").** Designed in prose; no reference script. A `labs/reference/kl_score.py`
  that substitutes rule-predicted activations for one neuron and reports KL
  against mean-ablation and random-neuron controls would let lesson 13's
  Gao/Cammarata disagreement be tested on L2/2928.
- **Copying score for induction heads (lesson 11 practice).** The reference
  detector tests prefix matching only. Adding per-head direct logit attribution
  to the attended token would complete the Olsson et al. definition.
- **Dataset-examples line of evidence for the vision replication (lesson 07
  "not tested" table).** Needs natural images with a clear licence; the course
  ships none. With a small licensed set, the purity claim could be tested.
- **Per-head patching (lesson 10).** The residual-stream table shows the country
  information moving between layers 8 and 10; `hook_z` patching per head would
  name the heads. Assessment family E already asks a learner for this.
- **Rendered browser verification.** check_site validates structure, links,
  and nesting; no page was opened in a browser during authoring.
- **Sibling links.** All five sibling `index.html` targets existed at the final
  check; check_site reports them as notes rather than failing if one is renamed.
