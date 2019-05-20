"""
test_skdata
----------------------------------

Tests for `skdata` module.
"""
# local
from skdata.data import SkDataFrame as DataFrame

import pandas as pd
import sys
import unittest


class TestData(unittest.TestCase):
    data = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_df_basic(self):
        df = DataFrame({'a': [1, 5]})

        # steps doesn't increased
        assert df.sum().values[0] == 6
        assert len(df.steps) == 0

        # steps doesn't increased
        df / 2
        assert len(df.steps) == 0

        # inplace method increase step
        df += 1
        assert len(df.steps) == 1

        # df receive df (1 step) more 2 private operation (add)
        df = 1 + df + 1
        assert len(df.steps) == 3

    def test_titanic(self):
        df = DataFrame(
            pd.read_csv('./data/train.csv', index_col='PassengerId')
        )

        df['Sex'].replace({
            'male': 'Male', 'female': 'Female'
        }, inplace=True)

        assert len(df['Sex'].steps) == 1
        assert len(df.steps) == 2

        df['Embarked'].replace({
            'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'
        }, inplace=True)
        
        assert len(df['Embarked'].steps) == 1
        assert len(df['Sex'].steps) == 1
        assert len(df.steps) == 3


        df['Sex'] = df['Sex'].astype('category')

        assert len(df['Embarked'].steps) == 1
        assert len(df['Sex'].steps) == 2
        assert len(df.steps) == 4

        df['Embarked'] = df['Embarked'].astype('category')

        assert len(df['Embarked'].steps) == 2
        assert len(df['Sex'].steps) == 2
        assert len(df.steps) == 5


        # survived_dict = {0: 'Died', 1: 'Survived'}
        # pclass_dict = {1: 'Upper Class', 2: 'Middle Class', 3: 'Lower Class'}
        # df_train['Pclass'].categorize(categories=pclass_dict)
        # df_train['Survived'].categorize(categories=survived_dict)


if __name__ == '__main__':
    sys.exit(unittest.main())
