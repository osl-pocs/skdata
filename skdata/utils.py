# -*- coding: utf-8 -*-
from IPython.display import display
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
import textwrap
import traceback


def summary(data: pd.DataFrame):
    """
    
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


def make_chart(data: pd.DataFrame, ax: plt.Axes):
    """
    Ex:
    k = ['Sex', 'Survived']
    df[k].groupby(by='Sex').sum()

    """
    try:
        data.plot.bar(ax=ax, stacked=True)

        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
    except:
        t = '<br/>'.join(textwrap.wrap(traceback.format_exc(), 80))
        display(t)
    return ax


def cross_fields(
    data: pd.DataFrame,
    field_reference: str,
    fields_comparison: [str],
    bins: int
) -> pd.DataFrame:
    """

    """
    labels_reference = []
    labels = []

    if not (fields_comparison and field_reference):
        return data

    _data = data[list(fields_comparison)+[field_reference]].copy()
    for f in list(fields_comparison)+[field_reference]:
        try:
            if isinstance(data[f].dtype.type(), np.number):
                _data[f], _ = pd.cut(data[f].copy(), bins=bins, retbins=True)
        except:
            pass

    return pd.crosstab(
        [_data[f] for f in fields_comparison],
        _data[field_reference]
    )

