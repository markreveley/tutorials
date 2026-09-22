"""Verify retained source against a local pinned clone. Does not fetch or modify it."""

from pathlib import Path
import subprocess
import sys

from checks import HERE, local_file, read_json, require, sha256
from test_sources import check_snapshots


def verify(repo):
    lock = read_json(HERE / "fixtures/beatcode.lock.json")
    check_snapshots(lock)
    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    require(commit == lock["commit"], f"Checkout is {commit}; expected {lock['commit']}")
    for source_id, entry in lock["functions"].items():
        raw = local_file(repo, entry["path"]).read_bytes()
        require(sha256(raw) == entry["file_sha256"], f"{source_id}: source file changed")
        excerpt = b"".join(raw.splitlines(keepends=True)[entry["start_line"] - 1:entry["end_line"]])
        snapshot = local_file(HERE / "fixtures", entry["snapshot"]).read_bytes()
        require(excerpt == snapshot, f"{source_id}: checkout differs from retained excerpt")
    print(f"PASS: {len(lock['functions'])} excerpts match beatcode {commit}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 verify_beatcode.py /path/to/beatcode")
    verify(Path(sys.argv[1]).resolve())
