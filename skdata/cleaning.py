import pandas as pd


def categorize(
    data, col_name: str = None, new_col_name: str = None,
    categories: dict = None, max_categories: float = 0.15
):
    """
    :param data:
    :param col_name:
    :param new_col_name:
    :param categories:
    :param max_categories: max proportion threshold of categories
    :return: new categories
    :rtype dict:
    """

    _categories = {}
    if col_name is None:
        if categories is not None:
            raise Exception(
                'col_name is None when categories was defined.'
            )
        # create a list of cols with all object columns
        cols = [
            k for k in data.keys()
            if data[k].dtype == 'object' and
            (data[k].unique() / data[k].count()) <= max_categories
        ]
    else:
        # create a list with col_name
        if new_col_name is not None:
            data[new_col_name] = data[col_name]
            col_name = new_col_name

        cols = [col_name]

    for c in cols:
        if categories is not None:
            # assert all keys is a number
            assert all(type(k) in (int, float) for k in categories.keys())
            # replace values using given categories dict
            data[c].replace(categories, inplace=True)
            # change column to categorical type
            data[c] = data[c].astype('category')
            # update categories information
            _categories.update({c: categories})
        else:
            # change column to categorical type
            data[c] = data[c].astype('category')
            # change column to categorical type
            _categories.update({
                c: dict(enumerate(
                    data[c].cat.categories,
                ))
            })
    return _categories


def dropna(data: pd.DataFrame, axis: int, **params):
    """
    Remove columns with more NA values than threshold level

    :param data:
    :param axis:
      Axes are defined for arrays with more than one dimension.
      A 2-dimensional array has two corresponding axes: the first running
      vertically downwards across rows (axis 0), and the second running
      horizontally across columns (axis 1).
      (https://docs.scipy.org/doc/numpy-1.10.0/glossary.html)
    :param params:
    :return:

    """
    if axis == 0:
        dropna_rows(data=data, **params)
    else:
        dropna_columns(data=data, **params)


def dropna_columns(data: pd.DataFrame, max_na_values: int=0.15):
    """
    Remove columns with more NA values than threshold level

    :param data:
    :param max_na_values: proportion threshold of max na values
    :return:

    """
    size = data.shape[0]
    df_na = (data.isnull().sum()/size) >= max_na_values
    data.drop(df_na[df_na].index, axis=1, inplace=True)


def dropna_rows(data: pd.DataFrame, columns_name: str=None):
    """
    Remove columns with more NA values than threshold level

    :param data:
    :param columns_name:
    :return:

    """
    params = {}
    if columns_name is not None:
        params.update({'subset': columns_name.split(',')})
    data.dropna(inplace=True, **params)


def drop_columns_with_unique_values(
    data: pd.DataFrame, max_unique_values: int = 0.25
):
    """
    Remove columns when the proportion
    of the total of unique values is more than the max_unique_values
    threshold, just for columns with type as object or category

    :param data:
    :param max_unique_values:
    :return:

    """
    size = data.shape[0]
    df_uv = data.apply(
        lambda se: (
            (se.dropna().unique().shape[0]/size) > max_unique_values and
            se.dtype in ['object', 'category']
        )
    )
    data.drop(df_uv[df_uv].index, axis=1, inplace=True)
