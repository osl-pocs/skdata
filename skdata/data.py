from datetime import datetime
from odo import odo
# local
from .steps import StepSkData

import h5py
import numpy as np
import os
import pandas as pd
import pickle


class SkData:
    """

    """
    data = None
    sets = {}
    path = ''

    def __del__(self):
        self.data.flush()
        self.data.close()

    def __init__(self, file_path: str):
        self.load(file_path)

    def __getitem__(self, item):
        if item not in self.sets.keys():
            raise Exception('Item not found.')

        return self.sets[item]

    def import_from(
        self, source: str, dset_id: str = None,
        index_col: str = None, target_col: str = None
    ):
        """

        :param source: accepts sources as CSV, ...
        :param dset_id: data set id
        :param index_col:
        :param target_col:

        """
        try:
            file_name = source.split('.')[-2].lower().split(os.path.sep)[-1]
        except Exception:
            raise Exception(
                '[EE] Please inform a filename with extension.')

        data = odo(source=source, target=pd.DataFrame)

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

        self.data.flush()
        self.sets[dset_id] = SkDataSet(self, dset_id)
        self.sets[dset_id].log(message='Data set creation.')

    def load(self, file_path: str):
        self.path = file_path
        self.data = h5py.File(file_path, 'w')

        for dset_id in self.data.keys():
            self.sets[dset_id] = SkDataSet(self, dset_id)


class SkDataSet:
    parent = None
    iid = None
    steps = None
    result = None

    def __init__(self, parent: SkData, iid: str):
        """

        :param parent:
        :param iid:
        """
        self.parent = parent
        self.iid = iid
        self.steps = StepSkData(parent=self)

    def __getitem__(self, item):
        if item not in self.parent.data[self.iid].dtype.names:
            raise Exception('Item not found')

        return SkDataColumn(parent=self, column_name=item)

    def attrs(self, key: str, value: str=None):
        """

        :param key:
        :param value:
        :return:
        """
        if value is None:
            return self.parent.data[self.iid].attrs[key]

        self.parent.data[self.iid].attrs[key] = value

    def attr_update(self, attr: str, value: object):
        """

        :param attr:
        :param value:
        :return:
        """

        attr_obj = self.attr_load(attr, type(value)())

        if isinstance(value, list):
            attr_obj += value
        elif isinstance(value,  dict):
            attr_obj.update(value)
        else:
            raise Exception('Attribute type not identified.')

        self.attr_dump(attr, attr_obj)

    def attr_dump(self, attr: str, value: object):
        """

        :param attr:
        :param value:
        :return:
        """
        dset = self.parent.data[self.iid]
        dset.attrs[attr] = pickle.dumps(value, protocol=0)

    def attr_load(self, attr: str, default: object = {}) -> object:
        """

        :param attr:
        :param default:
        :return:
        """
        dset = self.parent.data[self.iid]

        if attr not in dset.attrs:
            return default

        return pickle.loads(dset.attrs[attr])

    def compute(self):
        self.result = self.steps.compute()
        return self.result.copy()

    def drop_columns(
        self, max_na_values: int = None, max_unique_values: int = None
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
        step = {}

        if max_na_values is not None:
            step = {
                'data-set': self.iid,
                'operation': 'drop-na',
                'expression': '{"max_na_values":%s, "axis": 1}' % max_na_values
            }
        if max_unique_values is not None:
            step = {
                'data-set': self.iid,
                'operation': 'drop-unique',
                'expression': '{"max_unique_values":%s}' % max_unique_values
            }
        self.attr_update(attr='steps', value=[step])

    def dropna(self):
        """
        :return:

        """
        step = {
            'data-set': self.iid,
            'operation': 'drop-na',
            'expression': '{"axis": 0}'
        }

        self.attr_update(attr='steps', value=[step])

    def log(self, message: str):
        """
        @deprecated

        :param message:
        :return:

        """
        dset_log_id = '_%s_log' % self.iid

        if dset_log_id not in self.parent.data.keys():
            dset = self.parent.data.create_dataset(
                dset_log_id, shape=(1,),
                dtype=np.dtype([
                    ('dt_log', '<i8'),
                    ('message', 'S250')
                ])
            )
        else:
            dset = self.parent.data[dset_log_id]

        timestamp = np.array(
            datetime.now().strftime("%s")
        ).astype('<i8').view('<M8[s]')

        dset['dt_log'] = timestamp.view('<i8')
        dset['message'] = message
        self.parent.data.flush()

    def summary(self, compute=False) -> pd.DataFrame:
        """
        :param compute: if should call compute method
        :return:
        """
        if compute or self.result is None:
            self.compute()
        return summary(self.result)


class SkDataColumn:
    parent = None
    column_name = None

    def __init__(self, parent: SkDataSet, column_name: str):
        self.parent = parent
        self.column_name = column_name

    def categorize(
        self, categories: dict = None, max_categories: float = 0.15
    ):
        """

        :param categories:
        :param max_categories:
        :return:

        """
        step = {
            'data-set': self.parent.iid,
            'operation': 'categorize',
            'column': self.column_name,
            'expression': str(categories)  # missing max_categories
        }

        self.parent.attr_update(attr='steps', value=[step])

    def replace(self, dict_map: dict):
        """

        :param dict_map:
        :return:

        """
        step = {
            'data-set': self.parent.iid,
            'operation': 'text-transform',
            'column': self.column_name,
            'expression': 'replace(value, {})'.format(str(dict_map))
        }

        self.parent.attr_update('steps', [step])


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
