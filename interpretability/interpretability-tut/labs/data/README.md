# Course corpus

`corpus.txt` is original prose written for this course on 2026-10-20: a fictional
archive note, a technical memo, a dialogue, a recipe, a society report, lecture
notes, a letter, a short glossary, a manifest, and a reflection. All names,
places, dates, and figures in it are invented. It is about 2,700 words and
tokenises to 3,270 GPT-2 tokens, which the labs cut into twenty-five 128-token
chunks: even chunks are the screening split (13 chunks), odd chunks are held out
(12 chunks). The split is positional and fixed, so every learner holds out the
same tokens.

The corpus is deliberately varied in surface form (numbers, quotes, list
numbering, newlines, capitalised names) so that simple token-level rules have
non-trivial base rates. It is small; a rule that holds here may not hold on code
or on web text, and the lessons say so.

No natural images ship with the course. Vision stimuli are rendered by
`labs/reference/vision_common.py` (arcs and lines on a grey field), and the one
image under `assets/img/` is a feature visualisation produced by
`labs/reference/feature_vis.py` from random noise. Total data under `labs/data/`
is under 20 KB.
