from datetime import datetime
# local from import

from . import cleaning

import h5py
import os
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
    path = ''

    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        return self.data

    def __del__(self):
        self.data.flush()
        self.data.close()

    def __init__(self, file_path: str):
        self.load(file_path)

    def categorize(
        self, dset_id: str, col_name: str=None, categories: dict = None,
        max_categories: float=0.15
    ):
        """

        :param dset_id:
        :param col_name:
        :param categories:
        :param max_categories:
        :return:
        """
        categories = cleaning.categorize(
            data=self.data, col_name=col_name, categories=categories,
            max_categories=max_categories
        )
        dset = self.data[dset_id]

        _categories = {}
        if 'categories' in dset.attr:
            _categories.update(dset.attr['categories'])

        _categories.update(categories)
        dset.attr['categories'] = _categories
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

    def import_from(
        self, source: str, dset_id: str=None,
        index_col: str=None, target_col: str=None
    ):
        """

        :param source: accepts sources as CSV, ...
        :param dset_id: data set id
        :param index_col:
        :param target_col:
        """
        read_from = {
            'csv': pd.read_csv
        }

        try:
            _source = source.split('.')
            ext = _source[-1].lower()
            file_name = _source[-2].lower().split(os.path.sep)[-1]
        except Exception:
            raise Exception('[EE] Please inform a filename with extension.')

        data = read_from[ext](source)

        if dset_id is None:
            dset_id = file_name

        dtypes = np.dtype([
            (k, pandas_dtype_to_hdf5(data[k]))
            for k in list(data.keys())
        ])

        dset = self.data.create_dataset(
            dset_id, shape=(data.shape[0],),
            dtype=dtypes, fillvalue=None
        )

        null_string = ''
        for k in data.keys():
            if data[k].dtype == pd.api.types.pandas_dtype('O'):
                data[k].fillna(null_string, inplace=True)

            dset[k] = data[k]

        dset.attrs['null_string'] = null_string

        if target_col is not None:
            dset.attrs['target'] = target_col

        if index_col is not None:
            dset.attrs['index'] = index_col

        self.log(dset_id=dset_id, message='Data set creation.')

        self.data.flush()

    def get_data(self, dset_id: str):
        dset = self.data[dset_id]

        index_col = dset.attrs['index']

        keys = tuple(
            k for k in dset.dtype.names[:]
            if k not in [index_col]
        )

        df = pd.DataFrame(
            dset[keys], index=dset[index_col]
        )

        for k in df.keys():
            if df[k].dtype == pd.api.types.pandas_dtype('O'):
                df[k] = df[k].str.decode("utf-8")
                df[k].replace(
                    dset.attrs['null_string'], np.nan, inplace=True
                )

        return df

    def load(self, file_path: str):
        self.path = file_path
        self.data = h5py.File(file_path, 'w')

    def log(self, dset_id: str, message: str):
        """

        :param dset_id:
        :param message:
        :return:

        """
        dset_log_id = '_%s_log' % dset_id

        if dset_log_id not in self.data.keys():
            dset = self.data.create_dataset(
                dset_log_id, shape=(1,),
                dtype=np.dtype([
                    ('dt_log', '<i8'),
                    ('message', 'S250')
                ])
            )
        else:
            dset = self.data[dset_id]

        timestamp = np.array(
            datetime.now().strftime("%s")
        ).astype('<i8').view('<M8[s]')

        dset['dt_log'] = timestamp.view('<i8')
        dset['message'] = message
        self.data.flush()

    def summary(self) -> pd.DataFrame:
        """

        :return:
        """
        return summary(self.data)


def pandas_dtype_to_hdf5(d):
    """

    :param d:
    :return:
    """
    return (
        d.dtype if not d.dtype == pd.api.types.pandas_dtype('O') else
        'S%s' % int(d.str.len().max())
    )


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
