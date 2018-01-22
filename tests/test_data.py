"""
test_skdata
----------------------------------

Tests for `skdata` module.
"""
# local
from skdata.data import SkDataFrame

import sys
import unittest


class TestData(unittest.TestCase):
    data = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_df(self):
        skdf = SkDataFrame({'a': [1, 5]})

        assert skdf.sum().values[0] == 6
        assert len(skdf.steps) == 0

        skdf / 2
        assert len(skdf.steps) == 0

        skdf += 1
        assert len(skdf.steps) == 1

        skdf = 1 + skdf + 1
        assert len(skdf.steps) == 3


if __name__ == '__main__':
    sys.exit(unittest.main())
