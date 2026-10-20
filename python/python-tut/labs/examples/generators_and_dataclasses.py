"""Lesson 05: generators, dataclasses, and type hints as documentation."""
from dataclasses import FrozenInstanceError, dataclass, field
import json
from pathlib import Path
import tempfile


def read_jsonl(path):
    """Yield (line_number, record) lazily; nothing is parsed until asked for."""
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            if line.strip():
                yield lineno, json.loads(line)


with tempfile.TemporaryDirectory() as d:
    path = Path(d) / "cases.jsonl"
    path.write_text("\n".join(json.dumps({"id": f"t-{i}"}) for i in range(5)) + "\n")
    rows = read_jsonl(path)
    print("a generator object, nothing read yet:", type(rows).__name__)
    print("first record on demand:", next(rows))
    print("the rest:", [rec["id"] for _, rec in rows])
    print("exhausted; list() of it now:", list(read_jsonl(path))[:2])

squares = (n * n for n in range(4))
print("generator expression:", list(squares))
print("sum without a list in memory:", sum(n * n for n in range(1_000_000)))


@dataclass(frozen=True)
class Result:
    case_id: str
    status: str            # "scored" or "error"
    passed: bool | None = None
    error: str | None = None


r = Result("t-1", "scored", passed=True)
print(r)
print("equality by fields:", r == Result("t-1", "scored", passed=True))
try:
    r.passed = False
except FrozenInstanceError as exc:
    print("frozen:", exc)


@dataclass
class Run:
    model: str
    prompts: list[str] = field(default_factory=list)   # never `= []`


a, b = Run("gpt2"), Run("gpt2")
a.prompts.append("x")
print("default_factory gives each instance its own list:", a.prompts, b.prompts)


def accuracy(passed: int, scored: int) -> float | None:
    """Hints document intent; Python does not check them at run time."""
    return None if scored == 0 else passed / scored


print("accuracy(3, 4) =", accuracy(3, 4), "| accuracy(0, 0) =", accuracy(0, 0))
print("hints are not enforced: accuracy('3', '4') raises TypeError only because '/' does ->", end=" ")
try:
    accuracy("3", "4")
except TypeError as exc:
    print(exc)
