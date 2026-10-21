# Source checking and provenance

Checked on 2026-10-20. Every source below was fetched during authoring (with
`curl` into a scratch directory, converted to plain text, and searched; the
LessWrong and Alignment Forum posts through the site's GraphQL API because the
HTML endpoint refused the fetch). `sources.json` records each URL and the claim
scope that was checked. Quotations in the lessons are verbatim from the fetched
text; where a lesson shortens a sentence it uses an ellipsis or quotes a
substring, and nowhere does it alter words inside quotation marks. One
exception is typographic: the Bills et al. formula is quoted with ρ in place of
the page's LaTeX `$\rho$`.

## The 2026 essay and critique

- **Cammarata, "Neural Networks Are Already Clean"** (already-clean.goodfire.com).
  Fetched in full (about 199,000 characters of text). The page carries no
  publication date; secondary coverage dates it 15 October 2026 and the course
  does not assert a date. Verified passages: the header ("An informal research
  essay and working hypothesis"), "The Short Version", the Qwen3-32B audit
  sentence and its footnote on thresholds, the 1.7% sentence about the 2023
  OpenAI project, the 4e:55 passage, the "two ways to approach mechanistic
  interpretability" passage, the squeezed-mixed3b experiment and its SAE
  comparison, the table of ten curve detectors with preferred orientations and
  widths and its caption ("Tuning is the response at the centre of the image to
  a thin dark arc drawn at 180 angles and two curvatures"), the section "On
  Simulation Scores", the agent-written positive-control and distant-concept
  tests with their numbers (about 1%; 179 of 183), the "100 million tokens
  through one Qwen3-32B neuron" caption, the sentence promising a companion
  paper, and the Kimi K3 attribution-graph passage. The essay's numbers for
  Qwen3-32B and Kimi K3 are reported as the essay's estimates, not as
  independently verified, and the course runs nothing on either model.
- **Gao, "Neural networks are not already clean"** (LessWrong, posted
  2026-10-17T01:17 UTC per the API). Fetched in full through the GraphQL API
  (post body and footnotes, about 8,500 characters). Every Gao quotation in the
  lessons is from this text. The post contains no numeric results; none are
  claimed.

## Distill and Transformer Circuits

- **Olah et al. 2020, Zoom In.** Fetched (about 60,000 characters of text).
  Verified: the three claims, the seven arguments, the 4e:55 description, the
  superposition circuit and definition, "Feature visualization establishes a
  causal link, while dataset examples test the neuron's use in practice".
- **Cammarata et al. 2020, Curve Detectors.** Fetched (about 56,000 characters).
  Verified: the per-layer unit listing ("Layer 3b 10 neurons": 379, 406, 385,
  343, 342, 388, 324, 340, 330, 349), the "Each curve detector implements a
  variant of the same algorithm" paragraph, the 11% / pre-activation mean −200
  sentence for 3b:379, the 800-image hand-labelling and its four categories,
  the joint tuning curve method, the synthetic curve/angle/line experiments, the
  "wisps" sentence, "Curves are invariant to fill", the causality/generality/
  purity/family claims, and the "echoes" sentence about conv2d2. The article's
  model is the TensorFlow InceptionV1 used by Lucid; the course's model is
  torchvision's GoogLeNet, and lesson 06 reports that the unit numbers do not
  transfer.
- **Olsson et al. 2022, Induction Heads.** Fetched (about 124,000 characters).
  Verified: the behavioural definition on repeated random sequences, prefix
  matching and copying, the [A][B]…[A]→[B] sentence, the "continuum" remark, the
  six arguments, the phase-change claim, the in-context learning score. The
  article gives no numeric threshold for an induction head; the course's 0.5 is
  its own and is labelled so.
- **Bricken et al. 2023, Towards Monosemanticity.** Fetched (about 163,000
  characters). Verified: 512-neuron one-layer MLP, the summary of results, the
  human rubric medians (0 for neurons, 12 for features), the Arabic-script
  proxy correlation of 0.74 over 40 million tokens, the remark distinguishing
  their sampling from Bills et al.'s top-and-random mixture, "At present, we do
  not have any metric we trust more than human judgment of interpretability".

## OpenAI and arXiv

- **Bills et al. 2023.** The paper page loads its text from a JavaScript bundle;
  the bundle was fetched (2.7 MB) and searched. Verified strings: the
  explanation-score definition, the ρ scaling sentence and "explained variance
  at ρ²", "over 1,000 neurons with explanations that scored at least 0.8,
  meaning that according to GPT-4 they account for most of the neuron's
  top-activating behavior", the top-and-random description, and "correlation
  scores of 0.9 still lead to relatively low ablation scores on average (0.3
  for scoring on random-only text excerpts and 0.6 for top-and-random".
- **Huang et al. 2023, arXiv:2309.10312.** Fetched the arXiv HTML (about
  64,000 characters). Verified: the abstract, the observational and
  intervention modes, the precision/recall definitions, the 300-of-1.7k sample,
  the mean F1 0.56 (precision 0.64, recall 0.50) against a random baseline of
  zero, the 10-excerpt (5 top, 5 random) description of the GPT-4 score and the
  worked unfaithful-explanation argument, and the intervention-mode conclusion.
- **Gao et al. 2024, arXiv:2406.04093.** Fetched the arXiv HTML (about 93,000
  characters). Verified: TopK autoencoders, the 16 million latent / 40 billion
  token sentence, the three quality-metric categories, the downstream-loss
  definition, dead-latent mitigations, and the "10% of the pretraining compute"
  sentence.
- **Gorton 2024, arXiv:2406.03662.** Fetched the abstract page; verified title
  and author only. No result from it is asserted.

## Posts, curricula, tools

- **nostalgebraist 2020, logit lens.** Fetched through the LessWrong API.
  Verified the definition sentence, the "pretty good guess" sentence, the "some
  of what is going on, not all of it" caveat, the note that intermediate
  activations are taken after layer norm, and the later KL-is-not-a-metric
  addition.
- **Nanda 2025, How To Become A Mechanistic Interpretability Researcher.**
  Fetched through the Alignment Forum API (about 102,000 characters). Verified
  the quoted sentences on empiricism, GPT-2 Small, TransformerLens, ARENA
  Chapter 1.2, "The default state of the world is that your research is
  false", "Excitement is evidence of bullshit", and "Red-team your results
  relentlessly".
- **ARENA.** Fetched the ARENA_3.0 repository README. Verified the Chapter 1
  highlights (transformer from scratch, induction heads in a 2-layer model with
  TransformerLens, IOI in GPT-2 small, superposition and SAEs, steering vectors).
- **Neuronpedia.** Fetched the front page. Verified "Neuronpedia is an open
  source interpretability platform" and the listing of GPT2-Small residual
  stream SAE releases and the latent search. No feature page was fetched; the
  lesson describes a typical feature page in general terms and marks the
  lookup as optional.
- **torchvision GoogLeNet.** Verified from the installed package source
  (torchvision 0.29.1): the IMAGENET1K_V1 weight URL (googlenet-1378be20.pth),
  the recipe link to torchvision's classification reference, the
  transform_input flag, and by a forward pass the inception3b output shape.

## Original material

The corpus under `labs/data/` is original prose. All stimuli are rendered. The
feature-visualisation image is generated from noise. Every number quoted from a
run is in `research/verify/lab-transcript.txt`, produced by
`scripts/verify_commands.py` on the authoring machine; lessons quote that
transcript and nothing else for local results. General explanations (what a
probe is, what patching does) are written independently and cite sources where
a method or an attributed claim is introduced.

## Not found or not used

The course searched for and found both the 2026 essay and the critique; no
claim rests on secondary coverage. No feature page on Neuronpedia was fetched.
No result is quoted from the essay's promised companion paper or from Gao's
promised follow-up post, neither of which existed on the checking date.
