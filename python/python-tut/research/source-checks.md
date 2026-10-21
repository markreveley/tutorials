# Source checking and provenance

Checked on 2026-10-20 by fetching each page. `sources.json` records each URL and
the specific claim scope that was checked. This is not a claim that every
statement in each source was validated. External links need Internet access;
the course and its labs do not.

## Pages inspected

- Python language reference, data model §3.1: identity, type, value;
  immutability by type.
- Python library reference: `json` (duplicate names keep the last value by
  default; `object_pairs_hook`; `JSONDecodeError` attributes), `unittest`
  (discover, `-s`, `-p`, `subTest`, `assertRaises` as context manager),
  `dataclasses` (generated methods, `frozen`, mutable-default `ValueError`,
  `default_factory`).
- NumPy user guide, broadcasting rules; NumPy reference, `numpy.einsum`
  (summation of repeated labels, explicit mode, examples).
- PyTorch 2.14 notes: broadcasting semantics (including the in-place
  restriction), autograd mechanics (recording rule, leaf `.grad`, no-grad
  mode, in-place caveats), reproducibility (`manual_seed`, no cross-platform
  guarantee, deterministic algorithms); tensor views page; `torch.nn.Module`
  reference (`register_forward_hook` signature and handle, `state_dict`,
  `named_parameters`). The unversioned `docs.pytorch.org/docs/stable/...`
  URLs redirected to `2.14`, which matches the installed torch 2.14.1+cpu;
  the `2.14` URLs are the ones recorded.
- Transformers documentation: model outputs (ModelOutput behaviour,
  `hidden_states` description, last-hidden-state normalisation caveat) and
  GPT-2 (config defaults, `GPT2LMHeadModel.forward` return shapes).
- TransformerLens documentation "Migrating to TransformerLens 4.0" and the
  GitHub releases page for 4.0.0 to 4.2.0. The migration page confirms the
  removal of the Hooked stack, `TransformerBridge.boot_transformers`, and what
  `enable_compatibility_mode()` does. It does not state that cache keys such as
  `blocks.5.hook_resid_post` keep working; that was verified locally with
  transformer_lens 4.2.0 and is recorded in the transcript (lesson 14).
- nnsight documentation: "Getting activations" and the Tracer page. The
  examples there use `TransformersModel`; the course uses `LanguageModel`,
  which is its subclass in the installed nnsight 0.8.1 (checked in the
  package source). The out-of-order error and the file-or-cell requirement
  for `trace` were observed locally, not read from the documentation.
- Hugging Face safetensors documentation index: purpose, `save_file`,
  `safe_open`.

## Not fetched

- The original nnsight walkthrough URL returned 404; the two pages above were
  used instead.
- No papers are cited. The course makes no empirical claims about models
  beyond what its own transcript shows for GPT-2 small on the stated prompt.

## Original material

All example scripts, prompts, tests, exercises and explanations are original.
Numbers in the lessons (token ids, probabilities, norms, differences between
toolkits, file sizes) come from the recorded run in
`research/verify/lab-transcript.txt` and are pasted from it by the build, not
typed.
