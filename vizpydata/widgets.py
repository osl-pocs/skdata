# -*- coding: utf-8 -*-
from IPython.display import display, HTML
from ipywidgets import widgets, interactive, IntSlider
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
import textwrap
import traceback

# locals
from vizpydata.utils import cross_fields, make_chart, summary


class DataAnalysisWidget:
    def __init__(
        self, data: pd.DataFrame
    ):
        self.data = data.copy()
        
    @staticmethod
    def load(filepath: str):
        """
        """
        return DataAnalysisWidget(pd.read_csv(filepath))

    
    def prepare_data(self, fields: dict):
        """
        fields: {'field_name1': {old_value: new_value}}
        """
        # Survived field
        _df = self.data.copy()
        
        # iterate over fields
        for i_field, v_field in fields.items():
            # iterate over labels
            for old_label, new_label in v_field.items():
                _mask = _df[i_field]==old_label
                self.data.loc[_mask, i_field] = new_label
            self.data[i_field] = self.data[i_field].astype(
                'category', categories=list(set(self.data[i_field].dropna()))
            )
    
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

