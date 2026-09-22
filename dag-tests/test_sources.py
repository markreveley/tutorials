"""Offline integrity checks for the source used by Rust reading assessments."""

import re
import unittest

from checks import HERE, RUST_ROOTS, local_file, read_json, require, sha256


def check_snapshots(lock):
    require(lock["repository"] == "https://github.com/ob6to8/beatcode", "Wrong source repository")
    require(re.fullmatch(r"[0-9a-f]{40}", lock["commit"]), "Source needs a full commit SHA")
    require(RUST_ROOTS <= lock["functions"].keys(), "Missing reading source")
    for source_id, entry in lock["functions"].items():
        raw = local_file(HERE / "fixtures", entry["snapshot"]).read_bytes()
        require(sha256(raw) == entry["excerpt_sha256"], f"{source_id}: snapshot hash mismatch")
        require(0 < entry["start_line"] <= entry["end_line"], f"{source_id}: invalid source range")
        require(len(raw.splitlines()) == entry["end_line"] - entry["start_line"] + 1,
                f"{source_id}: source range differs from excerpt")
        require(re.fullmatch(r"[0-9a-f]{64}", entry["file_sha256"]), "Missing source-file hash")
        expected_url = (f"{lock['repository']}/blob/{lock['commit']}/{entry['path']}"
                        f"#L{entry['start_line']}-L{entry['end_line']}")
        require(entry["url"] == expected_url, f"{source_id}: source URL is not pinned")
        require(re.match(rf"(?:pub )?fn {re.escape(entry['symbol'])}[<(]", raw.decode()),
                f"{source_id}: snapshot does not start with its declared function")


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.lock = read_json(HERE / "fixtures/beatcode.lock.json")

    def test_retained_beatcode_functions_have_intact_provenance(self):
        check_snapshots(self.lock)

    def test_changed_excerpt_hash_is_rejected(self):
        self.lock["functions"]["cli.build"]["excerpt_sha256"] = "0" * 64
        with self.assertRaisesRegex(AssertionError, "hash mismatch"):
            check_snapshots(self.lock)

    def test_floating_branch_reference_is_rejected(self):
        self.lock["functions"]["cli.build"]["url"] = "https://github.com/ob6to8/beatcode/blob/main/src/cli.rs"
        with self.assertRaisesRegex(AssertionError, "not pinned"):
            check_snapshots(self.lock)


if __name__ == "__main__":
    unittest.main()
