"""Positive and adversarial examples for the DAG acceptance checks."""

import copy
from pathlib import Path
import tempfile
import unittest

from checks import check_graph, check_pages, check_course, COVERAGE, GOALS, HERE, RUST_ROOTS, local_file, read_json


def valid_graph():
    def node(node_id, kind, level, targets):
        return {
            "id": node_id, "kind": kind, "level": level, "title": node_id,
            "page": f"{node_id}.md", "payload": "def score_ticket(x):\n    return x",
            "explanation": "A fixture, not an authored lesson.",
            "context": "support-ticket-eval",
            "depends_on": [{"id": t, "anchor": "x", "why": "Explain x here."} for t in targets],
            "assessment": {"mode": "explain", "prompt": "What does x mean?", "success": "Name its binding."},
        }
    nodes = [node("score", "function", 3, ["keys", "values"]),
             node("keys", "rule", 2, ["lookup"]),
             node("values", "rule", 2, ["lookup"]),
             node("lookup", "expression", 1, ["name"]),
             node("name", "primitive", 0, [])]
    nodes[0]["assessment"]["mode"] = "implement"
    nodes[-1]["stop_reason"] = "Recognizing a written name is the stated baseline."
    return {"schema_version": 1, "language": "python", "goal": GOALS["python"],
            "roots": ["score"], "nodes": nodes,
            "coverage": {k: ["score"] for k in COVERAGE["python"]}}


class GraphContractTests(unittest.TestCase):
    def setUp(self):
        self.graph = valid_graph()

    def reject(self, message):
        with self.assertRaisesRegex(AssertionError, message):
            check_graph(self.graph)

    def test_accepts_shared_concepts(self):
        check_graph(self.graph)

    def test_accepts_python_course_contract(self):
        check_course(self.graph, "python", {})

    def test_accepts_multiple_functions_sharing_rules(self):
        root = copy.deepcopy(self.graph["nodes"][0])
        root.update(id="other-function", page="other.md")
        self.graph["nodes"].append(root)
        self.graph["roots"].append(root["id"])
        check_graph(self.graph)

    def test_order_of_storage_is_not_a_learning_order(self):
        self.graph["nodes"].reverse()
        check_graph(self.graph)

    def test_duplicate_id(self):
        self.graph["nodes"].append(copy.deepcopy(self.graph["nodes"][0]))
        self.reject("Duplicate node")

    def test_dangling_edge(self):
        self.graph["nodes"][0]["depends_on"][0]["id"] = "missing"
        self.reject("dangling edge")

    def test_duplicate_edge(self):
        self.graph["nodes"][0]["depends_on"] *= 2
        self.reject("duplicate edge")

    def test_cycle_below_root(self):
        self.graph["nodes"][3]["depends_on"].append({"id": "keys", "anchor": "x", "why": "Invalid cycle"})
        self.reject("Cycle")

    def test_self_cycle(self):
        self.graph["nodes"][1]["depends_on"][0]["id"] = "keys"
        self.reject("Cycle")

    def test_orphan(self):
        orphan = copy.deepcopy(self.graph["nodes"][-1])
        orphan["id"] = "unused"
        self.graph["nodes"].append(orphan)
        self.reject("Orphan")

    def test_equal_abstraction_rank(self):
        self.graph["nodes"][1]["level"] = 3
        self.reject("lower abstraction")

    def test_rule_cannot_masquerade_as_a_foundation(self):
        self.graph["nodes"][-1]["kind"] = "rule"
        self.reject("unexplained leaf")

    def test_foundation_requires_stopping_reason(self):
        del self.graph["nodes"][-1]["stop_reason"]
        self.reject("stop_reason")

    def test_foundation_cannot_hide_more_dependencies(self):
        self.graph["nodes"][3]["kind"] = "primitive"
        self.reject("primitive cannot")

    def test_edge_needs_relevant_code_anchor(self):
        self.graph["nodes"][0]["depends_on"][0]["anchor"] = "unrelated code"
        self.reject("anchor")

    def test_edge_needs_reason(self):
        self.graph["nodes"][0]["depends_on"][0]["why"] = " "
        self.reject("edge needs an explanation")

    def test_shallow_glossary_is_not_recursive_explanation(self):
        for n in self.graph["nodes"][1:3]:
            n["depends_on"][0]["id"] = "name"
        del self.graph["nodes"][3]
        self.reject("lower rule/expression")

    def test_tree_does_not_demonstrate_concept_reuse(self):
        self.graph["nodes"][0]["depends_on"] = self.graph["nodes"][0]["depends_on"][:1]
        del self.graph["nodes"][2]
        self.reject("shared dependency")

    def test_assessment_requires_observable_success(self):
        self.graph["nodes"][1]["assessment"]["success"] = ""
        self.reject("success criterion")

    def test_root_must_be_a_function(self):
        self.graph["nodes"][0]["kind"] = "rule"
        self.reject("root must carry a function")

    def test_python_needs_authorship_assessment(self):
        self.graph["nodes"][0]["assessment"]["mode"] = "trace"
        with self.assertRaisesRegex(AssertionError, "wrong proficiency"):
            check_course(self.graph, "python", {})

    def test_python_payload_must_be_function_code(self):
        self.graph["nodes"][0]["payload"] = "x = 1"
        with self.assertRaisesRegex(AssertionError, "one Python function"):
            check_course(self.graph, "python", {})

    def test_python_function_needs_eval_context(self):
        self.graph["nodes"][0]["context"] = "leetcode"
        with self.assertRaisesRegex(AssertionError, "eval context"):
            check_course(self.graph, "python", {})

    def test_course_cannot_omit_capability(self):
        del self.graph["coverage"]["error-accounting"]
        with self.assertRaisesRegex(AssertionError, "Missing capability"):
            check_course(self.graph, "python", {})

    def test_coverage_cannot_reference_nonexistent_node(self):
        self.graph["coverage"]["scoring"] = ["absent"]
        with self.assertRaisesRegex(AssertionError, "absent nodes"):
            check_course(self.graph, "python", {})

    def test_page_links_are_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for n in self.graph["nodes"]:
                links = "\n".join(f"[explain]({e['id']}.md)" for e in n["depends_on"])
                (root / n["page"]).write_text(n["payload"] + "\n" + links)
            check_pages(self.graph, root)
            (root / "score.md").write_text(self.graph["nodes"][0]["payload"])
            with self.assertRaisesRegex(AssertionError, "missing dependency page link"):
                check_pages(self.graph, root)

    def test_path_must_remain_inside_course(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(AssertionError, "escapes"):
                local_file(Path(directory), "../outside.md")


class RustCourseContractTests(unittest.TestCase):
    def setUp(self):
        self.lock = read_json(HERE / "fixtures/beatcode.lock.json")
        self.graph = valid_graph()
        template = self.graph["nodes"].pop(0)
        self.graph.update(language="rust", goal=GOALS["rust"], roots=[])
        for source_id in sorted(RUST_ROOTS):
            root = copy.deepcopy(template)
            source = self.lock["functions"][source_id]
            root.update(id=source_id, source_id=source_id, context="beatcode",
                        payload=(HERE / "fixtures" / source["snapshot"]).read_text())
            root["assessment"]["mode"] = "explain"
            for edge in root["depends_on"]:
                edge["anchor"] = "("
            self.graph["nodes"].append(root)
            self.graph["roots"].append(source_id)
        self.graph["coverage"] = {k: ["cli.build"] for k in COVERAGE["rust"]}

    def test_accepts_pinned_beatcode_course(self):
        check_course(self.graph, "rust", self.lock)

    def test_rejects_synthetic_or_unpinned_rust_example(self):
        self.graph["nodes"][-1]["source_id"] = "invented.function"
        with self.assertRaisesRegex(AssertionError, "unpinned Rust"):
            check_course(self.graph, "rust", self.lock)

    def test_rejects_changed_rust_payload(self):
        self.graph["nodes"][-1]["payload"] += "\n// a change to the source\n"
        with self.assertRaisesRegex(AssertionError, "differs from pinned"):
            check_course(self.graph, "rust", self.lock)

    def test_rejects_rust_implementation_requirement_even_below_root(self):
        self.graph["nodes"][0]["assessment"]["mode"] = "implement"
        with self.assertRaisesRegex(AssertionError, "Rust requires reading"):
            check_course(self.graph, "rust", self.lock)


if __name__ == "__main__":
    unittest.main()
