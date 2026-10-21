"""Author's reference solution for labs/tokens.py (see labs/ASSESSMENTS.md)."""


def pair_counts(words):
    counts = {}
    for word, count in words.items():
        for pair in zip(word, word[1:]):
            counts[pair] = counts.get(pair, 0) + count
    return counts


def merge_pair(words, pair):
    merged = {}
    for word, count in words.items():
        out, i = [], 0
        while i < len(word):
            if i + 1 < len(word) and (word[i], word[i + 1]) == pair:
                out.append(word[i] + word[i + 1]); i += 2
            else:
                out.append(word[i]); i += 1
        merged[tuple(out)] = merged.get(tuple(out), 0) + count
    return merged


def train_bpe(corpus, n_merges):
    words = {tuple(w): c for w, c in corpus.items()}
    merges = []
    for _ in range(n_merges):
        counts = pair_counts(words)
        if not counts:
            break
        best = max(counts, key=lambda p: (counts[p], [-ord(ch) for ch in ''.join(p)]))
        merges.append(best)
        words = merge_pair(words, best)
    return merges


def bpe_encode(word, merges):
    symbols = list(word)
    for a, b in merges:
        out, i = [], 0
        while i < len(symbols):
            if i + 1 < len(symbols) and symbols[i] == a and symbols[i + 1] == b:
                out.append(a + b); i += 2
            else:
                out.append(symbols[i]); i += 1
        symbols = out
    return symbols


def pieces(text, tokenizer):
    return [(tid, tokenizer.decode([tid])) for tid in tokenizer.encode(text)]


def token_span(text, start, end, tokenizer):
    offsets = tokenizer(text, return_offsets_mapping=True)['offset_mapping']
    covering = [i for i, (s, e) in enumerate(offsets) if s < end and e > start]
    first, last = covering[0], covering[-1]
    aligned = offsets[first][0] == start and offsets[last][1] == end
    return first, last, aligned
