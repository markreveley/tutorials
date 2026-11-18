"""Lesson 05 — Strings and slicing.

Run: python3 -m pytest exercises/05_strings.py
"""


def split_at(s, k):
    """Return the pair (s[:k], s[k:]).

    Precondition: s is a str, k is any int (in range, out of range, negative).
    Postcondition: a + b == s and, for 0 <= k <= len(s), len(a) == k.
    """
    return s[:k], s[k:]


def every_kth(s, k):
    """Return the same string as s[::k], built without an extended slice.

    Precondition: k >= 1.
    Postcondition: result == s[::k]; len(result) == ceil(len(s) / k).
    Use indexing and ''.join so the build is O(len(s)), not O(len(s)**2).
    """
    out = []
    i = 0
    while i < len(s):
        out.append(s[i])
        i += k
    return "".join(out)


def letter_counts(s):
    """Return a list of 26 ints: how often each of 'a'..'z' occurs in s.

    Precondition: every character of s is a lowercase ASCII letter.
    Postcondition: result[ord(c) - ord('a')] counts c; sum(result) == len(s).
    Index with ord arithmetic, not a dict.
    """
    counts = [0] * 26
    base = ord('a')
    for ch in s:
        counts[ord(ch) - base] += 1
    return counts


def is_anagram(a, b):
    """Return True iff a and b are anagrams of one another.

    Precondition: a and b contain only lowercase ASCII letters.
    Postcondition: True iff the two count vectors agree. Theta(len(a)+len(b)),
    i.e. no sorting.
    """
    if len(a) != len(b):
        return False
    return letter_counts(a) == letter_counts(b)


def is_palindrome_alnum(s):
    """Return True iff s reads the same forwards and backwards.

    Compare only alphanumeric characters, ignoring case.
    Postcondition: O(1) extra space — two pointers, no filtered copy.
    Invariant: the already-compared prefix and suffix are mirror images.
    """
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalnum():
            i += 1
        elif not s[j].isalnum():
            j -= 1
        elif s[i].lower() != s[j].lower():
            return False
        else:
            i += 1
            j -= 1
    return True


def caesar_shift(s, k):
    """Return s with every ASCII letter advanced k places, wrapping a..z.

    Precondition: k is any int, possibly negative or larger than 26.
    Postcondition: case is preserved, non-letters are copied unchanged, and
    caesar_shift(caesar_shift(s, k), -k) == s.
    """
    out = []
    for ch in s:
        if 'a' <= ch <= 'z':
            out.append(chr((ord(ch) - ord('a') + k) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            out.append(chr((ord(ch) - ord('A') + k) % 26 + ord('A')))
        else:
            out.append(ch)
    return "".join(out)


def normalize_spaces(s):
    """Return s with leading/trailing whitespace removed and every internal
    run of whitespace collapsed to a single space.

    Postcondition: the result has no leading, trailing, or doubled spaces,
    and its words equal s.split().
    """
    return " ".join(s.split())


def longest_common_prefix(strs):
    """Return the longest string that is a prefix of every element of strs.

    Precondition: strs is a list of str (possibly empty).
    Postcondition: '' when strs is empty or the strings share no first
    character; otherwise the maximal common prefix. Cost: O(total characters).
    """
    if not strs:
        return ""
    prefix = strs[0]
    for word in strs[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


# ---------------------------------------------------------------- tests

def test_split_at_is_exact():
    for s in ("", "a", "abcdef"):
        for k in range(-8, 9):
            a, b = split_at(s, k)
            assert a + b == s, (s, k, a, b)
    assert split_at("abcdef", 2) == ("ab", "cdef")
    assert split_at("abcdef", -1) == ("abcde", "f")
    assert split_at("abcdef", 99) == ("abcdef", "")


def test_split_at_length_law():
    s = "abcdef"
    for k in range(0, len(s) + 1):
        a, b = split_at(s, k)
        assert len(a) == k
        assert len(b) == len(s) - k


def test_every_kth():
    s = "abcdefgh"
    for k in range(1, 6):
        assert every_kth(s, k) == s[::k], k
    assert every_kth("", 3) == ""
    assert every_kth("abc", 1) == "abc"


def test_letter_counts():
    c = letter_counts("banana")
    assert c[ord('a') - ord('a')] == 3
    assert c[ord('b') - ord('a')] == 1
    assert c[ord('n') - ord('a')] == 2
    assert sum(c) == 6
    assert len(c) == 26
    assert letter_counts("") == [0] * 26


def test_is_anagram():
    assert is_anagram("listen", "silent")
    assert is_anagram("", "")
    assert not is_anagram("rat", "car")
    assert not is_anagram("aab", "abb")
    assert not is_anagram("ab", "abc")


def test_is_palindrome_alnum():
    assert is_palindrome_alnum("A man, a plan, a canal: Panama")
    assert is_palindrome_alnum("")
    assert is_palindrome_alnum(".,")
    assert is_palindrome_alnum("aba")
    assert not is_palindrome_alnum("race a car")


def test_caesar_shift():
    assert caesar_shift("abc", 1) == "bcd"
    assert caesar_shift("xyz", 3) == "abc"
    assert caesar_shift("Hello, World!", 13) == "Uryyb, Jbeyq!"
    assert caesar_shift("abc", -1) == "zab"
    assert caesar_shift("abc", 52) == "abc"
    s = "Attack at Dawn, 06:00!"
    assert caesar_shift(caesar_shift(s, 7), -7) == s


def test_normalize_spaces():
    assert normalize_spaces("  a   b \n c\t") == "a b c"
    assert normalize_spaces("") == ""
    assert normalize_spaces("   ") == ""
    assert normalize_spaces("one") == "one"


def test_longest_common_prefix():
    assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"
    assert longest_common_prefix(["dog", "racecar", "car"]) == ""
    assert longest_common_prefix(["same", "same"]) == "same"
    assert longest_common_prefix(["a"]) == "a"
    assert longest_common_prefix([]) == ""
    assert longest_common_prefix(["", "a"]) == ""
