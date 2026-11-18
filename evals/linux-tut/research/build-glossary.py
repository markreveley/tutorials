#!/usr/bin/env python3
"""Assemble assets/glossary-data.js from research/gloss-part*.json.
Checks every slug against the canonical list in AUTHORING.md. Usage: python3 research/build-glossary.py"""
import glob, json, os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
canon = set()
in_list = False
for line in open(os.path.join(here, "AUTHORING.md"), encoding="utf-8"):
    if line.startswith("### Canonical glossary slugs"):
        in_list = True
        continue
    if in_list and line.startswith("## "):
        break
    if in_list:
        canon.update(re.findall(r"`([a-z0-9-]+)`", line))

merged = {}
for path in sorted(glob.glob(os.path.join(here, "gloss-part*.json"))):
    for slug, entry in json.load(open(path, encoding="utf-8")).items():
        if slug in merged:
            sys.exit(f"duplicate slug {slug} in {path}")
        merged[slug] = entry

problems = []
for slug in sorted(canon - set(merged)):
    problems.append(f"missing entry: {slug}")
for slug in sorted(set(merged) - canon):
    problems.append(f"non-canonical entry: {slug}")
for slug, e in merged.items():
    for key in ("name", "short", "def"):
        if not e.get(key):
            problems.append(f"{slug}: empty {key}")
    if "<" in e.get("short", ""):
        problems.append(f"{slug}: HTML in short")
    for ref in e.get("see", []):
        if ref not in canon:
            problems.append(f"{slug}: see -> unknown slug {ref}")
ordered = {s: merged[s] for s in merged}
out = os.path.join(here, "..", "assets", "glossary-data.js")
with open(out, "w", encoding="utf-8") as f:
    f.write("// Glossary data (generated from research/gloss-part*.json by research/build-glossary.py — edit those and rerun).\n")
    f.write("// Each entry: slug -> { name, short, def, also?, see? }\n")
    f.write("window.GLOSSARY = " + json.dumps(ordered, ensure_ascii=False, indent=2) + ";\n")
print(f"{len(merged)} entries ({len(canon)} canonical slugs) -> assets/glossary-data.js")
for p in problems:
    print("  PROBLEM", p)
sys.exit(1 if problems else 0)
