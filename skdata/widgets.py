from IPython.display import display
from ipywidgets import widgets, interactive, IntSlider
from matplotlib import pyplot as plt

# locals from import
from .utils import cross_fields, make_chart
from .data import SkData


class SkDataWidget:
    """

    """
    def __call__(self, *args, **kwargs):
        return self.skd

    def __init__(
        self, skd: SkData
    ):
        """

        :param skd:
        """
        self.skd = skd

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

        # bins widget
        w_bins = IntSlider(min=2, max=10, value=2)

        # fields comparison widget
        w_fields_comparison = widgets.SelectMultiple(
            description='Xs:',
            options=all_fields,
            selected_labels=fields_comparison
        )
        w_fields_comparison.value = fields_comparison

        # field reference widget
        w_field_reference = widgets.Dropdown(
            description='Y:',
            options=all_fields,
            selected_label=field_reference
        )
        w_field_reference.value = field_reference

        # display data and chart
        ax = plt.figure().gca()

        def display_data(field_reference, fields_comparison, bins):
            _data = cross_fields(
                data=self.skd.data,
                field_reference=field_reference,
                fields_comparison=fields_comparison,
                bins=bins
            )

            display(_data)
            make_chart(data=_data, ax=ax)

        # observe hooks
        def w_bins_change(change):
            display_data(
                w_field_reference.value,
                w_fields_comparison.value,
                change['new']
            )
        w_bins.observe(w_bins_change, 'value')

        def w_f_comparison_change(change):
            display_data(
                w_field_reference.value,
                change['new'],
                w_bins.value
            )
        w_fields_comparison.observe(w_f_comparison_change, 'value')

        def w_f_reference_change(change):
            display_data(
                change['new'],
                w_fields_comparison.value,
                w_bins.value
            )
        w_field_reference.observe(w_f_reference_change, 'value')

        display(
            w_field_reference,
            w_fields_comparison,
            w_bins
        )

        display_data(
            w_field_reference.value,
            w_fields_comparison.value,
            w_bins.value
        )

    def _interactive_show_panel_chart(
        self, field_reference: str, fields_comparison: [str], bins
    ):
        """

        :param field_reference:
        :param fields_comparison:
        :param bins:
        :return:
        """
        ax = plt.figure().gca()

        _data = cross_fields(
            data=self.skd.data,
            field_reference=field_reference,
            fields_comparison=fields_comparison,
            bins=bins
        )

        display(_data)
        make_chart(data=_data, ax=ax)

    def show_panel_chart(self, field_reference: str):
        """

        :param field_reference:
        :return:
        """
        w_bins = IntSlider(min=2, max=10, value=2)
        w_field_reference = widgets.Dropdown(
            description='Y:',
            options=[i for i in self.skd.data.keys()],
            selected_label=field_reference
        )
        w_fields_comparison = widgets.SelectMultiple(
            description='Xs:',
            options=[i for i in self.skd.data.keys()],
            selected_labels=[
                i for i in self.skd.data.keys() if not i == field_reference
            ]
        )

        return interactive(
            self._interactive_show_panel_chart,
            field_reference=w_field_reference,
            fields_comparison=w_fields_comparison,
            bins=w_bins
        )

    def __repr__(self):
        return ''
