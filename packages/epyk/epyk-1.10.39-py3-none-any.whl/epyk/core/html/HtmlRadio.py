#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Union, Optional, List
from epyk.core.py import primitives
from epyk.core.py import types

from epyk.core.html import Html

from epyk.core.js.html import JsHtmlSelect
from epyk.core.js import JsUtils
from epyk.core.js.objects import JsComponents

from epyk.core.css import Defaults as cssDefaults
from epyk.core.html import Defaults as htmlDefaults


class Radio(Html.Html):
  name = 'Radio Buttons'

  def __init__(self, page: primitives.PageModel, vals: List[dict], html_code: Optional[str],
               group_name: Optional[str], width: tuple, height: tuple, options: Optional[dict],
               profile: Optional[Union[bool, dict]], verbose: bool = False):
    super(Radio, self).__init__(page, [], html_code=html_code,
                                css_attrs={"width": width, "height": height}, profile=profile, options=options,
                                verbose=verbose)
    self.group_name = group_name or self.htmlCode
    for v in vals:
      self.add(v['value'], v.get('checked', False))

  def add(self, val: Union[Html.Html, str], checked: bool = False):
    """
    Add a value to the radio component.

    :param val: The item to be added
    :param checked: Optional. Check the item
    """
    if not hasattr(val, 'name') or (hasattr(val, 'name') and val.name != 'Radio'):
      val = self.page.ui.inputs.radio(checked, val, group_name="radio_%s" % self.group_name, width=("auto", ""))
    val.set_attrs(name="name", value="radio_%s" % self.htmlCode)
    val.options.managed = False
    super(Radio, self).__add__(val)
    return self

  def set_disable(self, text: str):
    """

    :param text: The item value to disable
    """
    for v in self.val:
      if v.val["text"] == text:
        self.page.properties.js.add_builders(v.dom.attr("disabled", 'true').r)
    return self

  def set_checked(self, text: str):
    """

    :param text: The item value to set as checked
    """
    for v in self.val:
      if v.val["text"] == text:
        v.val["value"] = True
    return self

  @property
  def dom(self) -> JsHtmlSelect.Radio:
    """ HTML Dom object. """
    if self._dom is None:
      self._dom = JsHtmlSelect.Radio(self, page=self.page)
    return self._dom

  def __str__(self):
    row = self.page.ui.layouts.div(self.val)
    row.options.managed = False
    row.style.css.text_align = "inherit"
    return "<div %s>%s</div>%s" % (self.get_attrs(css_class_names=self.style.get_classes()), row.html(), self.helper)


class Tick(Html.Html):
  requirements = (cssDefaults.ICON_FAMILY, )
  name = 'Tick'

  def __init__(self, page: primitives.PageModel, position: str, icon: str, text: str, tooltip: str,
               width: tuple, height: tuple, html_code: str, options: Optional[dict],
               profile: Optional[Union[bool, dict]], verbose: bool = False):
    self._options = options
    super(Tick, self).__init__(page, '', html_code=html_code, profile=profile,
                               css_attrs={"width": width, 'height': height,
                                          'float': 'left' if position is None else position}, verbose=verbose)
    if tooltip is not None:
      self.tooltip(tooltip)
    # Add the internal components icons and helper
    self.add_span(text, css={"float": 'right'})
    self.add_icon(icon, {"color": self.page.theme.success.base, "margin": "2px",
                         'font-size': page.body.style.globals.font.normal()},
                  html_code=self.htmlCode, family=options.get("icon_family"))
    self.icon.style.add_classes.div.background_hover()
    self.css({"margin": "5px 0", 'cursor': 'pointer'})
    self.style.css.float = position
    self.style.css.display = "inline-block"
    self.css({"text-align": "center"})
    if text is not None:
      self.span.css({"line-height": '%spx' % 25, 'vertical-align': 'middle'})
    self.icon.css({"border-radius": "%spx" % 25, "width": "%spx" % 25, "margin-right": "auto", "margin": "auto",
                   "color": 'blue', "line-height": '%s%s' % (25, width[1])})

  @property
  def dom(self) -> JsHtmlSelect.Tick:
    """ HTML Dom object. """
    if self._dom is None:
      self._dom = JsHtmlSelect.Tick(self, page=self.page)
      self._dom.options = self._options
    return self._dom

  def __str__(self):
    return "<span %s></span>" % (self.get_attrs(css_class_names=self.style.get_classes()))


class Switch(Html.Html):
  requirements = ('bootstrap', 'jquery')
  name = 'Switch Buttons'
  builder_name = "HtmlSwitch"

  def __init__(self, page: primitives.PageModel, records: dict, color: str, width: types.SIZE_TYPE,
               height: types.SIZE_TYPE, html_code: str, options: dict, profile: types.PROFILE_TYPE, verbose: bool = False):
    self.width = width[0]
    super(Switch, self).__init__(page, records, html_code=html_code, options=options, profile=profile,
                                 css_attrs={"width": width, "height": height, 'color': color}, verbose=verbose)
    self.style.add_classes.radio.switch_checked()
    self._clicks = {'on': [], 'off': [], "profile": False}

    is_on = options.get("is_on", False)
    self.checkbox = page.ui.inputs.checkbox(is_on, width=(None, "%"))
    self.checkbox.style.add_classes.radio.switch_checkbox()
    self.checkbox.options.managed = False
    if is_on:
      self.checkbox.attr["checked"] = is_on

    self.switch_label = page.ui.texts.label(page.entities.non_breaking_space)
    self.switch_label.style.clear_all(no_default=True)
    self.switch_label.style.css.display = "inline-block"
    #self.switch_label.style.css.top = 4
    self.switch_label.style.css.width = "%spx" % htmlDefaults.INPUTS_TOGGLE_WIDTH
    self.switch_label.style.add_classes.radio.switch_label()
    self.switch_label.options.managed = False
    self.switch_label.style.css.line_height = int(self.page.body.style.globals.line_height / 2)

    self.switch_text = page.ui.tags.p(self.val['on'] if is_on else self.val['off'])
    self.switch_text.css({"display": "inline-block", "margin-left": "3px", "font-weight": "bold", "margin-top": 0})
    self.switch_text.tooltip(self.val.get('text', ''))
    self.switch_text.style.css.font_size = int(self.page.body.style.globals.line_height / 2) + 2
    self.switch_text.options.managed = False
    self.switch_text.style.css.line_height = int(self.page.body.style.globals.line_height / 2) + 2

    self.switch = self.dom.querySelector("label")

  @property
  def on(self):
    """ Change the value displayed when switch on """
    return self._vals["on"]

  @on.setter
  def on(self, value: str):
    self._vals["on"] = value
    if self.checkbox.attr.get("checked") is not None:
      self.switch_text._vals = value

  @property
  def off(self):
    """ Change the value displayed when switch off """
    return self._vals["off"]

  @off.setter
  def off(self, value: str):
    self._vals["off"] = value
    if self.checkbox.attr.get("checked") is None:
      self.switch_text._vals = value

  @property
  def dom(self) -> JsHtmlSelect.JsHtmlSwitch:
    """
    Return all the Javascript functions defined for an HTML Component.

    Those functions will use plain javascript available for a DOM element by default.
    """
    if self._dom is None:
      self._dom = JsHtmlSelect.JsHtmlSwitch(self, page=self.page)
    return self._dom

  @property
  def js(self) -> JsComponents.Switch:
    """
    The Javascript functions defined for this component.

    Those can be specific ones for the module or generic ones from the language.

    :return: A Javascript Dom object.
    """
    if self._js is None:
      self._js = JsComponents.Switch(self, page=self.page)
    return self._js

  def event_fnc(self, event: str):
    """
    Function to get the generated JavaScript method in order to then reuse it in other components.

    This will return the event function in a string already transpiled.

    :param event: The event function.
    """
    return list(self._browser_data['mouse'][event][self.switch.toStr()]["content"])

  def click(self, js_funcs: types.JS_FUNCS_TYPES, profile: types.PROFILE_TYPE = None,
            source_event: str = None, on_ready: bool = False):
    """
    Add click event to the switch component.

    Usage::

      mode_switch = page.ui.fields.toggle({"off": 'hidden', "on": "visible"}, is_on=True, label="", htmlCode="switch")
      mode_switch.input.click([
        page.js.console.log(mode_switch.input.dom.val)
      ])

    :param js_funcs: A Javascript Python function
    :param profile: Optional. Set to true to get the profile for the function on the Javascript console
    :param source_event: Optional. The source target for the event
    :param on_ready: Optional. Specify if the event needs to be trigger when the page is loaded
    """
    if on_ready:
      self.page.body.onReady([self.dom.events.trigger("click")])
    return self.on("click", js_funcs, profile, self.switch.toStr())

  def toggle(self, on_funcs: types.JS_FUNCS_TYPES = None, off_funcs: types.JS_FUNCS_TYPES = None,
             profile: types.PROFILE_TYPE = None, on_ready: bool = False):
    """
    Set the click property for the Switch.

    The toggle event allow specifying different Javascript functions for each states of the component.

    Usage::

      sw = page.ui.buttons.switch({'on': "true", 'off': 'false'})
      sw.toggle([
        page.js.console.log(sw.content)
      ])

    :param on_funcs: Optional. The Javascript functions
    :param off_funcs: Optional. The Javascript functions
    :param profile: Optional. A flag to set the component performance storage
    :param on_ready: Optional. Specify if the event needs to be trigger when the page is loaded
    """
    self._clicks['profile'] = profile
    if on_funcs is not None:
      if not isinstance(on_funcs, list):
        on_funcs = [on_funcs]
      self._clicks['on'].extend(on_funcs)
    if off_funcs is not None:
      if not isinstance(off_funcs, list):
        off_funcs = [off_funcs]
      self._clicks['off'].extend(off_funcs)

  def __str__(self):
    self.page.properties.js.add_builders("var %s_data = %s" % (self.htmlCode, self._vals))
    self.page.properties.js.add_builders(
      self.switch.onclick('''
        var input_check = this.parentNode.querySelector('input');
        if(input_check.checked){
           %(clickOn)s; this.parentNode.querySelector('p').innerHTML = %(htmlCode)s_data.off; 
           input_check.checked = false}
        else {
           %(clickOff)s; input_check.checked = true; 
           this.parentNode.querySelector('p').innerHTML = %(htmlCode)s_data.on}
        ''' % {'clickOn': JsUtils.jsConvertFncs(self._clicks["off"], toStr=True, profile=self._clicks['profile']),
               "htmlCode": self.htmlCode,
               'clickOff': JsUtils.jsConvertFncs(self._clicks["on"], toStr=True, profile=self._clicks['profile'])
               }).toStr())
    return '''
      <div %s>%s %s %s</div>''' % (self.get_attrs(css_class_names=self.style.get_classes()),
                                   self.checkbox.html(), self.switch_label.html(), self.switch_text.html())
