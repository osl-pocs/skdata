from IPython.display import HTML, update_display
from matplotlib import pyplot as plt
# from local import
from .data import cross_fields

import base64
import io
import numpy as np
import pandas as pd


def plot2html(
    data: pd.DataFrame, container: object, title: str='Data Analysis',
    **kwargs
) -> [plt.figure]:
    """

    :param data:
    :param container:
    :param kwargs:
    :return:
    """
    with io.BytesIO() as f:
        if 'y' in kwargs:  # multi chart
            # chart with individual data
            y = kwargs['y']  # required
            xs = kwargs['xs']  # required
            bins = kwargs['bins']  # required

            del kwargs['y']
            del kwargs['xs']
            del kwargs['bins']

            k = len(xs)
            cols = 4
            rows = int(np.ceil(k / cols))

            if k < cols:
                rows = 1
                cols = k

            fig, axes = plt.subplots(
                nrows=rows, ncols=cols, squeeze=False,
                figsize=(10, rows*5), **kwargs
            )
            fig.suptitle(title, fontsize=18)

            for i, fc in enumerate(xs):
                # chart settings

                ax = axes.flat[i]

                # create a cross tab
                _data = cross_fields(
                    data=data,
                    y=y,
                    xs=[fc],
                    bins=bins
                )

                _data.plot(
                    ax=ax, legend=True, kind='bar', stacked=True,
                    title='%s x %s' % (y, fc), **kwargs
                )

                ax.grid(True)

                for tick in ax.get_xticklabels():
                    tick.set_rotation(45)
        else:
            # chart with grouped data
            ax = plt.figure().gca()
            data.plot(ax=ax, legend=True, **kwargs)

            ax.grid(True)

            for tick in ax.get_xticklabels():
                tick.set_rotation(45)

        plt.tight_layout(h_pad=3)
        plt.subplots_adjust(top=0.89)
        plt.savefig(f)

        f.seek(0)
        img = base64.b64encode(f.getvalue()).decode('utf8')

        try:
            plt.close()
        except:
            pass
    container.value = '<img src="data:image/png;base64,%s">' % img
