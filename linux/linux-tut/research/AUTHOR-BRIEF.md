# Author brief (linux-tut)

You are writing pages of the course **Linux for Evals Engineers** at
`/Users/mark/dev/repos/_do/evals/courses/linux/linux-tut/`. Your prompt names your pages.

## Read first, in this order

1. `research/AUTHORING.md` — the binding contract (template, components, provenance, voice, labs). All of it.
2. `research/PAGE-BRIEFS.md` — the intro ("recurring teaching devices") and the briefs for YOUR pages; skim the
   one-line "Job:" of every other page so you know what is taught where and can cross-link instead of re-teaching.
3. `assets/nav-data.js` — exact titles and paths (for cross-links and your `<title>`/kicker).
4. `index.html` — the course's framing and voice. And ONE model page from the sibling course for
   house style: `../../evals/evals-tut/pages/11-evaluating-agents.html`.
5. `research/wordfreq-bench/README.md` if any of your pages touches the running example.
6. The source notes listed under "Sources:" in each of your briefs: `research/sources/<id>.json`.
   Read the `claims` (use `finding`, respect `verdict`), `extra_findings`, and `teaching_notes`.
   `ls research/sources/` — if a listed note is missing, the fact is unavailable: write around it
   or verify it yourself per AUTHORING.md rule 4 (fetch the primary source, append the claim to a note).

**Also read the Addendum at the end of AUTHORING.md** (conventions adopted from the sibling networking
course: a `.check` box on every page, failure accounting, evidence-vs-hypothesis, depth triage,
and the division of labour with `../../networking/networking-tut`).

## Then, per page

1. **Run everything first.** Work out the page's terminal material in Docker before writing
   prose; save the raw sessions to `research/verify/<page-file-stem>.txt`. The page shows what
   really happened. If reality contradicts the brief (it will, somewhere), reality wins — teach
   what you observed and mention the discrepancy in your final report. Container names
   `lt-<page-number>-…`; remove them when done. Run permission demos as a real non-root user.
   Do not start anything that could hurt the host: no fork bombs without `--pids-limit`, no
   memory hogs without `--memory`, no `--privileged` containers with host mounts, never touch
   other agents' containers, never prune.
2. **Write the page** to the path in nav-data.js, following the template exactly. 1,300–2,300
   words of prose for course pages. Every page: ≥1 `.evals` box (concrete!), ≥1 pitfall/warn,
   ≥1 diagram or fully worked terminal example, one `.check` judgment question, a `.lab` with 3–6 exercises with verified
   solutions, a `.srcbox`. 6–15 glossary terms marked (first mention only; canonical slugs only).
3. **Cite** every fact-about-the-world with the note's `tag` and URL; list them in the srcbox.
   Executed mechanics need no citation. No numbers/defaults/incident details from memory.
4. **Escape** `<`, `>`, `&` in all code. Give every h2/h3 an id.
5. **Check**: `node research/qa.js 2>&1 | grep "<your-file-name>"` must print nothing for your
   pages (links to pages other authors are still writing will show as broken until they land —
   those are fine as long as the path matches nav-data.js; everything else must be clean).
   Run `shellcheck` on every script you show.

## Style reminders that matter most

- Teach the model (fds, the process tree, the mount table, the routing table, the permission
  decision procedure), then the command that reads it. Few commands, deeply.
- The through-line is evals. A reader should finish each page able to say what this mechanism does
  to the *validity* or *integrity* of an agentic eval. If a section has no such consequence, shorten it.
- Entry-level reader on a Mac. Define jargon at first use. Anticipate confusion out loud.
- Terminal blocks: `<pre class="term"><code>…</code></pre>` with `<span class="p">$</span>` prompts
  (`#` when root) and `<span class="o">…</span>` around output. Trim long output with `…`.
- Don't pad. Don't moralise. No "in today's fast-moving AI landscape".

## Final report (≤15 lines)

Files written, word counts, anything in the brief that reality contradicted, any claim you
wanted but could not source (so the editor knows what was left out), any note you appended to.

## Known quirks of THIS authoring machine (found during research — do not teach them as Linux facts)

- Docker Desktop's daemon here runs with seccomp `Profile: unconfined`: a default container shows
  `Seccomp: 0`. To demonstrate Docker's real default profile use `--security-opt seccomp=builtin`
  (`Seccomp: 2`), and tell the reader a stock Linux Docker Engine shows 2 by default.
- No AppArmor in the Docker Desktop VM — describe, don't demo.
- A fresh network namespace here also contains fallback tunnel devices (`tunl0`, `gre0`, `sit0`…)
  beside the DOWN `lo` (kernel sysctl `fb_tunnels_only_for_init_net`). Trim or explain.
- Storage driver here is the containerd snapshotter (`overlayfs`), not `overlay2`; see overlayfs note.
- The host is an Apple Silicon Mac: images are `linux/arm64`, `uname -m` prints `aarch64`.
- cgroup limits are invisible to `/proc`: `nproc`/`free` show the VM's totals inside a limited container.
- macOS has no `timeout`, no `/proc`; its `sed -i` differs. Always run course commands in a container.
