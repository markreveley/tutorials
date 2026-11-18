#!/usr/bin/env python3
"""Validate the curriculum, show progress, or open an unassessed lesson attempt."""
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LESSON_STATES = {"not_started", "in_progress", "needs_review", "blocked", "completed"}
CAPABILITY_STATES = {
    "not_assessed", "introduced", "practiced_with_assistance",
    "demonstrated_independently", "needs_review",
}
ASSESSMENTS = {"not_attempted", "assisted", "passed", "needs_review"}
ASSISTANCE = {"not_recorded", "independent", "hints", "agent_implemented"}


def read_json(relative):
    return json.loads((ROOT / relative).read_text())


def local_path(relative):
    value = Path(relative)
    if value.is_absolute():
        raise ValueError(f"Evidence path must be repository-relative: {relative}")
    resolved = (ROOT / value).resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError(f"Path leaves the repository: {relative}")
    return resolved


def lesson_section(lesson, heading):
    content = local_path(lesson["path"]).read_text()
    match = re.search(
        rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)",
        content, re.MULTILINE | re.DOTALL,
    )
    if match is None or not match.group(1).strip():
        raise ValueError(f"{lesson['id']}: missing or empty section {heading}")
    return match.group(1).strip()


def validate():
    manifest = read_json("curriculum/manifest.json")
    progress = read_json("curriculum/progress.json")
    resources = read_json("curriculum/resources.json")
    resource_ids = {entry["id"] for entry in resources}
    lessons = manifest["lessons"]
    expected_ids = [f"M1-{number:02d}" for number in range(1, 31)]
    if [entry["id"] for entry in lessons] != expected_ids:
        raise ValueError("Manifest must contain M1-01 through M1-30 in order")
    if set(progress["lessons"]) != set(expected_ids):
        raise ValueError("Progress lesson IDs do not match the manifest")
    if len(resource_ids) != len(resources):
        raise ValueError("Duplicate resource IDs")
    seen = set()
    for entry in lessons:
        lesson_id = entry["id"]
        if not set(entry["prerequisites"]).issubset(seen):
            raise ValueError(f"{lesson_id}: unknown, forward, or cyclic prerequisite")
        seen.add(lesson_id)
        if not isinstance(entry.get("concept"), str) or not entry["concept"].strip():
            raise ValueError(f"{lesson_id}: missing concept focus")
        if not set(entry["resources"]).issubset(resource_ids):
            raise ValueError(f"{lesson_id}: unknown resource")
        if not set(entry["capabilities"]).issubset(progress["capabilities"]):
            raise ValueError(f"{lesson_id}: unknown capability")
        document = local_path(entry["path"])
        if not document.is_file():
            raise ValueError(f"{lesson_id}: missing lesson document")
        content = document.read_text()
        for heading in [
            "## Concept", "## Starting state", "## Today's path",
            "## Predict before reading",
            "## Prescribed reading, in order", "## Exercise",
            "## Required artifacts and commit", "## Exit criteria",
            "## Independent understanding check", "## Recovery if unfinished",
            "## Optional extension",
        ]:
            if heading not in content:
                raise ValueError(f"{lesson_id}: missing section {heading}")
        if not lesson_section(entry, "Concept").startswith(f"**{entry['concept']}.** "):
            raise ValueError(f"{lesson_id}: concept does not match manifest")
        lesson_section(entry, "Predict before reading")
        delivery = entry.get("delivery", "document")
        if delivery not in {"document", "agent-led"}:
            raise ValueError(f"{lesson_id}: invalid delivery mode")
        steps = entry.get("steps", {})
        if delivery == "agent-led":
            if not isinstance(steps, dict) or not steps:
                raise ValueError(f"{lesson_id}: agent-led delivery needs ordered steps")
            for step, heading in steps.items():
                if not isinstance(step, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", step):
                    raise ValueError(f"{lesson_id}: invalid step ID")
                if not isinstance(heading, str) or not re.search(
                    rf"^#{{2,3}} {re.escape(heading)}$", content, re.MULTILINE
                ):
                    raise ValueError(f"{lesson_id}: step {step} has no lesson heading")
        state = progress["lessons"][lesson_id]
        if state["status"] not in LESSON_STATES:
            raise ValueError(f"{lesson_id}: invalid status")
        if state["status"] == "not_started" and state["attempts"]:
            raise ValueError(f"{lesson_id}: not_started conflicts with attempt history")
        for attempt in state["attempts"]:
            if not local_path(attempt["session"]).is_file():
                raise ValueError(f"{lesson_id}: missing attempt record")
            date.fromisoformat(attempt["date"])
            if attempt["independent_check"] not in ASSESSMENTS:
                raise ValueError(f"{lesson_id}: invalid independent check")
            if attempt["assistance"] not in ASSISTANCE:
                raise ValueError(f"{lesson_id}: invalid assistance value")
            if "step" in attempt and (
                delivery != "agent-led"
                or not isinstance(attempt["step"], str)
                or attempt["step"] not in steps
            ):
                raise ValueError(f"{lesson_id}: invalid saved step")
            # Preserve optional elapsed-time observations in older records.
            minutes = attempt.get("minutes")
            if minutes is not None and (type(minutes) is not int or minutes <= 0):
                raise ValueError(f"{lesson_id}: invalid actual minutes")
            for evidence in attempt["evidence"]:
                if not local_path(evidence).exists():
                    raise ValueError(f"{lesson_id}: missing evidence {evidence}")
        if state["status"] == "completed":
            if not state["attempts"]:
                raise ValueError(f"{lesson_id}: completion requires an attempt")
            latest = state["attempts"][-1]
            if latest["independent_check"] != "passed" or not latest["evidence"]:
                raise ValueError(f"{lesson_id}: completion requires an independent pass and evidence")
            if latest["assistance"] == "not_recorded":
                raise ValueError(f"{lesson_id}: completion requires assistance level")
            for dependency in entry["prerequisites"]:
                if progress["lessons"][dependency]["status"] != "completed":
                    raise ValueError(f"{lesson_id}: prerequisite {dependency} is not completed")
    known_sessions = {
        attempt["session"]
        for state in progress["lessons"].values()
        for attempt in state["attempts"]
    }
    for capability, state in progress["capabilities"].items():
        if state["status"] not in CAPABILITY_STATES:
            raise ValueError(f"{capability}: invalid capability status")
        if state["status"] != "not_assessed" and not state["evidence"]:
            raise ValueError(f"{capability}: an assessed status needs evidence")
        for evidence in state["evidence"]:
            if evidence not in known_sessions or not local_path(evidence).is_file():
                raise ValueError(f"{capability}: evidence must identify a recorded session")
        if state["status"] == "demonstrated_independently":
            related = [x for x in lessons if capability in x["capabilities"]]
            passed_sessions = {
                attempt["session"]
                for entry in related
                for attempt in progress["lessons"][entry["id"]]["attempts"]
                if attempt["independent_check"] == "passed"
            }
            if not set(state["evidence"]) & passed_sessions:
                raise ValueError(f"{capability}: no relevant independent pass")
    check_local_links()
    return manifest, progress


def check_local_links():
    for document in ROOT.rglob("*.md"):
        if any(part in {".git", "target", ".venv", "scratch", "local"} for part in document.relative_to(ROOT).parts):
            continue
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text()):
            if "://" in target or target.startswith("mailto:") or "{{" in target:
                continue
            path, _, fragment = target.partition("#")
            destination = (document.parent / unquote(path)).resolve() if path else document
            if not destination.exists():
                raise ValueError(f"{document.relative_to(ROOT)}: broken local link {target}")
            if fragment and destination.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", destination.read_text(), re.MULTILINE)
                anchors = {
                    re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
                    for heading in headings
                }
                if fragment not in anchors:
                    raise ValueError(f"{document.relative_to(ROOT)}: missing anchor {target}")


def ready_lessons(manifest, progress):
    return [
        entry for entry in manifest["lessons"]
        if progress["lessons"][entry["id"]]["status"] != "completed"
        and all(progress["lessons"][p]["status"] == "completed" for p in entry["prerequisites"])
    ]


def show_active_lesson(lesson, session, step=None):
    print("Current lesson:", f"{lesson['id']} — {lesson['title']}")
    if lesson.get("delivery") == "agent-led":
        print("Continue in the conversation: ask the guiding agent to resume this lesson.")
        print("The agent presents one step at a time and maintains the session record.")
        if step is not None:
            heading = lesson["steps"][step]
            anchor = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
            print("Resuming:", heading)
            print("Agent reference:", lesson["path"] + "#" + anchor)
        else:
            print("Resuming: the agent reviews the existing handover and evidence first.")
        print("Agent-maintained record:", session)
        return
    print("Lesson file:", lesson["path"])
    print("Session record:", session)
    print("Instructions: follow the lesson file; use the session record for answers and results.")
    print("First session: begin at 'Predict before reading' in the lesson:", lesson["path"] + "#predict-before-reading")
    print("Resuming: continue at the lesson section named in the session's Handover.")


def start(lesson_id, manifest, progress):
    lesson = next((entry for entry in manifest["lessons"] if entry["id"] == lesson_id), None)
    if lesson is None:
        raise ValueError(f"Unknown lesson: {lesson_id}")
    state = progress["lessons"][lesson_id]
    if state["status"] == "completed":
        raise ValueError("Lesson already completed. Record needs_review first if reassessment is required.")
    blockers = [p for p in lesson["prerequisites"] if progress["lessons"][p]["status"] != "completed"]
    if blockers:
        raise ValueError("Incomplete prerequisites: " + ", ".join(blockers))
    active = [
        key for key, value in progress["lessons"].items()
        if value["status"] == "in_progress" and key != lesson_id
    ]
    if active:
        raise ValueError("Close or mark the existing attempt blocked/needs_review first: " + ", ".join(active))
    if state["status"] == "in_progress" and state["attempts"]:
        attempt = state["attempts"][-1]
        show_active_lesson(lesson, attempt["session"], attempt.get("step"))
        return
    attempt_number = len(state["attempts"]) + 1
    relative = f"sessions/{lesson_id}/attempt-{attempt_number:02d}.md"
    destination = local_path(relative)
    if destination.exists():
        raise ValueError(f"Refusing to overwrite existing record: {relative}")
    lesson_section(lesson, "Concept")
    lesson_section(lesson, "Predict before reading")
    replacements = {
        "lesson_id": lesson_id, "title": lesson["title"],
        "attempt": f"{attempt_number:02d}", "date": date.today().isoformat(),
        "lesson_link": "../../" + lesson["path"],
    }
    template = (ROOT / "templates/session.md").read_text()
    for key, value in replacements.items():
        template = template.replace("{{" + key + "}}", value)
    if lesson.get("delivery") == "agent-led":
        template = template.replace(
            "**Instructions:** [Lesson]",
            "**Agent-maintained record; learner responds in conversation.**\n\n"
            "**Agent reference:** [Teaching sequence]",
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(template)
    state["status"] = "in_progress"
    state["attempts"].append({
        "session": relative, "date": replacements["date"],
        "assistance": "not_recorded", "independent_check": "not_attempted", "evidence": [],
    })
    if lesson.get("delivery") == "agent-led":
        state["attempts"][-1]["step"] = next(iter(lesson["steps"]))
    progress["note"] = "Actual attempt history; completion and capability claims require reviewed evidence."
    temporary = ROOT / "curriculum/progress.json.tmp"
    temporary.write_text(json.dumps(progress, indent=2) + "\n")
    temporary.replace(ROOT / "curriculum/progress.json")
    print(f"Started {lesson_id}: {relative}")
    print("No completion or mastery was awarded.")
    show_active_lesson(lesson, relative, state["attempts"][-1].get("step"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check")
    commands.add_parser("status")
    opening = commands.add_parser("start")
    opening.add_argument("lesson_id")
    args = parser.parse_args()
    try:
        manifest, progress = validate()
        if args.command == "check":
            print("OK: 30 modules; concept focus, dependencies, local links, and progress structure valid.")
            print("Structural validation does not establish learner understanding or Linux lab results.")
        elif args.command == "status":
            active = [
                entry for entry in manifest["lessons"]
                if progress["lessons"][entry["id"]]["status"] == "in_progress"
            ]
            if active:
                lesson = active[0]
                attempt = progress["lessons"][lesson["id"]]["attempts"][-1]
                show_active_lesson(lesson, attempt["session"], attempt.get("step"))
            else:
                ready = ready_lessons(manifest, progress)
                if ready:
                    lesson = ready[0]
                    print("Next ready:", f"{lesson['id']} — {lesson['title']}")
                    print("Lesson file:", lesson["path"])
                    print("Next action:", f"python3 scripts/curriculum.py start {lesson['id']}")
                    print("Why now: starting creates the evidence record where the lesson work is documented.")
                else:
                    print("Next ready: none; inspect blockers or final review")
            print("Lesson states:", dict(Counter(x["status"] for x in progress["lessons"].values())))
            print("Independent capabilities:", sum(x["status"] == "demonstrated_independently" for x in progress["capabilities"].values()))
        else:
            start(args.lesson_id, manifest, progress)
    except (ValueError, KeyError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
