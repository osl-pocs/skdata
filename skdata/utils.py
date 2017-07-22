# -*- coding: utf-8 -*-
from IPython.display import display, HTML, update_display
from matplotlib import pyplot as plt

import base64
import io
import numpy as np
import pandas as pd


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


def plot2html(df: pd.DataFrame, display_id, **kwargs) -> [plt.figure]:
    """
    fields name from db

    :param df:
    :param kwargs:
    :return:
    """
    with io.BytesIO() as f:
        if 'field_reference' in kwargs:  # multi chart
            axs = plt.figure().subplot()

        else:
            ax = plt.figure().gca()

            df.plot(ax=ax, legend=True, **kwargs)

            ax.grid(True)

            for tick in ax.get_xticklabels():
                tick.set_rotation(45)

        plt.tight_layout()
        plt.savefig(f)

        f.seek(0)
        img = base64.b64encode(f.getvalue()).decode('utf8')

        plt.close()

    update_display(
        HTML('<img src="data:image/png;base64,%s">' % img),
        display_id=display_id
    )
