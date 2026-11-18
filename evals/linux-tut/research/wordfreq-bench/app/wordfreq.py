#!/usr/bin/env python3
"""wordfreq: print the N most common words in a text file."""
import sys
from collections import Counter


def count_words(text):
    # BUG: splits on whitespace only, so "The", "the" and "the," are three different words.
    return Counter(text.split())


def top(text, n=3):
    counts = count_words(text)
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def main(argv):
    if len(argv) < 2:
        print("usage: wordfreq.py FILE [N]", file=sys.stderr)
        return 2
    n = int(argv[2]) if len(argv) > 2 else 3
    with open(argv[1], encoding="utf-8") as f:
        for word, count in top(f.read(), n):
            print(f"{count} {word}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
