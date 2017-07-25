from abc import ABCMeta, abstractmethod
from IPython.display import display, update_display
from ipywidgets import widgets, IntSlider

# locals from import
from .utils import plot2html
from .data import cross_fields
from .data import SkData

import numpy as np
import pandas as pd


class SkDataWidget:
    """

    """
    layout = {}
    controllers = {}

    def __call__(self, *args, **kwargs):
        # show dashboard
        return self.display(*args, **kwargs)

    def __init__(
        self, skd: SkData, settings: dict={}
    ):
        """

        :param skd:
        :param settings: dictionary
        """
        self.settings = settings
        self.skd = skd

        # settings
        if 'title' not in self.settings:
            self.settings['title'] = 'Data Analysis'

        chart_settings = self.settings.pop('chart', {})
        table_settings = self.settings.pop('table', {})

        self.register_controller(
            chart=SkDataChartController(self, chart_settings)
        )
        self.register_controller(
            table=SkDataTableController(self, table_settings)
        )


    def _(self, name: str):
        """
        Return layout object

        :param name:
        :return:
        """
        return self.layout[name]

    def _display_result(self, **kwargs):
        """

        :param kwargs: kwargs could receive these parameters:
            y, xs, bins, chart_type
        :return:
        """
        # get controller
        chart = self.controllers['chart']
        table = self.controllers['table']

        # widget value is the default value
        y = kwargs.pop('y', self._('y').value)
        xs = kwargs.pop('xs', self._('xs').value)
        bins = kwargs.pop('bins', self._('bins').value)
        chart_type = kwargs.pop('chart_type', self._('chart_type').value)

        table.display(
            y=y,
            xs=xs,
            bins=bins,
            display_id=self.settings['display_chart_id']
        )

        chart.display(
            y=y,
            xs=xs,
            bins=bins,
            chart_type=chart_type,
            display_id=self.settings['display_chart_id']
        )

        # disable slider bins if no fields are numerical
        fields = [y] + list(xs)
        dtypes = self.skd.data[fields].dtypes.values
        visibility = {True: 'visible', False: 'hidden'}

        self._('bins').layout.visibility = visibility[
            float in dtypes or int in dtypes
        ]

    def get_data(self) -> pd.DataFrame:
        """

        :return:
        """
        return self.skd.data

    def build_layout(self):
        """

        :return:
        """
        all_fields = list(self.skd().keys())

        if self.skd.target is None:
            field_reference = all_fields[0]
        else:
            field_reference = self.skd.target.name

        fields_comparison = [all_fields[1]]

        # display ids
        self.settings['display_table_id'] = (
            'table_id_%s' % np.random.randint(10000)
        )
        self.settings['display_chart_id'] = (
            'chart_id_%s' % np.random.randint(10000)
        )

        # chart type widget
        self.register_widget(
            chart_type=widgets.RadioButtons(
                options=['individual', 'grouped'],
                value='individual',
                description='Chart Type:'
            )
        )

        # bins widget
        self.register_widget(
            bins=IntSlider(
                description='Bins:',
                min=2, max=10, value=2,
                continuous_update=False
            )
        )

        # fields comparison widget
        self.register_widget(
            xs=widgets.SelectMultiple(
                description='Xs:',
                options=[f for f in all_fields if not f == field_reference],
                value=fields_comparison
            )
        )

        # field reference widget
        self.register_widget(
            y=widgets.Dropdown(
                description='Y:',
                options=all_fields,
                value=field_reference
            )
        )
        # used to internal flow control
        y_changed = [False]

        self.register_widget(
            box_filter_panel=widgets.HBox([
                self._('y'), self._('xs'), self._('bins')
            ])
        )

        # layout widgets
        self.register_widget(
            table=widgets.Output(),
            chart=widgets.Output()
        )

        self.register_widget(vbox_chart=widgets.VBox([
            self._('chart_type'), self._('chart')
        ]))

        self.register_widget(
            accordion=widgets.Accordion(
                children=[self._('table'), self._('vbox_chart')]
            )
        )

        # observe hooks
        def w_y_change(change: dict):
            """
            When y field was changed xs field should be updated and data table
            and chart should be displayed/updated.

            :param change:
            :return:
            """
            # remove reference field from the comparison field list
            _xs = [
                f for f in all_fields
                if not f == change['new']
            ]

            y_changed[0] = True  # flow control variable
            _xs_value = list(self._('xs').value)

            if change['new'] in self._('xs').value:
                _xs_value.pop(_xs_value.index(change['new']))
                if not _xs_value:
                    _xs_value = [_xs[0]]

            self._('xs').options = _xs
            self._('xs').value = _xs_value

            self._display_result(y=change['new'])

            y_changed[0] = False  # flow control variable

        # widgets registration

        # change accordion settings
        self._('accordion').set_title(0, 'Data')
        self._('accordion').set_title(1, 'Chart')

        # data panel
        with self._('accordion').children[0]:
            display('', display_id=self.settings['display_table_id'])

        # chart panel
        with self._('accordion').children[1].children[1]:
            display('', display_id=self.settings['display_chart_id'])

        # create observe callbacks
        self._('bins').observe(
            lambda change: self._display_result(bins=change['new']),
            'value'
        )
        self._('y').observe(w_y_change, 'value')
        # execute display result if 'y' was not changing.
        self._('xs').observe(
            lambda change: self._display_result(xs=change['new'])
                if not y_changed[0] else None,
            'value'
        )
        self._('chart_type').observe(
            lambda change: self._display_result(chart_type=change['new']),
            'value'
        )

    def display(self):
        """

        :return:

        """
        # build layout
        self.build_layout()

        # display widgets
        display(self._('box_filter_panel'), self._('accordion'))

        # display data table and chart
        self._display_result()

    def register_controller(self, **kwargs):
        """
        This method should receive objects as SkDataController instance.

        :return:
        """
        self.controllers.update(kwargs)

    def register_widget(self, **kwargs):
        """
        This method should receive objects as ipywidgets.Widgets instance

        :return:
        """
        self.layout.update(kwargs)

    def __repr__(self):
        return ''


class SkDataController:
    __metaclass__ = ABCMeta

    def __init__(self, parent, settings: dict={}):
        self.parent = parent
        self.settings = settings

    @abstractmethod
    def display(self):
        """
        This method should be overwritten.
        :return:
        """
        pass


class SkDataChartController(SkDataController):
    def __init__(self, parent, settings: dict={}):
        super(self.__class__, self).__init__(parent, settings)

        # default settings
        if 'sharey' not in self.settings:
            self.settings.update({'sharey': True})

    def display(
        self,
        y: str,  # field_reference
        xs: list,  # fields_comparison
        bins: int,
        chart_type: str,
        display_id: str
    ):
        """

        :param y:
        :param xs:
        :param bins:
        :param chart_type:
        :param display_id:
        :return:
        """
        chart_param = self.settings
        w_chart = self.parent.layout['chart']

        if chart_type == 'grouped':
            # create a cross tab
            d = cross_fields(
                data=self.parent.get_data(),
                y=y, xs=xs, bins=bins
            )
        else:
            d = self.parent.get_data()
            chart_param.update(dict(
                y=y, xs=xs, bins=bins
            ))

        # display chart
        with w_chart:
            plot2html(
                data=d,
                display_id=self.parent.settings['display_chart_id'],
                title=self.parent.settings['title'],
                **chart_param
            )


class SkDataTableController(SkDataController):
    # display data and chart
    def display(
        self, y: str, xs: list or tuple, bins: int, display_id: str
    ):
        """

        :param xs:
        :param bins:
        :param chart_type:
        :param display_id:
        :return:
        """
        w_table = self.parent.layout['table']
        # create a cross tab
        d = cross_fields(data=self.parent.get_data(), y=y, xs=xs, bins=bins)

        # display data table
        with w_table:
            update_display(
                d, display_id=self.parent.settings['display_table_id']
            )
