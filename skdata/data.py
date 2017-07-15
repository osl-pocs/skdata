import pandas as pd


class Data:
    _data = None  # original data
    _log = ''

    data = None
    categories = {}

    def __init__(self, data: pd.DataFrame = None, filename: str = None):
        if data is not None:
            self._data = data.copy()
            self.data = data.copy()

    def categorize(
        self, col_name: str=None, categories: dict = None,
        max_categories: float=0.15
    ):
        """

        :param col_name:
        :param categories:
        :param max_categories:
        :return:
        """
        if col_name is None:
            if categories is not None:
                raise Exception(
                    'col_name is None when categories was defined.'
                )
            # create a list of cols with all object columns
            # TODO: apply filter by threshold max_categories
            cols = [
                k for k in self.data.keys()
                if self.data[k].dtype == 'object'
            ]
        else:
            # create a list with col_name
            cols = [col_name]

        for c in cols:
            if categories is not None:
                # assert all keys is a number
                assert all(type(k) in (int, float) for k in categories.keys())
                # replace values using given categories dict
                self.data[c].replace(categories, inplace=True)
                # change column to categorical type
                self.data[c] = self.data[c].astype('category')
                # update categories information
                self.categories.update({c: categories})
            else:
                # change column to categorical type
                self.data[c] = self.data[c].astype('category')
                # change column to categorical type
                self.categories.update({
                    c: dict(enumerate(
                        self.data[c].cat.categories,
                    ))
                })
