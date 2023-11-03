#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List

from epyk.core.py import primitives, types
from epyk.core.html import Html
from epyk.core.html.mixins import MixHtmlState
from epyk.core.html.options import OptTableDatatable
from epyk.core.js.packages import JsDatatable
from epyk.core.js import JsUtils
from epyk.core.js.html import JsHtml

# The list of CSS classes
from epyk.core.css.styles import GrpClsTable

# External DataTable extensions added on demand to add some extra features
# Details of the different extensions are available on the different websites
# https://datatables.net/extensions/
extensions = {
    'rowsGroup': {'jsImports': ['datatables-rows-group']},
}


class Table(MixHtmlState.HtmlOverlayStates, Html.Html):
    requirements = ('datatables',)
    name = 'Table'
    _option_cls = OptTableDatatable.TableConfig

    def __init__(self, page: primitives.PageModel, records, width, height, html_code, options, profile):
        data, columns, self.__config = [], [], None
        super(Table, self).__init__(page, [], html_code=html_code, profile=profile, options=options,
                                    css_attrs={"width": width, "height": height})
        if records is not None:
            self.options.data = records

    @property
    def dom(self) -> JsHtml.JsHtml:
        """
        Return all the Javascript functions defined for an HTML Component.
        Those functions will use plain javascript available for a DOM element by default.

        Usage::

          div = page.ui.div(htmlCode="testDiv")
          print(div.dom.content)

        :return: A Javascript Dom object.
        """
        if self._dom is None:
            self._dom = JsHtml.JsHtml(component=self, page=self.page)
            self._dom._container = "%s.parentNode.parentNode" % self._dom.element
        return self._dom

    @property
    def style(self) -> GrpClsTable.Datatable:
        """ Property to the CSS Style of the component. """
        if self._styleObj is None:
            self._styleObj = GrpClsTable.Datatable(self)
        return self._styleObj

    @property
    def options(self) -> OptTableDatatable.TableConfig:
        """ Datatable table options. """
        return super().options

    @property
    def tableId(self) -> str:
        """ Return the Javascript variable of the chart. """
        return "window['%s_obj']" % self.htmlCode

    def get_column(self, by_title: str):
        """
        Get the column object from it is title.

        :param by_title:
        """
        for c in self.options.columns:
            if c.title == by_title:
                return c

    @property
    def js(self) -> JsDatatable.DatatableAPI:
        """
        Return the Javascript internal object.

        :return: A Javascript object
        """
        if self._js is None:
            self._js = JsDatatable.DatatableAPI(page=self.page, selector=self.tableId, set_var=False, component=self)
        return self._js

    def define(self, options: types.JS_DATA_TYPES = None, dataflows: List[dict] = None):
        """

        :param options:
        :param dataflows:
        :return:
        """

    def build(self, data: types.JS_DATA_TYPES = None, options: types.OPTION_TYPE = None,
              profile: types.PROFILE_TYPE = False, component_id: str = None,
              stop_state: bool = True, dataflows: List[dict] = None) -> str:
        """

        :param data: A String corresponding to a JavaScript object
        :param options: Optional. Specific Python options available for this component
        :param profile: Optional. A flag to set the component performance storage
        :param component_id: Optional. The component reference (the htmlCode)
        :param stop_state: Remove the top panel for the component state (error, loading...)
        :param dataflows: Chain of data transformations
        """
        if data:
            state_expr = ""
            if stop_state:
                state_expr = ";%s" % self.hide_state(component_id)
            return JsUtils.jsConvertFncs(
                [self.js.clear(),
                 self.js.rows.add(JsUtils.dataFlows(data, dataflows, self.page), update=True),
                 state_expr], toStr=True, profile=profile)

        return '%s = %s.DataTable(%s)' % (
            self.tableId, component_id or self.dom.jquery.varId, self.options.config_js(options))

    def __str__(self):
        self.page.properties.js.add_builders(self.refresh())
        return "<table %s></table>" % (self.get_attrs(css_class_names=self.style.get_classes()))
