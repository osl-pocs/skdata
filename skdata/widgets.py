from IPython.display import display, update_display
from ipywidgets import widgets, interactive, IntSlider
from matplotlib import pyplot as plt

# locals from import
from .utils import cross_fields, plot2html
from .data import SkData

import numpy as np


class SkDataWidget:
    """

    """
    def __call__(self, *args, **kwargs):
        # show dashboard
        return self.show_chart(*args, **kwargs)

    def __init__(
        self, skd: SkData
    ):
        """

        :param skd:
        """
        self.skd = skd

    def get_data(self):
        return self.skd()

    def show_chart(
        self, field_reference: str=None, fields_comparison: [str]=None
    ):
        """

        :param field_reference:
        :param fields_comparison:
        :return:

        """
        all_fields = list(self.skd().keys())

        if field_reference is None:
            if self.skd.target is None:
                field_reference = all_fields[0]
            else:
                field_reference = self.skd.target.name

        if fields_comparison is None:
            fields_comparison = [all_fields[1]]

        # display ids
        display_table_id = 'table_id_%s' % np.random.randint(10000)
        display_chart_id = 'chart_id_%s' % np.random.randint(10000)

        # chart type widget
        w_chart_type = widgets.RadioButtons(
            options=['individual', 'grouped'],
            value='individual',
            description='Chart Type:'
        )

        # bins widget
        w_bins = IntSlider(
            description='Bins:',
            min=2, max=10, value=2,
            continuous_update=False
        )

        # fields comparison widget
        w_fields_comparison = widgets.SelectMultiple(
            description='Xs:',
            options=[f for f in all_fields if not f == field_reference],
            value=fields_comparison
        )
        # used to internal flow control
        w_f_reference_changed = [False]

        # field reference widget
        w_field_reference = widgets.Dropdown(
            description='Y:',
            options=all_fields,
            value=field_reference
        )

        w_box_filter_panel = widgets.HBox([
            w_field_reference,
            w_fields_comparison,
            w_bins
        ])

        # layout widgets
        w_out_data = widgets.Output()
        w_out_chart = widgets.Output()

        w_vbox_chart = widgets.VBox([w_chart_type, w_out_chart])

        w_accordion = widgets.Accordion(
            children=[w_out_data, w_vbox_chart]
        )

        def plot_chart(
            _field_reference: str,
            _fields_comparison: list,
            _bins: int,
            _chart_type: str
        ):
            """

            :param _field_reference:
            :param _fields_comparison:
            :param _bins:
            :param _chart_type:
            :return:
            """
            _chart_param = {}

            if _chart_type == 'grouped':
                # create a cross tab
                _data = cross_fields(
                    data=self.skd.data,
                    field_reference=_field_reference,
                    fields_comparison=_fields_comparison,
                    bins=_bins
                )
            else:
                _data = self.get_data()
                _chart_param.update(dict(
                    field_reference=_field_reference,
                    fields_comparison=_fields_comparison,
                    bins=_bins
                ))

            # display chart
            with w_accordion.children[1].children[1]:
                plot2html(
                    data=_data,
                    display_id=display_chart_id,
                    kind='bar',
                    title='Titanic',
                    stacked=True,
                    **_chart_param
                )

        # display data and chart
        def display_data(
            _field_reference: str, _fields_comparison: list or tuple,
            _bins: int, _chart_type: str
        ):
            """

            :param _field_reference:
            :param _fields_comparison:
            :param _bins:
            :param _chart_type:
            :return:
            """
            # create a cross tab
            _data = cross_fields(
                data=self.skd.data,
                field_reference=_field_reference,
                fields_comparison=_fields_comparison,
                bins=_bins
            )

            # display data table
            with w_accordion.children[0]:
                update_display(_data, display_id=display_table_id)

            # display chart
            plot_chart(
                _field_reference,
                _fields_comparison,
                _bins,
                _chart_type
            )

            # disable slider bins if no fields are numerical
            _fields = [_field_reference] + list(_fields_comparison)
            _dtypes = self.skd.data[_fields].dtypes.values
            _visibility = {True: 'visible', False: 'hidden'}

            w_bins.layout.visibility = _visibility[
                float in _dtypes or int in _dtypes
            ]

        def w_chart_type_change(change: dict):
            """

            :param change:
            :return:
            """
            plot_chart(
                w_field_reference.value,
                w_fields_comparison.value,
                w_bins.value,
                change['new']
            )

        # observe hooks
        def w_bins_change(change: dict):
            """

            :param change:
            :return:
            """
            display_data(
                w_field_reference.value,
                w_fields_comparison.value,
                change['new'],
                w_chart_type.value
            )

        def w_f_reference_change(change: dict):
            """

            :param change:
            :return:
            """
            # remove reference field from the comparison field list
            _fields_comparison = [
                f for f in all_fields
                if not f == change['new']
            ]

            w_f_reference_changed[0] = True  # flow control variable
            _comp_value = list(w_fields_comparison.value)

            if change['new'] in w_fields_comparison.value:
                _comp_value.pop(_comp_value.index(change['new']))
                if not _comp_value:
                    _comp_value = [_fields_comparison[0]]

            w_fields_comparison.options = _fields_comparison
            w_fields_comparison.value = _comp_value

            display_data(
                change['new'],
                w_fields_comparison.value,
                w_bins.value,
                w_chart_type.value
            )

            w_f_reference_changed[0] = False  # flow control variable

        def w_f_comparison_change(change: dict):
            """

            :param change:
            :return:
            """
            if not w_f_reference_changed[0]:  # flow control variable
                display_data(
                    w_field_reference.value,
                    change['new'],
                    w_bins.value,
                    w_chart_type.value
                )

        # change accordion settings
        w_accordion.set_title(0, 'Data')
        w_accordion.set_title(1, 'Chart')

        # data panel
        with w_accordion.children[0]:
            display('', display_id=display_table_id)

        # chart panel
        with w_accordion.children[1].children[1]:
            display('', display_id=display_chart_id)

        # create observe callbacks
        w_bins.observe(w_bins_change, 'value')
        w_field_reference.observe(w_f_reference_change, 'value')
        w_fields_comparison.observe(w_f_comparison_change, 'value')
        w_chart_type.observe(w_chart_type_change, 'value')

        # display widgets
        display(w_box_filter_panel, w_accordion)

        # display data table and chart
        display_data(
            w_field_reference.value,
            w_fields_comparison.value,
            w_bins.value,
            w_chart_type.value,
        )

    def __repr__(self):
        return ''
