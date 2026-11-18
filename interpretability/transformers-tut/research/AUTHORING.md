# Authoring Transformer Anatomy

## Audience and outcome

Write for a programmer who has done the Python and linear-algebra courses, writes
Elixir and Rust at work, and is moving toward mechanistic interpretability. The
target is not fluency with a library but ownership of the object: the learner should
be able to write the forward pass, name every tensor and its shape, and locate any
activation in three libraries. Every lesson should end with the learner able to say
one more precise thing about a tensor.

Follow the statistics course's offline wiki conventions: cream reading surfaces,
serif text, searchable sidebar, glossary tooltips, previous/next navigation, no
external assets or requests. Static reading must work without JavaScript.

## Page requirements

Every lesson needs a worked mechanism or pencil example, an "In interpretability
work" box (class `evals`), a pitfall, a judgment question with a revealable
explanation, practice with an answer, and a sources box. Give each h2/h3 an ID.
Explain symbols immediately after a formula. Aim for 1,200–1,800 words; fewer
complete lessons beat more thin ones.

Pencil examples must be recomputable by hand (integers, powers of e, one sigmoid)
and must also be checked by a test in `labs/` or printed by `anatomy.py`.

## Terminal output is never invented

Lessons never contain typed-in output. Write `term([command])` for the command and
`out(command)` for its output; `out` copies the block for that exact command string
from `research/verify/lab-transcript.txt` at build time, and renders a placeholder
if the command has not been run. `scripts/verify_commands.py` collects every
`python ...` line in every `<pre class="term">`, runs it with the ML virtualenv's
interpreter, and writes the transcript with versions. `check_site.py` then rejects
any output line that is not in the transcript. The cycle is build, verify, build,
check. Commands that exercise learner stubs (`-m unittest`, `anatomy.py compare`
without `--reference`) are allowed to exit nonzero and are marked in the transcript.

Keep `anatomy.py` output deterministic: fixed seeds, CPU, `attn_implementation='eager'`,
no timing figures. If a command's output changes with package versions, the lesson
prose that quotes a number must be rechecked.

## Provenance

Mechanism explanations need no citation. Every architectural fact about a named
model (where a layer norm sits, which activation, head counts, tied embeddings,
parameter counts, which models use SwiGLU) must trace to a fetched source recorded in
`scripts/sources.py` and `research/source-checks.md`, or to the installed model's
config, state dict, or modeling source, with the command or file named. Never write a
number from memory of a paper. When sources disagree (GPT-2's 117M versus 124M), say
so and report what the weights support.

Library behaviour (TransformerLens hook names, nnsight ordering rules, the pre-affine
`hook_normalized`, the `[0]` on attention output) is verified by running the installed
package, and the run is in the transcript. Documentation is cited as support, not as
the evidence.

## Labs

Learner-facing lab files are stubs that raise `NotImplementedError` with the lesson
number. Tests import the stub, or the author's solution when `LAB_IMPL=reference`,
through `labs/_impl.py`. Tests needing torch or transformers skip with a message.
Reference solutions live only under `labs/reference/` and are used to generate
transcript output and to check the tests themselves. Held-out variant families are
described in `labs/ASSESSMENTS.md` and not published.

## Changes and checks

Edit the Python authoring sources, regenerate, verify, regenerate, check. Run the
lab tests with and without `LAB_IMPL=reference`. A structural check is not evidence
of rendered browser verification; report the distinction.
