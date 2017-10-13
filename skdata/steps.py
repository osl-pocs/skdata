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

import pandas as pd


def expr(dataset: pd.DataFrame, step: str):
    # aliases
    op = step['operation']
    k = step['column'] if 'column' in step else None
    k_new = k if 'new-column' not in step else step['new-column']
    c_expr = step['expression']

    if op == 'text-transform':
        f_expr = eval('lambda value: %s' % c_expr)
        dataset[k_new] = dataset[k].apply(f_expr)

    elif op == 'categorize':
        params = dict(data=dataset, col_name=k, categories=eval(c_expr))
        params.update(
            {'new_col_name': k_new} if 'new-column' in step else {}
        )
        categorize(**params)

    elif op == 'fill-na':
        fill = c_expr
        if c_expr in ['mean', 'max', 'min', 'median']:
            fill = dataset.eval('%s.%s()' % (k, c_expr))
        dataset[k].fillna(fill, inplace=True)

    elif op == 'drop-na':
        data = dataset  # data is a expression variable
        eval('dropna_%s' % c_expr)

    return dataset


def replace(value: str, replace_dict: dict):
    """
    """
    if not isinstance(value, str):
        return value

    return reduce(
        lambda x, y: x.replace(y, replace_dict[y]), replace_dict, value
    )


def compute(
    datasets: {}, steps: list, start: int = None, end: int = None,
    steps_id: list = None
):
    """

    :param datasets:
    :param steps:
    :param start:
    :param end:
    :param steps_id:
    :return:
    """

    if steps_id is not None:
        _steps = [s for i, s in enumerate(steps) if i in steps_id]
    else:
        _steps = steps[start:end]

    for step in _steps:
        datasets[step['data-set']] = expr(datasets[step['data-set']], step)
