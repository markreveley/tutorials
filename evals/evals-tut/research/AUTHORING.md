# Authoring Guide — eval-tut

This is the binding contract for every page in the course. Read all of it before writing.

## The audience

Entry-level: a working software engineer or technical PM who has used ChatGPT/Claude and maybe called an LLM API, but has **no background in ML evaluation and no statistics beyond high school**. Every piece of jargon gets defined at first use. Every mathematical idea is either explained inline in plain language or linked to the appendix that teaches it.

## The cardinal rule: provenance

**Every factual claim — every number, finding, position, and quote — must trace to a verified source note in `research/sources/*.json`.** Those files contain claims checked against the actual papers/docs. Rules:

1. If the source note marks a claim `confirmed`, you may state it, with the verified numbers, and cite it.
2. If marked `corrected`, use ONLY the corrected version.
3. If marked `unverifiable`, do not state it as fact. Either omit it or explicitly flag it ("the authors report… (not independently verified)").
4. Never add numbers or findings from your own memory of a paper. If it's not in the notes, it's not in the course.
5. General explanatory material (what a mean is, how an HTTP request works, what a unit test is) needs no citation. Specific empirical findings always do.

## Citations

- Inline: superscript link right after the claim:
  `<a class="cite" href="https://arxiv.org/abs/2306.05685" title="Zheng et al. 2023, Judging LLM-as-a-Judge">[MT-Bench]</a>`
  Use the short tag names: [Evals Book], [Evals FAQ], [Husain, Evals], [Husain, Judge], [EvalGen], [MT-Bench], [Self-Pref], [Yan], [Agents That Matter], [SWE-bench], [SWE-bench Verified], [SWE-bench+], [GAIA], [tau-bench], [WebArena], [OSWorld], [Terminal-Bench], [AgentBench], [METR], [Inspect], [Error Bars], [HumanEval], [Eleuther], [GSM1k], [LiveBench], [LiveCodeBench], [ARC-AGI], [Leaderboard Illusion], [BIG-bench], [Anthropic], [Bills], [Huang], [Gao SAE], [Monosemanticity], [Already Clean], [Gao reply]
- End of page: a `.srcbox` listing every source used on the page with full citation and link (see template).

## Page template

Every page uses exactly this skeleton. Pages live in `pages/` (appendices in `appendices/`); asset paths are `../assets/...`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PAGE TITLE · Understanding LLM Evals</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<div class="layout">
  <aside class="sidebar" data-nav></aside>
  <div class="content">
  <main class="page">

    <p class="kicker">Module N · Module Name</p>
    <h1>Page Title</h1>
    <p class="lede">One or two sentences: what this page teaches and why the reader should care. Written to be readable on its own.</p>

    <!-- body -->

    <div class="srcbox">
      <span class="label">Sources for this page</span>
      <ul>
        <li>Zheng et al., “Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena,” NeurIPS 2023. <a href="https://arxiv.org/abs/2306.05685">arxiv.org/abs/2306.05685</a></li>
      </ul>
    </div>

  </main>
  </div>
</div>
<script src="../assets/nav-data.js"></script>
<script src="../assets/glossary-data.js"></script>
<script src="../assets/wiki.js"></script>
</body>
</html>
```

Notes:
- Sidebar and prev/next links are injected by `wiki.js` — do not write them by hand.
- Give every `h2`/`h3` an `id` (kebab-case) so anchors work.
- Index page (`index.html`) and `glossary.html`/`bibliography.html` use the same skeleton but with `assets/...` paths (no `../`).

## Components (use them, don't invent new ones)

- `<div class="keyidea"><span class="label">Key idea</span> …</div>` — the one takeaway of a section. ≤1 per major section.
- `<div class="callout"><span class="label">Why this matters / Background / Example</span> …</div>` — blue, neutral asides.
- `<div class="warn"><span class="label">Caveat</span> …</div>` — amber, limitations and caveats.
- `<div class="pitfall"><span class="label">Pitfall</span> …</div>` — red, mistakes practitioners actually make.
- `<div class="card">…</div>` — grouped material, e.g. a worked example or checklist.
- `<div class="diagram">ASCII diagram</div>` — monospace, preserved whitespace. Use real ASCII art for pipelines/architectures; keep ≤72 cols.
- `<div class="math">…</div>` — display math (see Math below).
- Tables for enumerable comparisons; explain implications in prose around them.
- `<figure>` + `<figcaption>` around diagrams when a caption helps.

## Math (no MathJax — plain HTML)

The site has no external dependencies. Write math with HTML:
- Variables italic by default inside `.math` (it sets italic); use `<span class="plain">…</span>` for words.
- Subscripts/superscripts: `x<sub>i</sub>`, `σ<sup>2</sup>`.
- Use real Unicode: σ, μ, Σ, √, ≈, ≤, ×, − (minus sign, not hyphen).
- Binomial coefficients: write `C(n, k)` in body text; in display math you may use a fraction-free form, e.g. `1 − C(n−c, k) / C(n, k)`.
- Every formula must be immediately followed by a plain-English sentence saying what it means, and a link to the relevant appendix on first use: e.g. `(new to standard errors? See <a href="../appendices/b-sampling.html">Appendix B</a>)`.

## Glossary terms

First meaningful mention of a glossary concept on a page gets marked:
`<span class="term" data-g="standard-error">standard error</span>`
— this renders a dashed underline with a hover tooltip. Mark only the first mention per page; afterwards use plain text. Use ONLY slugs from the canonical list below (the glossary file defines exactly these). Don't mark words inside headings, lede paragraphs, or links.

### Canonical glossary slugs

Foundations: `eval`, `benchmark`, `metric`, `dataset`, `sample`, `trace`, `harness`, `grader`, `ground-truth`, `reference-based`, `reference-free`, `offline-eval`, `online-eval`, `capability-eval`, `product-eval`, `golden-dataset`, `train-test-split`, `regression-testing`, `guardrail`, `a-b-test`, `leaderboard`, `arena-rating`, `human-baseline`, `llm`, `token`, `temperature`, `context-window`, `prompt`, `system-prompt`, `fine-tuning`, `rag`, `hallucination`

Process: `error-analysis`, `open-coding`, `axial-coding`, `failure-mode`, `failure-taxonomy`, `theoretical-saturation`, `criteria-drift`, `principal-domain-expert`, `critique-shadowing`, `binary-judgment`, `likert-scale`, `annotation`, `inter-annotator-agreement`, `synthetic-data`, `eval-driven-development`

Judges: `llm-as-judge`, `pairwise-comparison`, `single-answer-grading`, `rubric`, `position-bias`, `verbosity-bias`, `self-enhancement-bias`, `self-preference`, `self-recognition`, `chain-of-thought`, `few-shot`, `reference-guided-grading`, `judge-alignment`, `g-eval`, `model-graded-scorer`

Agents: `agent`, `trajectory`, `tool-call`, `environment`, `outcome-based-evaluation`, `process-based-evaluation`, `user-simulation`, `pass-hat-k`, `state-based-evaluation`, `sandbox`, `scaffold`, `elicitation`, `time-horizon`, `cost-controlled-evaluation`, `pareto-frontier`, `holdout-set`, `overfitting`

Statistics: `random-variable`, `expectation`, `variance`, `standard-deviation`, `standard-error`, `central-limit-theorem`, `confidence-interval`, `clustered-standard-errors`, `paired-comparison`, `hypothesis-test`, `null-hypothesis`, `p-value`, `statistical-power`, `type-i-error`, `type-ii-error`, `pass-at-k`, `unbiased-estimator`, `bootstrap`, `binomial-distribution`, `bernoulli-trial`, `spearman-correlation`, `cohens-kappa`, `confusion-matrix`, `precision`, `recall`, `true-positive-rate`, `true-negative-rate`, `f1-score`, `sample-size`, `effect-size`, `independence`

Contamination & validity: `contamination`, `memorization`, `construct-validity`, `internal-validity`, `external-validity`, `data-leakage`, `solution-leakage`, `canary-string`, `private-holdout`, `live-benchmark`, `training-cutoff`, `n-gram-overlap`, `log-likelihood`, `saturation`

Tooling: `tracing`, `span`, `observability`, `assertion`, `solver`, `scorer`, `epoch`, `experiment`, `faithfulness`, `answer-relevancy`, `context-precision`, `context-recall`

Interpretability (Module 8): `neuron`, `activation`, `neuron-explanation`, `simulation-scoring`, `max-activating-examples`, `polysemanticity`, `control-neuron`, `permutation-test`, `intervention`, `sae-feature`, `sparse-autoencoder`

## Voice

- Plain, direct, confident. Second person where natural ("when you review traces…").
- Teach **derived rules, not memorized ones**: always show *why* a practice exists, so the reader can re-derive it when their situation breaks the pattern. ("Binary judgments beat Likert scales" is a memorized rule; "judges and humans can't agree on what a 4-vs-5 means, and disagreement you can't resolve is noise in your metric" is a derived one.)
- Numbers are precious: when you cite a finding, give the actual number and what was measured, not "significantly better."
- Anticipate the entry-level reader's confusion explicitly ("If you're wondering why we can't just…").
- No hype, no filler, no "in the rapidly evolving landscape of AI."
- En-dashes/em-dashes fine; section headings in sentence case.
- Each page: roughly 1,200–2,200 words of body prose (appendices may be shorter), at least one diagram or worked example, at least one pitfall or caveat box.
- Cross-link generously to other pages (relative hrefs) and appendices.

## Quality bar for examples

Worked examples must be fully worked: real (toy) numbers carried through every step to the final answer. A reader should be able to recompute every number with a pencil. Code snippets must be runnable as shown (Python preferred, stdlib only unless illustrating a named tool).
