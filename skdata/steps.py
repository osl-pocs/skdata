"""
SkData Steps

The OpenRefine json file for steps was used as reference:

[
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column Sex using expression
                    grel:if(value == 'male', 1, 0)",
    "engineConfig": {
      "mode": "row-based",
      "facets": []
    },
    "columnName": "Sex",
    "expression": "grel:if(value == 'male', 1, 0)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10
  }
]

SkData Steps format proposed:
[
  {
    'data-set': 'data_set_name', // required
    // required
    'operation': 'categorize|text-transform|fill-na|drop-na|drop-unique',
    'column': 'column_name',  // optional
    'new-column': 'new_column_name', // optional
    'expression': 'dict|inline-if' // required
  }
]

Variables available for expressions:

* data: entire dataset
* value: used when apply a method for each row

"""
from functools import reduce
# local
from .cleaning import *

import json
import numpy as np
import pandas as pd


class StepSkData:
    parent = None

    def __init__(self, parent: 'SkDataSet'):
        """

        :param parent:
        """
        self.parent = parent

    def compute(
        self, start: int = None, end: int = None,
        steps_id: list = None
    ) -> pd.DataFrame:
        """

        :param start:
        :param end:
        :param steps_id:
        :return:

        """
        dset = self.parent.parent.data[self.parent.iid]

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

        steps = self.parent.attr_load(attr='steps', default=[])

        if steps_id is not None:
            _steps = [s for i, s in enumerate(steps) if i in steps_id]
        else:
            _steps = steps[start:end]

        for step in _steps:
            df = self.expr(df, step)

        return df

    def export_steps(self, file_path: str, mode: str = 'a'):
        """

        :param file_path:
        :param mode: [a]ppend|[w]rite
        :return:

        """
        pass

    @staticmethod
    def expr(data: pd.DataFrame, step: str):
        # aliases
        op = step['operation']
        k = step['column'] if 'column' in step else None
        k_new = k if 'new-column' not in step else step['new-column']
        c_expr = step['expression']

        if op == 'text-transform':
            f_expr = eval('lambda value: %s' % c_expr)
            data[k_new] = data[k].apply(f_expr)

        elif op == 'categorize':
            params = dict(data=data, col_name=k, categories=eval(c_expr))
            params.update(
                {'new_col_name': k_new} if 'new-column' in step else {}
            )
            categorize(**params)

        elif op == 'fill-na':
            fill = c_expr
            if c_expr in ['mean', 'max', 'min', 'median']:
                fill = data.eval('%s.%s()' % (k, c_expr))
            data[k].fillna(fill, inplace=True)

        elif op == 'drop-na':
            params = eval(c_expr)
            dropna(data, **params)

        elif op == 'drop-unique':
            params = eval(c_expr)
            drop_columns_with_unique_values(data, **params)

        return data

    def import_steps(self, file_path: str, mode: str='a'):
        """

        :param file_path:
        :param mode: [a]ppend|[w]rite
        :return:

        """
        steps_json = json.load(file_path)


def replace(value: str, replace_dict: dict):
    """
    """
    if not isinstance(value, str):
        return value

    return reduce(
        lambda x, y: x.replace(y, replace_dict[y]), replace_dict, value
    )
