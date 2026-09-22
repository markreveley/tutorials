# Networking for LLM Evals

A beginner wiki-course for discussing, designing, and navigating evaluation infrastructure. Open **index.html** directly in a browser. No server, install, account, or Internet connection is required for the course itself. External reading links need Internet access.

The design extends the supplied `evals/domains/evals/evals-tut` reference: cream surfaces, serif reading text, searchable sidebar, glossary tooltips, linked lessons, source notes, and previous/next navigation.

## Included

- 24 lessons across 8 modules, with original scenarios, diagrams, and revealable reasoning checks.
- 87 glossary entries with first-mention links and keyboard-focus tooltips.
- Three local calculators: IPv4 ranges, transfer serialization, and average in-flight work.
- Command reference, focused textbook reading map, annotated primary-source bibliography.
- A loopback-only Python lab for HTTP errors, deadlines, retries, and partial streams.

Start at lesson 00. Lessons 19–20 provide practice; lesson 23 supplies a design brief and readiness rubric. The target is networking fluency for eval work, not a comprehensive network-operations certification.

## Lab

From this directory:

```sh
python3 labs/server.py
```

In another terminal, follow lesson 19. The server binds `127.0.0.1:8765`, makes no external requests, and retains only experiment counters in memory. Stop with Ctrl-C. Use `--port 8766` if necessary and update your client URLs. Python 3 and curl are required only for these exercises.

## Editing and checks

The delivered pages are plain HTML/CSS/JavaScript and work with `file://`. The Python scripts are authoring tools, not runtime dependencies. Edit prose in `scripts/course_content.py`, reference pages in `scripts/reference_pages.py`, and glossary entries in `scripts/make_glossary.py`, then regenerate:

```sh
python3 scripts/make_glossary.py
python3 scripts/build.py
python3 scripts/check_site.py
python3 -m unittest discover -s labs -p 'test_*.py' -v
node scripts/check_calculators.js
```

The structural check covers internal page/asset links, fragments, navigation, glossary references, heading IDs, and expected lesson structure. Lab checks use real loopback HTTP requests, including work that completes after a caller times out. They do not establish behavior of external providers.

## Sources

The foundation is *Computer Networks: A Systems Approach*, Larry Peterson and Bruce Davie, online 7.0-dev edition, with protocol specifications and official infrastructure documentation. See `bibliography.html` for attribution and `research/source-checks.md` for the verification scope. Scenarios and numeric examples are original and hypothetical. No model-provider quotas or prices are asserted.

No hosting or publication was performed. Browser-based visual verification was unavailable in the authoring session.
