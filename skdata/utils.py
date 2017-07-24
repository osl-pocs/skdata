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


def plot2html(data: pd.DataFrame, display_id, **kwargs) -> [plt.figure]:
    """

    :param data:
    :param display_id:
    :param kwargs:
    :return:
    """
    with io.BytesIO() as f:
        if 'field_reference' in kwargs:  # multi chart
            field_reference = kwargs['field_reference']
            fields_comparison = kwargs['fields_comparison']
            bins = kwargs['bins']

            del kwargs['field_reference']
            del kwargs['fields_comparison']
            del kwargs['bins']

            k = len(fields_comparison)
            cols = 4
            rows = int(np.ceil(k / cols))

            if k < cols:
                rows = 1
                cols = k

            if k == 1:
                fig, ax = plt.subplots()
                axes = [ax]
            else:
                fig, axes = plt.subplots(rows, cols)

            for i, fc in enumerate(fields_comparison):
                # chart settings

                row = i // cols
                col = i - row * cols

                j = (row, col) if row > 1 else col

                ax = axes[j]

                # create a cross tab
                _data = cross_fields(
                    data=data,
                    field_reference=field_reference,
                    fields_comparison=[fc],
                    bins=bins
                )

                _data.plot(ax=ax, legend=True, **kwargs)

                ax.grid(True)

                for tick in ax.get_xticklabels():
                    tick.set_rotation(45)
        else:
            ax = plt.figure().gca()

            data.plot(ax=ax, legend=True, **kwargs)

            ax.grid(True)

            for tick in ax.get_xticklabels():
                tick.set_rotation(45)

        plt.tight_layout()
        plt.savefig(f)

        f.seek(0)
        img = base64.b64encode(f.getvalue()).decode('utf8')

        try:
            plt.close()
        except:
            pass

    update_display(
        HTML('<img src="data:image/png;base64,%s">' % img),
        display_id=display_id
    )
