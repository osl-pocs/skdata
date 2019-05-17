import numpy as np
import pandas as pd
import uuid


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
    Overload public attribute of SkDataObject (SkDataFrame or SkDataSeries).

    The overload occurs on __new__ method.
    """

    @property
    def __target__(self, *args, **kwargs):
        """

        """
        return getattr(self.data, name)

    setattr(instance, name, __target__)


def overload_public_method(instance, name):
    """
    Overload public methods of SkDataObject (SkDataFrame or SkDataSeries).

    The overload occurs on __new__ method.
    """

    def __target__(self, *args, **kwargs):
        """

        """
        step_prefix = (
             '' if isinstance(self.data, pd.DataFrame) else
             '%s.' % self.data.name
        )
        step = (
            uuid.uuid4().hex,
            '%s%s(*%s, **%s)' % (step_prefix, name, args, kwargs)
        )
        result = getattr(self.data, name)(*args, **kwargs)

        if 'inplace' not in kwargs or not kwargs['inplace']:
            if isinstance(result, pd.DataFrame):
                _SkDataObject = SkDataFrame
            elif isinstance(result, pd.Series):
                _SkDataObject = SkDataSeries
            else:
                raise Exception('Data Type not supported yet.')

            return _SkDataObject(
                result, list(self.steps) + [step]
            )
        else:
            # inplace
            self.steps.append(step)
            if hasattr(self, 'parent_steps') and self.parent_steps is not None:
                self.parent_steps.append(step)
            return None

    setattr(instance, name, __target__)


def overload_private_method(instance, name, register_step=True):
    """
    Overload private operation methods of SkDataObject
    (SkDataFrame or SkDataSeries).

    The overload occurs on __new__ method.
    """

    def __target__(self, *args, **kwargs):
        """

        """
        # change from SkDataObject to data (DataFrame or Series)
        if args and isinstance(args[0], SkDataObject):
            args = list(args)
            args[0] = args[0].data
            args = tuple(args)

        step_prefix = (
            '' if isinstance(self.data, pd.DataFrame) else
            '%s.' % self.data.name
        )
        step = (
            uuid.uuid4().hex,
            '%s%s(*%s, **%s)' % (step_prefix, name, args, kwargs)
        )
        result = getattr(self.data, name)(*args, **kwargs)

        if not register_step:
            return result

        if isinstance(result, pd.DataFrame):
            _SkDataObject = SkDataFrame
        elif isinstance(result, pd.Series):
            _SkDataObject = SkDataSeries
        else:
            raise Exception('Data Type not supported yet.')

        return _SkDataObject(
            result, list(self.steps) + [step]
        )

    setattr(instance, name, __target__)


def overload_private_imethod(instance, name):
    """
    Overload private inplace operation methods of SkDataObject
    (SkDataFrame or SkDataSeries).

    The overload occurs on __new__ method.
    """

    def __target__(self, *args, **kwargs):
        """

        """
        # change from SkDataObject to data (DataFrame or Series)
        if args and isinstance(args[0], SkDataObject):
            args = list(args)
            args[0] = args[0].data
            args = tuple(args)

        step_prefix = (
            '' if isinstance(self.data, pd.DataFrame) else
            '%s.' % self.data.name
        )
        step = (
            uuid.uuid4().hex,
            '%s%s(*%s, **%s)' % (step_prefix, name, args, kwargs)
        )

        getattr(self.data, name)(*args, **kwargs)
        self.steps.append(step)

        if hasattr(self, 'parent_steps') and self.parent_steps is not None:
            self.parent_steps.append(step)

        return self

    setattr(instance, name, __target__)


class SkDataObject:
    """

    """
    data = None
    steps = []


class SkDataFrame(SkDataObject):
    """

    """
    series = {}

    def __getitem__(self, item):
        """
        Access to series from DataFrame

        :param item:
        :return:
        """
        if item not in self.series:
            self.series[item] = SkDataSeries(
                self.data[item], parent_steps=self.steps
            )
        return self.series[item]

    def __setitem__(self, key, value):
        """
        Set a series to the  DataFrame

        :param key:
        :param value:
        :return:
        """
        if key not in self.series:
            self.series[key] = SkDataSeries(
                self.data[key], parent_steps=self.steps
            )

        if not isinstance(value, SkDataSeries):
            self.data[key] = value
            series = SkDataSeries(self.data[key], parent_steps=self.steps)
        else:
            series = value
            series.parent_steps = self.steps

            # insert steps from series when needed
            for step_series in series.steps:
                insert_step = True
                for step_df in self.steps:
                    if step_series[0] == step_df[0]:
                        insert_step = False
                        break
                if insert_step:
                    step_series = (
                        step_series[0],
                        '%s = %s' % (key, step_series[1])
                    )
                    self.steps.append(step_series)

        self.series[key] = series

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
            self.data = pd.DataFrame(*args, **kwargs)

    def summary(self):
        return summary(self.data)


class SkDataSeries(SkDataObject):
    """

    """
    parent_steps = None

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
        # internal parameter
        if 'parent_steps' in kwargs:
            self.parent_steps = kwargs.pop('parent_steps')

        if args and isinstance(args[0], pd.Series):
            self.data = args[0]
            if len(args) > 1:
                self.steps = list(args[1])
            else:
                self.steps = []
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
