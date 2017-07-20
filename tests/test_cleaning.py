"""
test_skdata
----------------------------------

Tests for `skdata` module.
"""
# from contextlib import contextmanager
# local
from skdata import cleaning

import os
import sys
import pandas as pd
import unittest


class TestCleaning(unittest.TestCase):
    data = None

    def setUp(self):
        data_path = os.path.dirname(os.path.dirname(__file__))
        data_path = os.path.join(data_path, 'data', 'train.csv')
        self.data = pd.read_csv(data_path, index_col='PassengerId')

    def tearDown(self):
        pass

    def test_000_categorize(self):
        _data = self.data.copy()

        survived_dict = {0: 'Died', 1: 'Survived'}
        pclass_dict = {1: 'Upper Class', 2: 'Middle Class', 3: 'Lower Class'}
        embarked_dict = {
            'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'
        }

        _data.Embarked.replace(embarked_dict, inplace=True)

        cleaning.categorize(_data, 'Survived', survived_dict)
        cleaning.categorize(_data, 'Pclass', pclass_dict)
        cleaning.categorize(_data, 'Sex')
        cleaning.categorize(_data, 'Embarked')

        assert _data.Survived.dtype == 'category'
        assert _data.Pclass.dtype == 'category'
        assert _data.Sex.dtype == 'category'
        assert _data.Embarked.dtype == 'category'

    def test_001_drop_columns_with_unique_values(self):
        _data = self.data.copy()

        assert 'Name' in _data.keys()
        assert 'Ticket' in _data.keys()

        cleaning.drop_columns_with_unique_values(data=_data, max_unique_values=0.3)

        assert 'Name' not in _data.keys()
        assert 'Ticket' not in _data.keys()

    def test_002(self):
        _data = self.data.copy()

        assert 'Age' in _data

        cleaning.dropna_columns(data=_data, max_na_values=0.1)

        assert 'Age' not in _data


if __name__ == '__main__':
    sys.exit(unittest.main())
