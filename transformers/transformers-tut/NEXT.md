# What remains

The brief is complete: 16 lessons (00–15, including the readiness review), two
appendices, glossary, bibliography, three stub labs with 24 tests, the `anatomy.py`
inspection tool, a transcript of 43 verified commands, and source checks. All listed
checks pass. Follow-ups, none blocking:

- Rendered browser verification was not performed; only structural checks ran.
- Lessons 02 (1,012 words) and 08 (1,065 words) are complete but on the short side of
  the 1,200–1,800 target; candidates for a worked batching example (02) and a
  GEGLU/ReGLU comparison (08).
- The links to `../../interpretability/interpretability-tut/index.html` warn until that
  course exists; `check_site.py` treats missing sibling `index.html` links as warnings.
- Lesson 14 has no runnable Llama/Qwen3 command because no such checkpoint is cached;
  if `Qwen/Qwen3-0.6B` is cached later, add a `names`-style command for it and verify
  the GQA/RMSNorm/RoPE claims against its config and activations.
- If package versions change, rerun `scripts/verify_commands.py` then `build.py` and
  `check_site.py`; lesson prose quotes specific numbers (3.05e-05, 108.9, 493 cache
  entries) that would need rechecking.
