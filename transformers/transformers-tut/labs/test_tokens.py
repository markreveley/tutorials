"""Tests for labs/tokens.py. The toy BPE tests need only the standard library."""
import os
import unittest

from _impl import have, load

tokens = load('tokens')
CORPUS = {'hug': 10, 'pug': 5, 'pun': 12, 'bun': 4, 'hugs': 5}


class ToyBPE(unittest.TestCase):
    def test_pair_counts_weights_by_word_count(self):
        words = {tuple(w): c for w, c in CORPUS.items()}
        counts = tokens.pair_counts(words)
        self.assertEqual(counts[('u', 'g')], 20)   # hug 10 + pug 5 + hugs 5
        self.assertEqual(counts[('u', 'n')], 16)   # pun 12 + bun 4
        self.assertEqual(counts[('g', 's')], 5)
        self.assertNotIn(('g', 'u'), counts)

    def test_merge_pair_replaces_every_adjacent_occurrence(self):
        words = {('h', 'u', 'g'): 10, ('h', 'u', 'g', 's'): 5, ('u', 'g', 'u', 'g'): 1}
        merged = tokens.merge_pair(words, ('u', 'g'))
        self.assertEqual(merged, {('h', 'ug'): 10, ('h', 'ug', 's'): 5, ('ug', 'ug'): 1})

    def test_first_three_merges_match_the_pencil_example(self):
        self.assertEqual(tokens.train_bpe(CORPUS, 3), [('u', 'g'), ('u', 'n'), ('h', 'ug')])

    def test_merges_stop_when_nothing_is_left_to_merge(self):
        self.assertEqual(tokens.train_bpe({'ab': 1}, 5), [('a', 'b')])

    def test_encode_applies_merges_in_order(self):
        merges = tokens.train_bpe(CORPUS, 3)
        self.assertEqual(tokens.bpe_encode('hugs', merges), ['hug', 's'])
        self.assertEqual(tokens.bpe_encode('bug', merges), ['b', 'ug'])
        self.assertEqual(tokens.bpe_encode('pun', merges), ['p', 'un'])
        self.assertEqual(tokens.bpe_encode('x', merges), ['x'])


@unittest.skipUnless(have('transformers'), 'transformers is not installed; GPT-2 tokenizer drills skipped')
class GPT2Tokenizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.setdefault('HF_HUB_OFFLINE', '1')
        from transformers import AutoTokenizer
        cls.tok = AutoTokenizer.from_pretrained('gpt2')

    def test_pieces_keep_leading_spaces(self):
        got = tokens.pieces('The cat sat on the mat', self.tok)
        self.assertEqual([p for _, p in got], ['The', ' cat', ' sat', ' on', ' the', ' mat'])
        self.assertEqual([i for i, _ in got], [464, 3797, 3332, 319, 262, 2603])

    def test_space_changes_the_token(self):
        self.assertNotEqual(tokens.pieces('the', self.tok), tokens.pieces(' the', self.tok))
        self.assertEqual(tokens.pieces(' the', self.tok), [(262, ' the')])

    def test_token_span_aligned_and_misaligned(self):
        text = 'The cat sat on the mat'
        self.assertEqual(tokens.token_span(text, 3, 7, self.tok), (1, 1, True))    # ' cat' is exactly token 1
        self.assertEqual(tokens.token_span(text, 4, 7, self.tok), (1, 1, False))   # 'cat' without its space is not a token boundary
        self.assertEqual(tokens.token_span(text, 0, 7, self.tok), (0, 1, True))    # 'The cat' spans tokens 0-1
        first, last, aligned = tokens.token_span('Unbelievable', 2, 5, self.tok)   # 'bel' inside 'Un|bel|iev|able'
        self.assertEqual((first, last, aligned), (1, 1, True))


if __name__ == '__main__':
    unittest.main()
