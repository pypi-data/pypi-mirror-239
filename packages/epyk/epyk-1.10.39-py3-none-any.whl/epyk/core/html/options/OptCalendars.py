#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core.html.options import Options


class OptionDays(Options):

    @property
    def style(self):
        """ CSS attributes """
        return self.get({})

    @style.setter
    def style(self, css: dict):
        self.set(css)

    @property
    def unit(self):
        """
        Change the unit to the calendar.
        Default is in percentage.

        :prop num: Change the scale
        """
        return self.get(100)

    @unit.setter
    def unit(self, num: float):
        self.set(num)

    @property
    def overload(self):
        """
        Overload style of the day number when workload is above 100%.

        :prop css_attrs: Dictionary. CSS attributes.
        """
        return self.get({})

    @overload.setter
    def overload(self, css_attrs: dict):
        self.set(css_attrs)

    @property
    def number(self):
        """
        CSS Style for the day number.

        :prop css: CSS attributes.
        """
        return self.get({})

    @number.setter
    def number(self, css: dict):
        self.set(css)

    @property
    def today(self):
        """
        CSS Style for the today cell.

        :prop css: CSS attributes
        """
        return self.get({})

    @today.setter
    def today(self, css: dict):
        self.set(css)

    @property
    def header(self):
        """
        CSS Style for the table header.

        :prop css: Dictionary. CSS attributes.
        """
        return self.get({})

    @header.setter
    def header(self, css: dict):
        self.set(css)


class OptionDatePicker(Options):
    pass
