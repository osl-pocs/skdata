from IPython.display import display
from ipywidgets import widgets, interactive, IntSlider
from matplotlib import pyplot as plt

import pandas as pd

# locals
from .utils import cross_fields, make_chart, summary
from . import cleaning


class DataAnalysisWidget:
    def __init__(
        self, data: pd.DataFrame
    ):
        self._data = data
        self.data = self._data.copy()

    def drop_columns_with_unique_values(self, threshold: int = 0.25):
        """
        Remove columns when the proportion of the set of values is more than 
        the threshold

        :param threshold: 
        :return:

        """
        cleaning.drop_columns_with_unique_values(self.data, threshold)

    def dropna_columns(self, threshold: int=0.15):
        """
        
        :param threshold: 
        :return: 
        """
        cleaning.dropna_columns(self.data, threshold)

    @staticmethod
    def load(filepath: str):
        """
        """
        return DataAnalysisWidget(pd.read_csv(filepath))

    def prepare_data(self, fields: dict):
        """
        fields: {'field_name1': {old_value: new_value}}
        """
        cleaning.prepare_categorical_data(self.data, fields)

    def reset_changes(self):
        self.data = self._data.copy()

    def summary(self):
        return summary(self.data)

    def _interative_show_chart(
        self, field_reference: str, fields_comparison: [str], bins
    ):
        ax = plt.figure().gca()

        _data = cross_fields(
            data=self.data,
            field_reference=field_reference,
            fields_comparison=fields_comparison,
            bins=bins
        )

        display(_data)
        make_chart(data=_data, ax=ax)

    def show_chart(self, field_reference: str, fields_comparison: [str]):

        w_bins = IntSlider(min=2, max=10, value=2)
        w_fields_comparison = widgets.SelectMultiple(
            description='Xs:',
            options=[i for i in self.data.keys()],
            selected_labels=fields_comparison
        )

        w_field_reference = widgets.Dropdown(
            description='Y:',
            options=[i for i in self.data.keys()],
            selected_label=field_reference
        )

        return interactive(
            self._interative_show_chart,
            field_reference=w_field_reference,
            fields_comparison=w_fields_comparison,
            bins=w_bins
        )

    def _interative_show_panel_chart(
        self, field_reference: str, fields_comparison: [str], bins
    ):
        ax = plt.figure().gca()

        _data = cross_fields(
            data=self.data,
            field_reference=field_reference,
            fields_comparison=fields_comparison,
            bins=bins
        )

        display(_data)
        make_chart(data=_data, ax=ax)

    def show_panel_chart(self, field_reference: str):

        w_bins = IntSlider(min=2, max=10, value=2)
        w_field_reference = widgets.Dropdown(
            description='Y:',
            options=[i for i in self.data.keys()],
            selected_label=field_reference
        )
        w_fields_comparison = widgets.SelectMultiple(
            description='Xs:',
            options=[i for i in self.data.keys()],
            selected_labels=[
                i for i in self.data.keys() if not i == field_reference
            ]
        )

        return interactive(
            self._interative_show_panel_chart,
            field_reference=w_field_reference,
            fields_comparison=w_fields_comparison,
            bins=w_bins
        )

    def __repr__(self):
        return ''

