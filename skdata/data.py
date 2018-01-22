import numpy as np
import pandas as pd


METHODS = [
    'add', 'sub', 'mul', 'floordiv', 'div', 'truediv', 'mod',
    'divmod', 'pow', 'lshift', 'rshift', 'and', 'or', 'xor'
]

_df = pd.DataFrame()
_se = pd.Series()

PANDAS_DATAFRAME_OBJECTS = [
    attr for attr in dir(_df)
    if not attr.startswith('_')
]

PANDAS_DATAFRAME_ATTRIBUTES = [
    attr for attr in PANDAS_DATAFRAME_OBJECTS
    if not callable(getattr(_df, attr))
]

PANDAS_DATAFRAME_METHODS = [
    attr for attr in PANDAS_DATAFRAME_OBJECTS
    if callable(getattr(_df, attr))
]

PANDAS_SERIES_OBJECTS = [
    attr for attr in dir(_se)
    if not attr.startswith('_')
]

PANDAS_SERIES_ATTRIBUTES = [
    attr for attr in PANDAS_SERIES_OBJECTS
    if not callable(getattr(_se, attr))
]

PANDAS_SERIES_METHODS = [
    attr for attr in PANDAS_SERIES_OBJECTS
    if callable(getattr(_se, attr))
]


def overload_public_attribute(instance, name):
    """

    """

    @property
    def __target__(self, *args, **kwargs):
        """

        """
        return getattr(self.data, name)

    setattr(instance, name, __target__)


def overload_public_method(instance, name):
    """

    """

    def __target__(self, *args, **kwargs):
        """

        """
        if not 'inplace' in kwargs or not kwargs['inplace']:
            _data = getattr(self.data, name)(*args, **kwargs)

            if isinstance(_data, pd.DataFrame):
                _SkDataObject = SkDataFrame
            elif isinstance(_data, pd.Series):
                _SkDataObject = SkDataSeries
            else:
                raise Exception('Data Type not supported yet.')

            return _SkDataObject(
                getattr(self.data, name)(*args, **kwargs),
                list(self.steps) + ['%s(*%s)' % (name, args)]
            )
        else:
            getattr(self.data, name)(*args, **kwargs),
            self.steps.append('%s(*%s)' % (name, args))
            return None

    setattr(instance, name, __target__)


def overload_private_method(instance, name, register_step=True):
    """

    """

    def __target__(self, *args, **kwargs):
        """

        """
        if not register_step:
            return getattr(self.data, name)(*args, **kwargs)

        if args and isinstance(args[0], SkDataObject):
            args = list(args)
            args[0] = args[0].data
            args = tuple(args)

        return SkDataFrame(
            getattr(self.data, name)(*args, **kwargs),
            list(self.steps) + ['%s(*%s)' % (name, args)]
        )

    setattr(instance, name, __target__)


def overload_private_imethod(instance, name):
    """

    """

    def __target__(self, *args, **kwargs):
        """

        """
        if args and isinstance(args[0], SkDataObject):
            args = list(args)
            args[0] = args[0].data
            args = tuple(args)

        getattr(self.data, name)(*args, **kwargs),
        self.steps.append('%s(*%s)' % (name, args))
        return self

    setattr(instance, name, __target__)


class SkDataObject:
    """

    """
    data = None
    steps = []

    def __getitem__(self, x):
        return getattr(self.data, x)


class SkDataFrame(SkDataObject):
    """

    """
    def __new__(cls, *args, **kwargs):
        """

        """
        overload_public_attribute(cls, 'values')
        overload_private_method(cls, '__repr__', register_step=False)
        overload_private_method(cls, '_repr_html_', register_step=False)

        for method in METHODS:
            overload_private_method(cls, '__%s__' % method)
            overload_private_method(cls, '__r%s__' % method)
            overload_private_imethod(cls, '__i%s__' % method)

        for method in PANDAS_DATAFRAME_METHODS:
            overload_public_method(cls, method)

        return super(SkDataFrame, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], pd.DataFrame):
            self.data = args[0]
            if len(args) > 1:
                self.steps = list(args[1])
        else:
            print(args, kwargs)
            self.data = pd.DataFrame(*args, **kwargs)

    def summary(self):
        return summary(self.data)


class SkDataSeries(SkDataObject):
    """

    """
    def __new__(cls, *args, **kwargs):
        """

        """
        overload_public_attribute(cls, 'values')
        overload_private_method(cls, '__repr__', register_step=False)
        # overload_private_method(cls, '_repr_html_', register_step=False)

        for method in METHODS:
            overload_private_method(cls, '__%s__' % method)
            overload_private_method(cls, '__r%s__' % method)
            overload_private_imethod(cls, '__i%s__' % method)

        for method in PANDAS_DATAFRAME_METHODS:
            overload_public_method(cls, method)

        return super(SkDataSeries, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], pd.Series):
            self.data = args[0]
            if len(args) > 1:
                self.steps = list(args[1])
        else:
            self.data = pd.Series(*args, **kwargs)


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
