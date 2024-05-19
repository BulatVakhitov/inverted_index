# -*- coding: cp1251 -*-

import pytest
import os
import pandas as pd
from unittest.mock import patch
from contextlib import nullcontext as does_not_raise

from main import InvertedIndex
from utils import encode_delta_single, encode_gamma_single, decode_delta_single, decode_gamma_single


class Tester:
    @pytest.mark.parametrize(
        'paths',
        [
            (['data/meduzalive.json', 'data/naukamsu.json', 'data/spbuniversity.json']),
            (['data/meduzalive.json']),
            ([])
        ]
    )
    def test_merge_jsons(self, paths):
        inv_idx = InvertedIndex()
        inv_idx.merge_jsons(paths)
        len_sum = 0
        for path in paths:
            df = pd.read_json(path)
            df = df.drop(columns=list(set(df.columns) - inv_idx.columns_to_keep))
            df = df[df['message'].notna()]
            df = df[df['message'] != '']
            len_sum += len(df)
        assert len_sum == len(inv_idx.df)
    
    def test_encode_decode_delta(self):
        assert all(i == decode_delta_single(encode_delta_single(i)) for i in range(1, 100000))

    def test_encode_decode_gamma(self):
        assert all(i == decode_gamma_single(encode_gamma_single(i)) for i in range(1, 100000))
    
    @pytest.mark.parametrize(
        'paths, text', 
        [
            (['data/naukamsu.json'], '���'),
            (['data/naukamsu.json'], '������ ���'),
            ([], '������ ���'),
            (['data/naukamsu.json'], ''),
            ([], '')
        ]
    )
    def pass_find(self, paths, text):
        inv_idx = InvertedIndex()
        inv_idx.merge_jsons(paths)
        inv_idx.get_inverted_index()
        df = inv_idx.find(text, encoding=None)
    
    @pytest.mark.parametrize(
        'paths', 
        [
            ['data/naukamsu.json'],
            []
        ]
    )
    def pass_encode_delta(self, paths):
        inv_idx = InvertedIndex()
        inv_idx.merge_jsons(paths)
        inv_idx.get_inverted_index()
        inv_idx.encode_delta()

    @pytest.mark.parametrize(
        'paths', 
        [
            ['data/naukamsu.json'],
            []
        ]
    )
    def pass_encode_gamma(self, paths):
        inv_idx = InvertedIndex()
        inv_idx.merge_jsons(paths)
        inv_idx.get_inverted_index()
        inv_idx.encode_delta()

    @pytest.mark.parametrize(
        'paths, text', 
        [
            (['data/naukamsu.json'], '���'),
            (['data/naukamsu.json'], '������ ���'),
            ([], '������ ���'),
            (['data/naukamsu.json'], ''),
            ([], '')
        ]
    )
    def test_find(self, paths, text):
        inv_idx = InvertedIndex()
        inv_idx.merge_jsons(paths)
        inv_idx.get_inverted_index()
        df = inv_idx.find(text, encoding=None)
        assert all(word in inv_idx.preprocess(row['message']) for idx, row in df.iterrows() for word in inv_idx.preprocess(text))