"""Tokenization lab: a toy byte-pair encoder, then drills on the real GPT-2 tokenizer.

Implement every function that raises NotImplementedError, then run:

    python -m unittest discover -s labs -p 'test_tokens.py' -v

The toy BPE functions use only the standard library. The GPT-2 drills take a
`tokenizer` argument (transformers.AutoTokenizer.from_pretrained('gpt2')); the
tests skip them when transformers is not installed.
"""


def pair_counts(words):
    """words: {tuple_of_symbols: count}. Return {(a, b): total count} over adjacent symbol pairs."""
    raise NotImplementedError('lesson 01')


def merge_pair(words, pair):
    """Return a new words dict in which every adjacent occurrence of `pair` is replaced by the joined symbol."""
    raise NotImplementedError('lesson 01')


def train_bpe(corpus, n_merges):
    """corpus: {word: count}. Return the list of merges [(a, b), ...] chosen by highest pair count.

    Break ties by the pair that sorts first alphabetically on a + b (the tests use tie-free corpora
    except where they say otherwise). Start from words split into single characters.
    """
    raise NotImplementedError('lesson 01')


def bpe_encode(word, merges):
    """Apply `merges` in order to the characters of `word`; return the resulting list of symbols."""
    raise NotImplementedError('lesson 01')


def pieces(text, tokenizer):
    """Return [(token_id, decoded_piece), ...] for `text` under the GPT-2 tokenizer."""
    raise NotImplementedError('lesson 01')


def token_span(text, start, end, tokenizer):
    """Which tokens cover text[start:end]?

    Return (first_token_index, last_token_index_inclusive, aligned) where `aligned` is True only
    when the character span begins exactly at a token boundary and ends exactly at one.
    Use tokenizer(text, return_offsets_mapping=True) for the character offsets.
    """
    raise NotImplementedError('lesson 01')
