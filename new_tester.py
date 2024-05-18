# -*- coding: cp1251 -*-

import pytest
import os
import pandas as pd
from unittest.mock import patch
from contextlib import nullcontext as does_not_raise

from main import InvertedIndex
from utils import encode_delta_single, encode_gamma_single, decode_delta_single, decode_gamma_single


class Tester:
    def test_merge_jsons(self):
        inv_idx = InvertedIndex()
        inv_idx.merge_jsons(['data/meduzalive.json', 'data/naukamsu.json', 'data/spbuniversity.json'])
        assert len(pd.read_json('data/meduzalive.json').rows) + len(pd.read_json('data/naukamsu.json').rows) + len(pd.read_json('data/spbuniversity.json').rows) == len(inv_idx.df)
    
    def test_encode_decode_delta(self):
        assert all(i == decode_delta_single(encode_delta_single(i)) for i in range(100000))

    def test_encode_decode_gamma(self):
        assert all(i == decode_gamma_single(encode_gamma_single(i)) for i in range(100000))

    def pass_find_pass(self):
        inv_idx = InvertedIndex()
        inv_idx.merge_jsons(['data/naukamsu.json'])
        inv_idx.get_inverted_index()
        df = inv_idx.find('Ректор МГУ', encoding=None)
        assert True
    
    def pass_encode_delta_pass(self):
        inv_idx = InvertedIndex()
        inv_idx.merge_jsons(['data/naukamsu.json'])
        inv_idx.get_inverted_index()
        inv_idx.encode_delta()
        assert True

    def pass_encode_gamma(self):
        inv_idx = InvertedIndex()
        inv_idx.merge_jsons(['data/naukamsu.json'])
        inv_idx.get_inverted_index()
        inv_idx.encode_delta()
        assert True

    def test_find(self):
        inv_idx = InvertedIndex()
        inv_idx.merge_jsons(['data/naukamsu.json'])
        inv_idx.get_inverted_index()
        df = inv_idx.find('Ректор МГУ', encoding=None)
        assert all(word in inv_idx.preprocess(row['message']) for idx, row in df.iterrows() for word in inv_idx.preprocess('Ректор МГУ'))