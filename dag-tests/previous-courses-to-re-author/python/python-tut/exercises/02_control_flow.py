"""Lesson 02 — Control flow and loop invariants.

Run: python3 -m pytest exercises/02_control_flow.py

Every loop below has a stated invariant and a stated variant. Write the
invariant in a comment before you write the body.
"""

import math


def sum_and_max(nums):
    """Return (total, largest) after a single pass over nums.

    Precondition: nums is a sequence of numbers.
    Postcondition: total == sum(nums); largest == max(nums), or None if
    nums is empty (then total is 0).
    Invariant at the top of iteration i: total == sum(nums[0..i)) and
    largest == max(nums[0..i)) (None when i == 0).
    Variant: len(nums) - i.
    """
    raise NotImplementedError


def power(base, exp):
    """Return base ** exp by repeated squaring, in O(log exp) multiplications.

    Precondition: exp is an int with exp >= 0; base is an int or float.
    Postcondition: result == base ** exp.
    Invariant: result * acc ** n == base ** exp and n >= 0.
    Variant: n, which at least halves each iteration.
    Do not use ** or pow().
    """
    raise NotImplementedError


def gcd(a, b):
    """Return the greatest common divisor of a and b.

    Precondition: a >= 0, b >= 0, not both zero.
    Postcondition: result divides a and b, and every common divisor of
    a and b divides result.
    Invariant: gcd(a, b) is unchanged, because gcd(a, b) == gcd(b, a % b).
    Variant: b, which strictly decreases since 0 <= a % b < b.
    Do not use math.gcd.
    """
    raise NotImplementedError


def first_index_of(xs, target):
    """Return the smallest i with xs[i] == target, or -1 if there is none.

    Precondition: xs is a sequence.
    Postcondition: if result >= 0 then xs[result] == target and target is
    not in xs[0..result); if result == -1 then target is not in xs.
    Use a for loop with an else clause rather than a found flag.
    """
    raise NotImplementedError


def is_prime(n):
    """Return True iff n is a prime number.

    Precondition: n is an int (any sign).
    Postcondition: True iff n >= 2 and no d in [2, n) divides n.
    Trial division to floor(sqrt(n)) suffices: if n == p*q with p <= q
    then p*p <= n, so a composite always has a factor at or below sqrt(n).
    Use break plus the loop's else clause.
    """
    raise NotImplementedError


def fizzbuzz(n):
    """Return the FizzBuzz list for 1..n.

    Precondition: n is an int with n >= 0.
    Postcondition: a list of length n whose i-th entry (1-based i) is
    'FizzBuzz' if 15 | i, else 'Fizz' if 3 | i, else 'Buzz' if 5 | i,
    else str(i). The order of the elif chain is the whole exercise.
    """
    raise NotImplementedError


def collatz_steps(n):
    """Return how many steps the Collatz map takes to bring n to 1.

    Precondition: n is an int with n >= 1.
    Postcondition: result is the number of applications of
    n -> n//2 (n even) / 3n+1 (n odd) needed to reach 1; 0 when n == 1.
    Invariant: steps counts the applications performed so far.
    Termination: no variant is known -- the Collatz conjecture is open.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- tests

def test_sum_and_max():
    assert sum_and_max([]) == (0, None)
    assert sum_and_max([5]) == (5, 5)
    assert sum_and_max([3, 1, 4, 1, 5]) == (14, 5)
    assert sum_and_max([-3, -1, -4]) == (-8, -1)
    assert sum_and_max((2, 2, 2)) == (6, 2)


def test_power():
    for b in (0, 1, 2, 3, -2):
        for e in range(0, 12):
            assert power(b, e) == b ** e, (b, e)
    assert power(2, 40) == 2 ** 40
    assert power(1.5, 3) == 1.5 ** 3


def test_gcd():
    assert gcd(12, 18) == 6
    assert gcd(18, 12) == 6
    assert gcd(17, 5) == 1
    assert gcd(0, 7) == 7
    assert gcd(7, 0) == 7
    assert gcd(270, 192) == 6
    for a in range(1, 40):
        for b in range(0, 40):
            g = gcd(a, b)
            assert a % g == 0 and b % g == 0
            for d in range(1, min(a, b or a) + 1):
                if a % d == 0 and b % d == 0:
                    assert d <= g


def test_first_index_of():
    assert first_index_of([3, 1, 4, 1], 1) == 1
    assert first_index_of([3, 1, 4], 9) == -1
    assert first_index_of([], 0) == -1
    assert first_index_of("abca", "a") == 0


def test_is_prime():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 97, 101]
    for p in primes:
        assert is_prime(p), p
    for c in [-7, 0, 1, 4, 6, 8, 9, 15, 21, 25, 91, 100]:
        assert not is_prime(c), c


def test_fizzbuzz():
    assert fizzbuzz(0) == []
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    out = fizzbuzz(15)
    assert out[14] == "FizzBuzz"
    assert len(out) == 15
    assert out.count("Fizz") == 4      # 3, 6, 9, 12 (15 is FizzBuzz)
    assert out.count("Buzz") == 2      # 5, 10


def test_collatz_steps():
    assert collatz_steps(1) == 0
    assert collatz_steps(2) == 1
    assert collatz_steps(3) == 7
    assert collatz_steps(6) == 8
    assert collatz_steps(27) == 111
