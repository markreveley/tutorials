"""Assertions shared by the course acceptance tests; no third-party dependencies."""

import ast
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
COURSES = HERE.parent  # repository root
GOALS = {"python": "implement-debug-explain-evals", "rust": "read-explain-beatcode"}
MODES = {"implement", "debug", "adapt", "trace", "predict", "explain", "change-impact"}
CONTEXTS = {"support-ticket-eval", "grader-validation", "eval-data", "eval-analysis",
            "eval-runner", "agent-traces"}
COVERAGE = {
    "python": {"functions-collections", "mutation-and-records", "files-jsonl-validation",
               "scoring", "grader-validation", "error-accounting", "reproducibility",
               "paired-analysis", "bounded-concurrency-retries", "agent-traces"},
    "rust": {"pipeline-navigation", "ownership-borrowing", "option-result-errors",
             "enums-patterns", "generics-traits", "collections-iterators",
             "numeric-determinism", "tests-and-spec", "change-impact"},
}
RUST_ROOTS = {"cli.build", "events.compile", "score.num_token", "jsonl.events_jsonl",
              "events.time_offset", "render.render"}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def read_json(path):
    path = Path(path)
    require(path.is_file(), f"Missing {path}: author this artifact to satisfy the test-first contract")
    return json.loads(path.read_text())


def local_file(root, relative):
    require(nonempty(relative) and not Path(relative).is_absolute(), "Expected a relative local path")
    target = (root / relative).resolve()
    require(target.is_relative_to(root.resolve()), f"Path escapes its root: {relative}")
    require(target.is_file(), f"Missing local page or fixture: {relative}")
    return target


def check_graph(course):
    require(course.get("schema_version") == 1, "schema_version must be 1")
    require(course.get("language") in GOALS, "language must be python or rust")
    nodes = course.get("nodes")
    require(isinstance(nodes, list) and nodes, "nodes must be a nonempty list")
    ids = [n.get("id") for n in nodes]
    require(all(nonempty(i) for i in ids), "Every node needs an id")
    require(len(ids) == len(set(ids)), "Duplicate node id")
    by_id = dict(zip(ids, nodes))
    roots = course.get("roots")
    require(isinstance(roots, list) and roots, "roots must be a nonempty list")
    require(all(nonempty(r) for r in roots), "Root ids must be strings")
    require(len(roots) == len(set(roots)), "Duplicate root")
    require(set(roots) <= by_id.keys(), "Dangling root")
    parents = {i: set() for i in ids}
    for n in nodes:
        label = n["id"]
        require(n.get("kind") in {"function", "rule", "expression", "primitive"}, f"{label}: invalid kind")
        require(type(n.get("level")) is int and n["level"] >= 0, f"{label}: invalid level")
        for field in ("title", "payload", "explanation", "page"):
            require(nonempty(n.get(field)), f"{label}: missing {field}")
        assessment = n.get("assessment", {})
        require(assessment.get("mode") in MODES, f"{label}: invalid assessment mode")
        require(nonempty(assessment.get("prompt")) and nonempty(assessment.get("success")),
                f"{label}: assessment needs prompt and success criterion")
        edges = n.get("depends_on")
        require(isinstance(edges, list), f"{label}: depends_on must be a list")
        targets = [e.get("id") for e in edges]
        require(all(nonempty(t) for t in targets), f"{label}: dependency ids must be strings")
        require(len(targets) == len(set(targets)), f"{label}: duplicate edge")
        require(set(targets) <= by_id.keys(), f"{label}: dangling edge")
        for edge in edges:
            require(nonempty(edge.get("anchor")) and edge["anchor"] in n["payload"],
                    f"{label}: edge anchor is absent from payload")
            require(nonempty(edge.get("why")), f"{label}: edge needs an explanation")
            parents[edge["id"]].add(label)
        if not edges:
            require(n["kind"] == "primitive" and n["level"] == 0,
                    f"{label}: unexplained leaf must be an explicit primitive at level 0")
            require(nonempty(n.get("stop_reason")), f"{label}: primitive needs stop_reason")
        else:
            require(n["kind"] != "primitive", f"{label}: primitive cannot have dependencies")

    active, seen = set(), set()

    def visit(node_id):
        require(node_id not in active, f"Cycle through {node_id}")
        if node_id in seen:
            return
        active.add(node_id)
        for edge in by_id[node_id]["depends_on"]:
            visit(edge["id"])
        active.remove(node_id)
        seen.add(node_id)

    for root in roots:
        require(by_id[root]["kind"] == "function", f"{root}: root must carry a function")
        require(not parents[root], f"{root}: entry root has an incoming edge")
        visit(root)
    require(seen == set(ids), f"Orphan nodes: {sorted(set(ids) - seen)}")
    for n in nodes:
        for edge in n["depends_on"]:
            require(by_id[edge["id"]]["level"] < n["level"],
                    f"{n['id']}: dependency must lower abstraction level")
    require(any(len(p) > 1 for p in parents.values()), "Expected a shared dependency, not only a tree")
    for root in roots:
        # Require an actual function → rule → lower rule/expression → ... path.
        rules = [by_id[e["id"]] for e in by_id[root]["depends_on"]
                 if by_id[e["id"]]["kind"] == "rule"]
        require(any(by_id[e["id"]]["kind"] in {"rule", "expression"}
                    for rule in rules for e in rule["depends_on"]),
                f"{root}: needs a rule and a lower rule/expression before primitives")
    return by_id


def check_course(course, language, lock):
    by_id = check_graph(course)
    require(course["language"] == language, "Wrong language")
    require(course.get("goal") == GOALS[language], "Wrong proficiency goal")
    coverage = course.get("coverage", {})
    require(COVERAGE[language] <= coverage.keys(), "Missing capability coverage")
    for capability, ids in coverage.items():
        require(isinstance(ids, list) and ids and all(nonempty(i) for i in ids),
                f"{capability}: coverage needs node ids")
        require(set(ids) <= by_id.keys(), f"{capability}: coverage references absent nodes")
    modes = {"implement", "debug", "adapt"} if language == "python" else {
        "trace", "predict", "explain", "change-impact"}
    for root in course["roots"]:
        require(by_id[root]["assessment"]["mode"] in modes, f"{root}: wrong proficiency assessment")
    for n in by_id.values():
        if language == "rust":
            require(n["assessment"]["mode"] not in {"implement", "debug", "adapt"},
                    f"{n['id']}: Rust requires reading assessments")
        if n["kind"] != "function":
            continue
        if language == "python":
            require(n.get("context") in CONTEXTS, f"{n['id']}: missing eval context")
            tree = ast.parse(n["payload"])
            require(len(tree.body) == 1 and isinstance(tree.body[0], (ast.FunctionDef, ast.AsyncFunctionDef)),
                    f"{n['id']}: payload must be one Python function")
            require(not any(isinstance(x, ast.Constant) and x.value is Ellipsis for x in ast.walk(tree)),
                    f"{n['id']}: unfinished function payload")
        else:
            require(n.get("context") == "beatcode", f"{n['id']}: missing beatcode context")
            require(n.get("source_id") in lock["functions"], f"{n['id']}: unpinned Rust function")
            source = lock["functions"][n["source_id"]]
            expected = local_file(HERE / "fixtures", source["snapshot"]).read_text()
            require(n["payload"].strip() == expected.strip(), f"{n['id']}: Rust payload differs from pinned source")
    if language == "rust":
        require(RUST_ROOTS <= {by_id[r].get("source_id") for r in course["roots"]},
                "Missing beatcode reading entry points")
    return by_id


def check_pages(course, root):
    by_id = {n["id"]: n for n in course["nodes"]}
    paths = {i: local_file(root, n["page"]) for i, n in by_id.items()}
    require(len(set(paths.values())) == len(paths), "Each concept needs its own page")
    for node_id, n in by_id.items():
        page = paths[node_id]
        content = page.read_text()
        require(n["payload"].strip() in content, f"{node_id}: page is missing its payload")
        links = re.findall(r"\]\(([^)]+)\)", content)
        local_targets = {(page.parent / link.split("#")[0]).resolve()
                         for link in links if "://" not in link}
        for edge in n["depends_on"]:
            require(paths[edge["id"]] in local_targets, f"{node_id}: missing dependency page link")


def sha256(data):
    return hashlib.sha256(data).hexdigest()
