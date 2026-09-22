"""Lesson 09 — Complexity: O, Θ, Ω, and amortized cost.

Run: python3 -m pytest exercises/09_complexity.py
"""


def is_big_o(f_values, g_values, c, n0):
    """Return True iff the witness pair (c, n0) survives the sample.

    Precondition: f_values and g_values are equal-length sequences with
    f_values[n] == f(n) and g_values[n] == g(n) for n = 0..len-1; c > 0;
    n0 >= 0.
    Postcondition: True iff f(n) <= c*g(n) for every sampled n >= n0. This
    checks a witness, it does not prove one — a finite sample can only refute.
    """
    return all(
        f_values[n] <= c * g_values[n] for n in range(n0, len(f_values))
    )


def witness_for_polynomial(coeffs):
    """Return (c, n0) witnessing p ∈ O(n^d), for p(n) = Σ coeffs[i]·n**i.

    Precondition: coeffs is a non-empty sequence of numbers, coeffs[i] is the
    coefficient of n**i, and coeffs[-1] > 0; d == len(coeffs) - 1.
    Postcondition: for all n >= n0, p(n) <= c * n**d. Use c = Σ|coeffs[i]| and
    n0 = 1; the proof is that n**i <= n**d for every i <= d once n >= 1.
    """
    return sum(abs(a) for a in coeffs), 1


def nested_loop_count(n):
    """Return how many times the body of the triangular nest runs:

        for i in range(n):
            for j in range(i + 1, n):
                body

    Precondition: n >= 0.
    Postcondition: result == n*(n-1)//2 == Θ(n²), computed in O(1) time —
    write the closed form, not a loop.
    """
    return n * (n - 1) // 2


def master_theorem(a, b, k):
    """Classify T(n) = a·T(n/b) + Θ(n**k) by the master theorem.

    Precondition: a, b, k are ints with a >= 1, b > 1, k >= 0.
    Postcondition: returns
        "n^log_b(a)"  when log_b(a) > k   — the leaves dominate
        "n^k log n"   when log_b(a) == k  — a tie, one log per level
        "n^k"         when log_b(a) < k   — the root dominates
    Decide with integer arithmetic: log_b(a) vs k is exactly a vs b**k. No
    floats, no math.log.
    """
    if a > b ** k:                  # log_b(a) > k: leaves dominate
        return "n^log_b(a)"
    if a == b ** k:                 # log_b(a) == k: a tie
        return "n^k log n"
    return "n^k"                    # log_b(a) < k: the root dominates


def amortized_append_cost(n):
    """Return the total cost of n appends to an empty doubling array.

    Cost model: capacity starts at 0. Appending when size == capacity first
    resizes to max(1, 2*capacity), copying the current size elements at one
    unit each; then the write itself costs one unit.

    Precondition: n >= 0.
    Postcondition: result == n + (total elements copied), and result <= 3*n
    for every n — the accounting-method bound proved in lesson 09.
    """
    cap = size = total = 0
    for _ in range(n):
        if size == cap:             # full: resize and copy everything
            total += size
            cap = max(1, 2 * cap)
        total += 1                  # write the new element
        size += 1
    return total


def binary_search_counted(xs, target):
    """Return (index, comparisons) for a binary search of target in xs.

    Precondition: xs is sorted non-decreasing.
    Postcondition: xs[index] == target when index >= 0, and target not in xs
    when index == -1. `comparisons` counts one three-way comparison of target
    against an element per loop iteration, and satisfies
    comparisons <= ⌊log₂ len(xs)⌋ + 1 for non-empty xs, because each iteration
    at least halves the candidate range.
    """
    lo, hi = 0, len(xs) - 1
    comparisons = 0
    # Invariant: if target is in xs, its index lies in [lo, hi].
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        if xs[mid] == target:
            return mid, comparisons
        if xs[mid] < target:
            lo = mid + 1            # everything <= mid is too small
        else:
            hi = mid - 1            # everything >= mid is too large
    return -1, comparisons


def cost_class(operation):
    """Return the tight time bound of a CPython operation, as a string.

    Precondition: operation is one of "list_index", "list_append",
    "list_insert_front", "list_contains", "list_sort", "dict_lookup",
    "set_contains", "heap_push", "len", "str_concat".
    Postcondition: the answer is one of "O(1)", "O(1) amortized",
    "O(1) expected", "O(log n)", "O(n)", "O(n log n)", matching the cost table
    in lesson 09. An unknown name raises KeyError.
    """
    table = {
        "list_index": "O(1)",
        "len": "O(1)",
        "list_append": "O(1) amortized",
        "dict_lookup": "O(1) expected",
        "set_contains": "O(1) expected",
        "heap_push": "O(log n)",
        "list_insert_front": "O(n)",
        "list_contains": "O(n)",
        "str_concat": "O(n)",
        "list_sort": "O(n log n)",
    }
    return table[operation]


# ---------------------------------------------------------------- tests

def _poly(coeffs, n):
    return sum(a * n ** i for i, a in enumerate(coeffs))


def test_is_big_o():
    f = [3 * n * n + 7 * n + 2 for n in range(50)]
    g = [n * n for n in range(50)]
    assert is_big_o(f, g, 12, 1) is True
    assert is_big_o(f, g, 3, 1) is False      # 3n² < 3n²+7n+2 for n >= 1
    assert is_big_o(f, g, 12, 0) is False     # g(0) == 0, f(0) == 2
    assert is_big_o(f, g, 12, 60) is True     # vacuous: no sampled n >= 60
    quad = [n * n for n in range(500)]
    lin = [n for n in range(500)]
    assert is_big_o(lin, quad, 1, 1) is True
    assert is_big_o(quad, lin, 100, 1) is False   # n² ∉ O(n): c fails past n=c


def test_witness_for_polynomial():
    assert witness_for_polynomial([2, 7, 3]) == (12, 1)
    for coeffs in ([1], [0, 1], [2, 7, 3], [5, 0, 0, 4]):
        c, n0 = witness_for_polynomial(coeffs)
        d = len(coeffs) - 1
        assert c > 0 and n0 >= 1
        for n in range(n0, 200):
            assert _poly(coeffs, n) <= c * n ** d


def test_nested_loop_count():
    for n in range(0, 40):
        brute = sum(1 for i in range(n) for _ in range(i + 1, n))
        assert nested_loop_count(n) == brute
    assert nested_loop_count(10 ** 6) == 10 ** 6 * (10 ** 6 - 1) // 2


def test_master_theorem():
    assert master_theorem(2, 2, 1) == "n^k log n"      # merge sort
    assert master_theorem(1, 2, 0) == "n^k log n"      # binary search
    assert master_theorem(2, 2, 0) == "n^log_b(a)"     # tree walk
    assert master_theorem(8, 2, 2) == "n^log_b(a)"     # naive matmul
    assert master_theorem(7, 2, 2) == "n^log_b(a)"     # Strassen
    assert master_theorem(3, 2, 1) == "n^log_b(a)"     # Karatsuba
    assert master_theorem(4, 2, 2) == "n^k log n"
    assert master_theorem(2, 2, 2) == "n^k"
    assert master_theorem(1, 3, 1) == "n^k"


def test_amortized_append_cost():
    assert amortized_append_cost(0) == 0
    assert amortized_append_cost(1) == 1
    assert amortized_append_cost(2) == 3          # 2 writes + 1 copy
    assert amortized_append_cost(5) == 12         # 5 writes + (0+1+2+4)
    for n in range(0, 600):
        cost = amortized_append_cost(n)
        assert n <= cost <= 3 * n


def test_binary_search_counted():
    for n in range(1, 65):
        xs = [2 * i for i in range(n)]
        limit = (n.bit_length() - 1) + 1          # ⌊log₂ n⌋ + 1
        for i, v in enumerate(xs):
            idx, comps = binary_search_counted(xs, v)
            assert idx == i
            assert comps <= limit, (n, v, comps, limit)
        for v in (-1, 1, 2 * n):                  # absent values
            idx, comps = binary_search_counted(xs, v)
            assert idx == -1
            assert comps <= limit, (n, v, comps, limit)
    assert binary_search_counted([], 3) == (-1, 0)


def test_cost_class():
    assert cost_class("list_index") == "O(1)"
    assert cost_class("len") == "O(1)"
    assert cost_class("list_append") == "O(1) amortized"
    assert cost_class("dict_lookup") == "O(1) expected"
    assert cost_class("set_contains") == "O(1) expected"
    assert cost_class("heap_push") == "O(log n)"
    assert cost_class("list_insert_front") == "O(n)"
    assert cost_class("list_contains") == "O(n)"
    assert cost_class("str_concat") == "O(n)"
    assert cost_class("list_sort") == "O(n log n)"
    try:
        cost_class("teleport")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown operation must raise KeyError")
