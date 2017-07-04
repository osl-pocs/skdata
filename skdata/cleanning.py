import pandas as pd


def prepare_categorical_data(data: pd.DataFrame, fields: dict):
    """
    fields: {'field_name1': {old_value: new_value}}
    """
    # Survived field
    _df = data.copy()

    # iterate over fields
    for i_field, v_field in fields.items():
        # iterate over labels
        for old_label, new_label in v_field.items():
            _mask = _df[i_field] == old_label
            data.loc[_mask, i_field] = new_label
        data[i_field] = data[i_field].astype(
            'category', categories=list(set(data[i_field].dropna()))
        )


def dropna_columns(data: pd.DataFrame, threshold: int=0.15):
    """
    Remove columns with more NA values than threshold level
    
    :param data: 
    :param threshold: 
    :return:
    
    """
    df_na = (data.isnull().sum() / data.shape[0]) >= threshold
    data.drop(df_na[df_na].index, axis=1, inplace=True)


def drop_columns_with_unique_values(data: pd.DataFrame, threshold: int = 0.25):
    """
    Remove columns when the proportion of the set of values is more than 
    the threshold

    :param data: 
    :param threshold: 
    :return:

    """
    df_uv = data.apply(
        lambda se: (se.dropna().unique().shape[0]/data.shape[0]) > threshold
    )
    data.drop(df_uv[df_uv].index, axis=1, inplace=True)
