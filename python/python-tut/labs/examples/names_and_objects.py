"""Lesson 02: names bind to objects; mutation is visible through every name."""
import copy

scores = [0.5, 0.7]
same = scores            # a second name for the same list object
same.append(0.9)
print("scores after appending through `same`:", scores)
print("scores is same:", scores is same, "| id equal:", id(scores) == id(same))

fresh = list(scores)     # a shallow copy: a new list object
fresh.append(1.0)
print("scores after appending to the copy:  ", scores)
print("fresh:", fresh, "| scores is fresh:", scores is fresh)

run = {"model": "gpt2", "prompts": ["a", "b"]}
shallow = dict(run)
shallow["prompts"].append("c")        # the inner list is shared
print("shallow copy shares the inner list:", run["prompts"])
deep = copy.deepcopy(run)
deep["prompts"].append("d")
print("deep copy does not:               ", run["prompts"])

t = (1, 2)
print("tuples are immutable; t + (3,) makes a new object:", t + (3,), "| t unchanged:", t)

def record(result, log=[]):               # the classic trap: one default list, shared
    log.append(result)
    return log
print("first call:", record("pass"))
print("second call reuses the same default list:", record("fail"))

def record_safely(result, log=None):
    log = [] if log is None else log
    log.append(result)
    return log
print("safe version, two calls:", record_safely("pass"), record_safely("fail"))

a = 1_000_000
b = a
b += 1                                    # ints are immutable: b now names a new int
print("a, b after b += 1:", a, b)
