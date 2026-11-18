"""Manifest assertions for labs/manifest.py. RED on the stubs; no solution here."""
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

import manifest


def arrays():
    rng = np.random.default_rng(0)
    return {"embed": rng.normal(size=(2, 5, 768)).astype(np.float32),
            "block.0": rng.normal(size=(2, 5, 768)).astype(np.float32)}


class DigestTests(unittest.TestCase):
    def test_digest_is_sha256_hex_and_stable(self):
        a = np.arange(6, dtype=np.float32).reshape(2, 3)
        d = manifest.tensor_digest(a)
        self.assertEqual(len(d), 64)
        self.assertEqual(d, manifest.tensor_digest(a.copy()))

    def test_non_contiguous_view_matches_its_copy(self):
        a = np.arange(12, dtype=np.float32).reshape(3, 4)
        view = a.T
        self.assertFalse(view.flags["C_CONTIGUOUS"])
        self.assertEqual(manifest.tensor_digest(view), manifest.tensor_digest(np.ascontiguousarray(view)))

    def test_changing_one_value_changes_the_digest(self):
        a = np.zeros((2, 3), dtype=np.float32); b = a.copy(); b[1, 2] = 1e-7
        self.assertNotEqual(manifest.tensor_digest(a), manifest.tensor_digest(b))


class BuildManifestTests(unittest.TestCase):
    def test_keys_shapes_dtypes_and_order(self):
        t = arrays()
        m = manifest.build_manifest("gpt2", ["The capital of France is", "Hello"], t, 0, {"torch": "x"})
        self.assertEqual(set(m), {"model", "prompts", "seed", "versions", "tensors"})
        self.assertEqual(list(m["tensors"]), ["embed", "block.0"])
        self.assertEqual(m["tensors"]["embed"], {"shape": [2, 5, 768], "dtype": "float32",
                                                 "sha256": manifest.tensor_digest(t["embed"])})
        self.assertEqual(m["seed"], 0)
        self.assertEqual(m["model"], "gpt2")

    def test_is_json_serialisable_and_deterministic(self):
        t = arrays()
        a = manifest.build_manifest("gpt2", ["p"], t, 1, {"numpy": np.__version__})
        b = manifest.build_manifest("gpt2", ["p"], t, 1, {"numpy": np.__version__})
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        self.assertEqual(json.loads(json.dumps(a)), a)

    def test_shape_entries_are_plain_ints_not_numpy_scalars(self):
        m = manifest.build_manifest("gpt2", ["p"], arrays(), 1, {})
        for dim in m["tensors"]["embed"]["shape"]:
            self.assertIs(type(dim), int)


class CheckManifestTests(unittest.TestCase):
    def test_matching_arrays_report_no_problems(self):
        t = arrays()
        m = manifest.build_manifest("gpt2", ["p", "q"], t, 0, {})
        self.assertEqual(manifest.check_manifest(m, t), [])

    def test_each_kind_of_mismatch_is_reported_not_raised(self):
        t = arrays()
        m = manifest.build_manifest("gpt2", ["p", "q"], t, 0, {})
        cases = {}
        c = arrays(); c["block.0"][0, 0, 0] += 1.0; cases["digest"] = c
        c = arrays(); c["block.0"] = c["block.0"][:, :4]; cases["shape"] = c
        c = arrays(); c["block.0"] = c["block.0"].astype(np.float64); cases["dtype"] = c
        c = arrays(); del c["block.0"]; cases["missing"] = c
        c = arrays(); c["block.1"] = c["block.0"]; cases["undescribed"] = c
        for label, bad in cases.items():
            with self.subTest(label=label):
                problems = manifest.check_manifest(m, bad)
                self.assertTrue(problems, "expected at least one problem")
                self.assertTrue(all(isinstance(p, str) and p for p in problems))

    def test_problem_messages_name_the_tensor(self):
        t = arrays()
        m = manifest.build_manifest("gpt2", ["p", "q"], t, 0, {})
        bad = arrays(); bad["block.0"] = bad["block.0"][:, :4]
        self.assertTrue(any("block.0" in p for p in manifest.check_manifest(m, bad)))


class WriteManifestTests(unittest.TestCase):
    def test_writes_sorted_utf8_json_with_newline(self):
        m = manifest.build_manifest("gpt2", ["Où est ma commande ?"], arrays(), 0, {})
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "manifest.json"
            manifest.write_manifest(m, path)
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.endswith("\n"))
            self.assertEqual(json.loads(text), m)
            self.assertEqual(text, json.dumps(m, sort_keys=True, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    unittest.main()
