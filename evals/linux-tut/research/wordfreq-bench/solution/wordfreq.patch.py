# Oracle solution: the body of count_words() after the fix.
import re
from collections import Counter


def count_words(text):
    return Counter(re.findall(r"[a-z]+(?:'[a-z]+)*", text.lower()))
