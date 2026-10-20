# Next: divergence addendums

State as of 2026-06-12. Promoted from session memory so the plan lives with
the course.

The course is deliberately generic (operator's choice). The planned next step:
the operator supplies AmIEval-specific resources, and relevant pages get
**divergence addendums** - clearly marked insets showing where AmIEval
methodology departs from industry practice. Keep the generic text untouched so
the divergence points stay conceptually clear.

Editing rules that bind addendums too:

- `research/AUTHORING.md` is the binding style and provenance contract; every
  factual claim traces to verified source notes in `research/sources/*.json`.
- Mark insets visually distinct (likely a new callout class).
- Re-run the link/slug QA pattern (node one-liner checking nav paths, hrefs,
  data-g slugs) before committing.

Addendum source material lives in the workspace siblings: `evals/`
(METHODOLOGY.md, CONFLATION.md, thesis notes) and `bench/` +
`composable-beliefs/docs/run-manifest.md` (operational divergences: the
run-manifest as the only door, immutable measurements, append-only archive).
Direct hooks: AmIEval runs on Inspect (course page 24); run-manifest
immutability and the append-only archive map onto pages 19 (reproducibility)
and 26 (logs as artifacts). The methodology contracts themselves are
method:a1-a7 and c1-c11 in `belief-collections/method/`.

2026-10-20: Module 8 (Evaluating explanations, pages 27–29) added as the bridge
to interpretability per `ROADMAP.md`; source notes under `research/sources/`
(bills-neuron-explainer, huang-neuron-explanations, gao-sae, monosemanticity,
already-clean, gao-reply). The addendum plan above is unchanged.
