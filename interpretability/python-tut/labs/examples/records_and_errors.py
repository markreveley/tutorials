"""Lesson 03: dicts, lists, JSON/JSONL, and exceptions as the error channel."""
import json
from pathlib import Path
import tempfile

row = {"id": "t-1", "input": "Refund order A-42", "reference": {"category": "refund", "urgent": True, "order_id": None}}
text = json.dumps(row)
print("json.dumps:", text)
back = json.loads(text)
print("round trip equal:", back == row, "| True became", type(back["reference"]["urgent"]).__name__, "| None became", back["reference"]["order_id"])

print("key order is irrelevant to ==:", {"a": 1, "b": 2} == {"b": 2, "a": 1})
print("but 1 == True in Python:", {"urgent": 1} == {"urgent": True}, "<- the trap score_ticket must avoid")
print("type check catches it:", type(1) is bool, type(True) is bool)

print("duplicate keys: json.loads keeps the last one ->", json.loads('{"x": 1, "x": 2}'))

def reject_duplicates(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key {key!r}")
        seen[key] = value
    return seen

try:
    json.loads('{"x": 1, "x": 2}', object_pairs_hook=reject_duplicates)
except ValueError as exc:
    print("with object_pairs_hook:", exc)

with tempfile.TemporaryDirectory() as d:
    path = Path(d) / "cases.jsonl"
    path.write_text('{"id": "a"}\n\n{"id": "b"}\n{bad json}\n', encoding="utf-8")
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"line {lineno}: invalid JSON ({exc.msg} at column {exc.colno})")
                break
            print(f"line {lineno}: {record}")

try:
    Path("/nonexistent/cases.jsonl").read_text()
except FileNotFoundError as exc:
    print("FileNotFoundError is a different error from bad data:", exc.strerror)

try:
    value = int("not a number")
except ValueError as exc:
    print("ValueError:", exc)
else:
    print("else runs only when nothing was raised")
finally:
    print("finally always runs: remove hooks here")
