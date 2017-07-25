# local from import
from . import cleaning

import pandas as pd
import numpy as np


class SkData:
    """

    """
    _data = None  # original data
    _log = ''

    data = None
    categories = {}
    target = None

    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        return self.data

    def __init__(
        self, data: pd.DataFrame = None, file_path: str = None,
        index_col: str=None, target_col: str=None
    ):
        """

        :param data:
        :param file_path: accepts sources as CSV, ...
        :param index_col:
        :param target_col:
        """
        if data is None:
            if file_path is None:
                raise Exception('[EE] Please inform data object or filename.')

            data = pd.read_csv(file_path, index_col=index_col)

        self._data = data.copy()
        self.data = data.copy()

        if target_col is not None:
            self.target = self.data[target_col]

    def categorize(
        self, col_name: str=None, categories: dict = None,
        max_categories: float=0.15
    ):
        """

        :param col_name:
        :param categories:
        :param max_categories:
        :return:
        """
        categories = cleaning.categorize(
            data=self.data, col_name=col_name, categories=categories,
            max_categories=max_categories
        )
        self.categories.update(categories)
        # TODO: Add log information

    def drop_columns(
        self, max_na_values: int=None, max_unique_values: int=None
    ):
        """
        When max_na_values was informed, remove columns when the proportion of
        total NA values more than max_na_values threshold.

        When max_unique_values was informed, remove columns when the proportion
        of the total of unique values is more than the max_unique_values
        threshold, just for columns with type as object or category.

        :param max_na_values: proportion threshold of max na values
        :param max_unique_values:
        :return:
        """
        if max_na_values is not None:
            cleaning.dropna_columns(
                data=self.data, max_na_values=max_na_values
            )
            # TODO: Add log information

        if max_unique_values is not None:
            cleaning.drop_columns_with_unique_values(
                data=self.data, max_unique_values=max_unique_values
            )
            # TODO: Add log information

    def summary(self) -> pd.DataFrame:
        """

        :return:
        """
        return summary(self.data)


def summary(data: pd.DataFrame) -> pd.DataFrame:
    """

    :param data:
    :return:
    """
    # types
    df = pd.DataFrame(data.dtypes).rename(columns={0: 'Types'})

    # set
    df = pd.merge(
        df, pd.DataFrame(
            data.apply(lambda se: str(sorted(set(se.dropna())))[:1000])
        ).rename(columns={0: 'Set Values'}),
        left_index=True, right_index=True
    )

    # count set
    df = pd.merge(
        df, pd.DataFrame(
            data.apply(lambda se: se.dropna().unique().shape[0])
        ).rename(columns={0: 'Count Set'}),
        left_index=True, right_index=True
    )

    # total observations
    df = pd.merge(
        df, pd.DataFrame(
            data.count()
        ).rename(columns={0: '# Observations'}),
        left_index=True, right_index=True
    )

    # total of nan
    df = pd.merge(
        df, pd.DataFrame(data.isnull().sum()).rename(columns={0: '# NaN'}),
        left_index=True, right_index=True
    )
    return df


def cross_fields(
    data: pd.DataFrame,
    y: str,
    xs: [str],
    bins: int
) -> pd.DataFrame:
    """

    :param data:
    :param y:
    :param xs:
    :param bins:
    :return:
    """
    if not (xs and y):
        return data

    d = data[list(xs)+[y]].copy()
    for x in list(xs)+[y]:
        try:
            # if the data is not a number type() will raise an exception
            if isinstance(data[x].dtype.type(), np.number):
                d[x], _ = pd.cut(data[x].copy(), bins=bins, retbins=True)
        except:
            pass

    return pd.crosstab([d[f] for f in xs], d[y])
