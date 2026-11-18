"""Lesson 01 — Objects, names, and expressions.

Run: python3 -m pytest exercises/01_objects.py
"""


def same_object(a, b):
    """Return True iff a and b are the very same object (identity, not value)."""
    return a is b


def is_integer_valued(x):
    """Return True iff x is an int, a bool, or a float with no fractional part.

    Precondition: x is any Python object.
    Postcondition: result is True for 3, True, 3.0, -0.0; False for 3.5,
    "3", None, float('inf'), float('nan').
    """
    if isinstance(x, (bool, int)):
        return True
    if isinstance(x, float):
        return x == x and x not in (float('inf'), float('-inf')) and x == int(x)
    return False


def floor_div_and_mod(a, b):
    """Return (q, r) with a == q*b + r and 0 <= r < b.

    Precondition: a is an int, b is an int with b > 0.
    Do not use //, %, divmod, or math.floor. Use repeated subtraction/addition
    or int(a / b) with a correction step.
    """
    q = int(a / b)          # truncates toward zero
    r = a - q * b
    if r < 0:               # truncation overshot for negative a
        q -= 1
        r += b
    return q, r


def classify(x):
    """Return one of 'bool', 'int', 'float', 'str', 'none', 'other'.

    Note bool must be reported as 'bool', not 'int', even though
    isinstance(True, int) is True.
    """
    if isinstance(x, bool):
        return 'bool'
    if isinstance(x, int):
        return 'int'
    if isinstance(x, float):
        return 'float'
    if isinstance(x, str):
        return 'str'
    if x is None:
        return 'none'
    return 'other'


def truthy_count(items):
    """Return how many elements of items are true in a boolean context."""
    return sum(1 for it in items if it)


def safe_divide(a, b):
    """Return a / b as a float, or None if b == 0."""
    if b == 0:
        return None
    return a / b


# ---------------------------------------------------------------- tests

def test_same_object():
    x = [1, 2]
    y = x
    z = [1, 2]
    assert same_object(x, y) is True
    assert same_object(x, z) is False
    assert same_object(None, None) is True


def test_is_integer_valued():
    assert is_integer_valued(3)
    assert is_integer_valued(True)
    assert is_integer_valued(3.0)
    assert is_integer_valued(-0.0)
    assert not is_integer_valued(3.5)
    assert not is_integer_valued("3")
    assert not is_integer_valued(None)
    assert not is_integer_valued(float("inf"))
    assert not is_integer_valued(float("nan"))


def test_floor_div_and_mod():
    for a in range(-20, 21):
        for b in (1, 2, 3, 7):
            q, r = floor_div_and_mod(a, b)
            assert a == q * b + r, (a, b, q, r)
            assert 0 <= r < b, (a, b, q, r)
            assert (q, r) == divmod(a, b)


def test_classify():
    assert classify(True) == "bool"
    assert classify(0) == "int"
    assert classify(0.0) == "float"
    assert classify("") == "str"
    assert classify(None) == "none"
    assert classify([]) == "other"


def test_truthy_count():
    assert truthy_count([0, 1, "", "a", None, [], [0], 0.0, -1]) == 4
    assert truthy_count([]) == 0


def test_safe_divide():
    assert safe_divide(7, 2) == 3.5
    assert isinstance(safe_divide(4, 2), float)
    assert safe_divide(1, 0) is None
