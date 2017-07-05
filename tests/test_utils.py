"""
test_skdata
----------------------------------

Tests for `skdata` module.
"""
# from contextlib import contextmanager
# local
from skdata import utils

import os
import pandas as pd
import sys
import unittest


class TestUtils(unittest.TestCase):
    data = None

    def setUp(self):
        data_path = os.path.dirname(os.path.dirname(__file__))
        data_path = os.path.join(data_path, 'data', 'train.csv')
        self.data = pd.read_csv(data_path, index_col='PassengerId')

    def tearDown(self):
        pass

    def test_000_cross_fields(self):
        data = utils.cross_fields(
            data=self.data,
            field_reference='Survived',
            fields_comparison=['Sex'],
            bins=None
        )

        died = 0
        survived = 1

        assert data[died].female == 81
        assert data[died].male == 468
        assert data[survived].female == 233
        assert data[survived].male == 109


if __name__ == '__main__':
    sys.exit(unittest.main())
