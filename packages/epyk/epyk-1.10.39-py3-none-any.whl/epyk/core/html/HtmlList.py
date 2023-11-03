#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
List of all the different templates configurations available for displaying bespoke lists.
This list can be extended and it is easy to test a new configuration by different defining the HTML template in the
common list object.
List are standard and very popular HTML objects, please have a look at the below websites if you need further
information to manipulate them in your report
"""

from typing import Union, Optional
from typing import List as type_List
from epyk.core.py import primitives
from epyk.core.py import types

from epyk.core.js import Imports
from epyk.core.js import JsUtils
from epyk.core.js.packages import JsQuery
from epyk.core.html import Html
from epyk.core.html.options import OptList

# The list of Javascript classes
from epyk.core.js.html import JsHtml
from epyk.core.js.html import JsHtmlList

from epyk.core.css.styles import GrpClsList


class Li(Html.Html):
  name = 'Entries'

  def __init__(self, page: primitives.PageModel, text: Union[str, Html.Html], options: dict = None,
               html_code: str = None):
    super(Li, self).__init__(page, text, html_code=html_code)
    if options is not None:
      self.item_type = options.get("item_type", "li")
    else:
      self.item_type = "li"
    if hasattr(text, 'options'):
      text.options.managed = False
    self.css({'font-size': 'inherit', 'margin': "1px 5px", 'padding': 0})

  def __add__(self, component: Html.Html):
    """ Add items to a container """
    if not hasattr(component, 'options'):
      raise ValueError("This can only be used for HTML components")

    self.set_html_content(component)
    return self

  def no_decoration(self):
    """ Remove the list default style. """
    self.css({"text-decoration": "none", "list-style-type": 'none'})
    return self

  def add_label(self, text: str, css: Optional[dict] = None, position: str = "before",
                for_: Optional[Html.Html] = None, html_code: Optional[str] = None,
                options: Optional[dict] = None):
    """
    Add an elementary label component.

    Related Pages:

      https://www.w3schools.com/tags/tag_label.asp

    :param text: The label content
    :param css: Optional. A dictionary with the CSS style to be added to the component
    :param position: Optional. The position
    :param for_: Optional. Specifies which form element a label is bound to
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    """
    self.label = ""
    if text is not None:
      dfl_css = {"float": 'none', 'width': 'none'}
      if css is not None:
        dfl_css.update(css)
      html_code_label = "%s_label" % html_code if html_code is not None else html_code
      self.label = self.page.ui.texts.label(text, options=options, html_code=html_code_label)
      if for_ is not None:
        # Attach the label to another HTML component based on the ID
        self.label.attr['for'] = for_
      if position == "before":
        self.prepend_child(self.label)
      else:
        self.append_child(self.label)
      self.label.css(dfl_css)
    return self

  def set_html_content(self, component: Html.Html):
    """
    Set the cell content to be an HTML object.

    :param component: Python HTML object

    :return: self, the cell object to allow the chaining
    """
    component.options.managed = False
    if self.innerPyHTML is not None:
      if not isinstance(self.innerPyHTML, list):
        self.innerPyHTML = [self.innerPyHTML]
      self.innerPyHTML.append(component)
    else:
      self.innerPyHTML = component
    return self

  def click(self, js_funcs: types.JS_FUNCS_TYPES, profile: types.PROFILE_TYPE = None,
            source_event: Optional[str] = None, on_ready: bool = False):
    """
    Add a click event to the component.

    :param js_funcs: Javascript functions
    :param profile: Optional. A flag to set the component performance storage
    :param source_event: Optional. The source target for the event
    :param on_ready: Optional. Specify if the event needs to be trigger when the page is loaded
    """
    if self.innerPyHTML is not None:
      return self.innerPyHTML.click(js_funcs, profile)

    if not isinstance(js_funcs, list):
      js_funcs = [js_funcs]
    js_funcs.insert(0, self.dom.toggleClass("active"))
    return super(Li, self).click(js_funcs, profile, source_event, on_ready=on_ready)

  @property
  def dom(self) -> JsHtml.JsHtmlLi:
    """
    Return all the Javascript functions defined for an HTML Component.

    Those functions will use plain javascript by default.

    :return: A Javascript Dom object
    """
    if self._dom is None:
      self._dom = JsHtml.JsHtmlLi(self, page=self.page)
    return self._dom

  def __str__(self):
    return "<%(type)s %(attrs)s>%(content)s</%(type)s>" % {
      "type": self.item_type, "attrs": self.get_attrs(css_class_names=self.style.get_classes()),
      "content": self.content}


class List(Html.Html):
  name = 'List'
  _option_cls = OptList.OptionsLi

  def __init__(self, page: primitives.PageModel, data: list, color, width: tuple, height: tuple, html_code: str,
               helper: str, options: dict, profile: types.PROFILE_TYPE):
    super(List, self).__init__(page, [], css_attrs={"width": width, "height": height},
                               html_code=html_code, profile=profile, options=options)
    self.add_helper(helper)
    self.color = color if color is not None else self.page.theme.greys[-1]
    self.css({'padding': 0, 'margin': "1px", 'list-style-position': 'inside'})
    self.items = None
    for item in data:
      self.add_item(item)
    if len(data) > 0:
      self.set_items()

  @property
  def options(self) -> OptList.OptionsLi:
    """
    Property to the component options.

    Options can either impact the Python side or the Javascript builder.

    Python can pass some options to the JavaScript layer.
    """
    return super().options

  @property
  def dom(self) -> JsHtml.JsHtmlList:
    """
    Return all the Javascript functions defined for an HTML Component.

    Those functions will use plain javascript by default.
    """
    if self._dom is None:
      self._dom = JsHtml.JsHtmlList(self, page=self.page)
    return self._dom

  def items_style(self, style_type: str = None, css_attrs: dict = None):
    """
    Function to load a predefined style for the items of the components.

    :param style_type. Optional. The alias of the style to apply
    :param css_attrs. Optional. The CSS attributes
    """
    li_item_style = {}
    if style_type == "bullets":
      li_item_style.update({
        "display": 'inline-block', 'padding': '0 5px', 'margin-right': '2px', 'background': self.page.theme.greys[2],
        'border': '1px solid %s' % self.page.theme.greys[2], 'border-radius': '10px'})
    if css_attrs is not None:
      li_item_style.update(css_attrs)
    self.options.li_css = li_item_style
    self.set_items()
    for item in self.items:
      item.css(self.options.li_css)
    return self

  def drop(self, js_funcs: types.JS_FUNCS_TYPES = None, prevent_default: bool = True,
           profile: types.PROFILE_TYPE = None):
    """
    Add a drop feature to the component.

    :param js_funcs: Javascript functions
    :param prevent_default: Optional. Cancels the event if it is cancelable, meaning that the default action
      that belongs to the event will not occur
    :param profile: Optional. A flag to set the component performance storage
    """
    from epyk.core.js.primitives import JsObjects

    if js_funcs is None:
      js_funcs = ["var wrapper = document.createElement('div'); wrapper.innerHTML = data",
        self.dom.add(JsObjects.JsObjects.get("(function(){if(typeof  wrapper.firstChild.innerText === 'undefined'){return wrapper.innerHTML} else{ return wrapper.firstChild.innerText}})()"))]
    else:
      if not isinstance(js_funcs, list):
        js_funcs = [js_funcs]
      js_funcs = ["var wrapper = document.createElement('div'); wrapper.innerHTML = data",
        self.dom.add(JsObjects.JsObjects.get("(function(){if(typeof  wrapper.firstChild.innerText === 'undefined'){return wrapper.innerHTML} else{ return wrapper.firstChild.innerText}})()"))] + js_funcs
    return super(List, self).drop(js_funcs, prevent_default, profile)

  def __add__(self, component: Li):
    """ Add items to a container """
    if not isinstance(component, Li):
      raise ValueError("This can only be used for Li")

    self.items = self.items or []
    component.options.managed = False
    self.items.append(component)
    return self

  def __getitem__(self, i: int) -> Li:
    """
    Python function to get the elements of the lists which will be passed to the JavaScript.

    :param i: Get an element from the Python list
    """
    return self.items[i] if self.items is not None else None

  def item(self, n: int) -> Li:
    return self.items[n]

  def add_item(self, d: Union[Html.Html, str]):
    """
    Add an element to the list before passing the list to the Javascript.

    :param d: The component to be added
    """
    self.items = self.items or []
    li_obj = Li(self.page, d, options={"item_type": self.options.item_type},
                html_code="%s_%s" % (self.htmlCode, len(self.items)))
    if self.options.delete:
      li_obj.click(["this.remove()"])
      li_obj.style.css.cursor = "pointer"
    if self.options.li_class:
      li_obj.style.clear_style()
      li_obj.attr["class"].initialise(self.options.li_class)
    if hasattr(d, 'options'):
      d.options.managed = False
    li_obj.options.managed = False
    li_obj.css(self.options.li_css)
    if self.options.li_class:
      li_obj.attr["class"].add(self.options.li_class)
    self.items.append(li_obj)
    return li_obj

  def add_items(self, components: list) -> type_List[Li]:
    li_objs = [self.add_item(component) for component in components]
    return li_objs

  def set_items(self):
    """ Reset all the items in the list by applying the default styles. """
    self.items = self.items or []
    for d in self.val:
      li_obj = Li(self.page, d, options={"item_type": self.options.item_type})
      if self.options.li_class:
        li_obj.style.clear_style()
        li_obj.attr["class"].initialise(self.options.li_class)
      li_obj.options.managed = False
      li_obj.css(self.options.li_css)
      if self.options.li_class:
        li_obj.attr["class"].add(self.options.li_class)
      self.items.append(li_obj)
    return self

  def on_items(self, event: str, js_funcs: types.JS_FUNCS_TYPES, profile: types.PROFILE_TYPE = None):
    """
    Add event to the list items.

    :param event: The event type
    :param js_funcs: Javascript functions
    :param profile: Optional. A flag to set the component performance storage
    """
    for i in self.items:
      i.on(event, js_funcs, profile)
    return self

  def click_items(self, js_funcs: types.JS_FUNCS_TYPES, profile: types.PROFILE_TYPE = None):
    """
    Add click events on the list items.

    :param js_funcs: Javascript functions
    :param profile: Optional. A flag to set the component performance storage
    """
    js_funcs = JsUtils.jsConvertFncs(js_funcs)
    for i, item in enumerate(self.items):
      fnc = JsUtils.jsConvertFncs([
        self.page.js.getElementsByName("divs_%s" % self.htmlCode).all(self.page.js.objects.dom("elt").hide().r),
        self.page.js.getElementsByName("divs_%s" % self.htmlCode)[i].toggle().r])
      item.click(fnc + js_funcs, profile)
    return self

  def click(self, js_funcs: types.JS_FUNCS_TYPES, profile: types.PROFILE_TYPE = None,
            source_event: str = None, on_ready: bool = False):
    self.style.css.cursor = "pointer"
    return super().click(js_funcs, profile=profile, source_event=source_event, on_ready=on_ready)

  def __str__(self):
    self._vals = "".join([i.html() for i in self.items]) if self.items is not None else ""
    return "<ul %s>%s</ul>" % (self.get_attrs(css_class_names=self.style.get_classes()), self._vals)


class Groups(Html.Html):
  name = 'Groups'

  def __init__(self, page: primitives.PageModel, data: list, categories: Optional[list], size: tuple, color: str,
               width: tuple, height: tuple, html_code: str, helper: str, options: Optional[dict],
               profile: types.PROFILE_TYPE):
    super(Groups, self).__init__(page, [], css_attrs={"width": width, "height": height}, options=options,
                                 html_code=html_code, profile=profile)
    self.add_helper(helper)
    self.color = color if color is not None else self.page.theme.greys[9]
    self.css({'font-size': "%s%s" % (size[0], size[1]) if size is not None else 'inherit',
              'margin': "1px", 'padding': '0 2px'})
    self.builder_name, self._lists__map, self._lists__map_index = False, {}, []
    for i, cat in enumerate(categories):
      self.add_list(data[i], cat)

  def __getitem__(self, i: int) -> Html.Html:
    return self.val[i]

  def add_list(self, data, category: str = "", color: str = 'inherit', width: tuple = (None, 'px'),
               height: tuple = (None, 'px'), html_code: str = None, helper: str = None, options: dict = None,
               profile: types.PROFILE_TYPE = None):
    self._lists__map[category] = len(self.val)
    html_li = List(self.page, data, color, width, height, html_code, helper, options, profile)
    html_li.options.managed = False
    html_li.css({"margin-bottom": '5px'})
    self.val.append(html_li)
    self._lists__map_index.append(category)
    return self

  def __str__(self):
    self._vals = "".join(['''
      <a onclick='this.nextElementSibling.querySelectorAll("li").forEach(
        function(evt){evt.style.display = evt.style.display === "none" ? "" : "none"})' style='cursor:pointer'>%s</a>%s
      ''' % (
      self._lists__map_index[i] if len(self._lists__map_index) > i else "Category %s" % i,
      l.html()) for i, l in enumerate(self.val)])
    self.builder_name = self.__class__.__name__
    return "<div %s>%s</div>" % (self.get_attrs(css_class_names=self.style.get_classes()), self._vals)


class Items(Html.Html):
  name = 'Items'
  _option_cls = OptList.OptionsItems

  def __init__(self, page: primitives.PageModel, records, width: tuple, height: tuple, options: Optional[dict],
               html_code: str, profile: Optional[Union[bool, dict]], helper: str):
    super(Items, self).__init__(page, records, html_code=html_code, profile=profile, options=options,
                                css_attrs={"width": width, 'height': height})
    self._vals = records
    if html_code in self.page.inputs:
      if not isinstance(self.page.inputs[html_code], list):
        inputs_vals = self.page.inputs[html_code].split(",")
      else:
        inputs_vals = self.page.inputs[html_code]
      if not isinstance(inputs_vals, list):
        inputs_vals = inputs_vals.split(self.options.delimiter)
      if self._vals:
        for v in self._vals:
          if v['value'] in inputs_vals:
            v[self.options.checked_key] = True
          else:
            v[self.options.checked_key] = False
    self.add_helper(helper, css={"float": "none", "margin-left": "5px"})
    self.__external_item = False

  @property
  def style(self) -> GrpClsList.ClassItems:
    """ Property to the CSS Style of the component. """
    if self._styleObj is None:
      self._styleObj = GrpClsList.ClassItems(self)
    return self._styleObj

  def record(self, values: types.JS_FUNCS_TYPES):
    """
    A function helper to set values from Python in this object.

    :param values: The items to be added to the list
    """
    records = []
    if isinstance(values, dict):
      for k, v in values.items():
        records.append({"text": k, "tooltip": v})
    else:
      records = values
    self._vals = records

  _js__builder__ = ''' htmlObj.innerHTML = "";
      data.forEach(function(item, i){
        if(options.showdown){var converter = new showdown.Converter(options.showdown); 
          converter.setOption("display", "inline-block"); var content = item; 
          if(typeof item.content !== 'undefined'){content = item.content}
          else if(typeof item.text !== 'undefined'){content = item.text};
          var content = converter.makeHtml(content).replace("<p>", "<p style='display:inline-block;margin:0'>")};
        var li = document.createElement("li");
        Object.keys(options.li_style).forEach(function(key){li.style[key] = options.li_style[key]});
        if(typeof item.type === 'undefined'){window[options.prefix+ options.items_type](li, item, options)}
        else{window[options.prefix + item.type](li, item, options)};
        if(typeof item.tooltip !== 'undefined'){
          var info = document.createElement("i");
          info.classList.add(...options.info_icon.split(" ")); info.style.position = 'absolute';
          info.style.top = "4px"; info.style.right = "20px";
          li.style.position = "relative";
          info.setAttribute('title', item.tooltip); 
          info.setAttribute('data-html', true); 
          info.setAttribute('data-placement', 'right'); 
          info.setAttribute('data-toggle', 'tooltip'); 
          li.lastChild.style.display = 'inline-block'; li.appendChild(info);
          %s.tooltip();
        }
        if(options.delete){
          var close = document.createElement("i");
          close.classList.add(...options.delete_icon.split(" ")); close.style.position = 'absolute';
          close.style.right = "0"; close.style.cursor = 'pointer';
          close.onclick = function(event){this.parentNode.remove()};
          li.style.position = "relative";
          for (const [key, value] of Object.entries(options.delete_position)){
            close.style[key] = value}
          li.lastChild.style.display = 'inline-block'; li.appendChild(close)}
        if(options.items_space){li.style.margin = "5px 0"; li.style.padding = "2px 0"}
        htmlObj.appendChild(li)})''' % JsQuery.decorate_var("info", convert_var=False)

  def items_style(self, style_type: str = None, css_attrs: dict = None):
    """
    Function to load a predefined style for the items of the components.

    :param style_type. The alias of the style to apply
    :param css_attrs. Optional. Items CSS attributes
    """
    li_item_style = {}
    if style_type == "bullets":
      li_item_style = {
        "display": 'inline-block', 'padding': '0 5px', 'margin-right': '2px', 'background': self.page.theme.greys[2],
        'border': '1px solid %s' % self.page.theme.greys[2], 'border-radius': '10px'}
    if css_attrs is not None:
      li_item_style.update(css_attrs)
    self.options.li_style = li_item_style
    return self

  @property
  def options(self) -> OptList.OptionsItems:
    """
    Property to the component options.

    Options can either impact the Python side or the Javascript builder.

    Python can pass some options to the JavaScript layer.
    """
    return super().options

  @property
  def dom(self) -> JsHtmlList.JsItem:
    """
    Return all the Javascript functions defined for an HTML Component.

    Those functions will use plain javascript by default.
    """
    if self._dom is None:
      self._dom = JsHtmlList.JsItem(self, page=self.page)
    return self._dom

  def click(self, js_funcs: types.JS_FUNCS_TYPES, profile: types.PROFILE_TYPE = None,
            source_event: Optional[str] = None, on_ready: bool = False):
    """
    The onclick event occurs when the user clicks on an element of the list.

    Tips: Use the pk.events.value to get the item value.

    Usage::

      status = page.ui.timelines.issues(height=150)
      status.click([
        page.js.console.log("value", skip_data_convert=True)
      ])

    :param js_funcs: Javascript functions
    :param profile: Optional. A flag to set the component performance storage
    :param source_event: Optional. The source target for the event
    :param on_ready: Optional. Specify if the event needs to be trigger when the page is loaded
    """
    if not isinstance(js_funcs, list):
      js_funcs = []
    self.options.click = "function(event, value){%s} " % JsUtils.jsConvertFncs(js_funcs, toStr=True, profile=profile)
    return self

  def draggable(self, js_funcs: types.JS_FUNCS_TYPES = None, options: types.OPTION_TYPE = None,
                profile: types.PROFILE_TYPE = None, source_event: Optional[str] = None):
    """


    :param js_funcs: Optional. Javascript functions
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param source_event: Optional. The source target for the event
    """
    js_funcs = js_funcs or []
    if not isinstance(js_funcs, list):
      js_funcs = [js_funcs]
    js_funcs.append('event.dataTransfer.setData("text", value)')
    self.options.draggable = "function(event, value){%s} " % JsUtils.jsConvertFncs(
      js_funcs, toStr=True, profile=profile)
    return self

  def add_type(self, name: str, item_def: Optional[str] = None, func_name: Optional[str] = None,
               dependencies: list = None):
    """
    Add a bespoke item type with it is specific style and components.

    TODO: Create a tutorial to explain how to extend list types.

    Usage::

      items = page.ui.lists.items(records.to_dict(orient="records"))
        items.add_type("demo", '''
        var item = document.createElement("DIV");
        var sub = document.createElement("DIV");
        var nameBox = document.createElement("DIV"); nameBox.innerHTML = 'Toto';
        nameBox.style.display = "inline-block";
        nameBox.style.fontWeight = 900;
        nameBox.style.marginRight = "5px";
        sub.setAttribute('name', 'value'); sub.setAttribute('data-valid', true); sub.innerHTML = data.Year;
        sub.style.display = "inline-block";
        var country = document.createElement("DIV"); country.innerHTML = data['Country Name'];
        country.style.textAlign = "right";
        country.style.fontSize = "9px";
        country.style.fontStyle = "italic";
        item.appendChild(nameBox);
        item.appendChild(sub);
        item.appendChild(country)
      ''')

    :param name: The reference of this type name in the framework
    :param item_def: Optional. The definition of the items (examples in JsHtmlList.py)
    :param func_name: Optional. The external function name used to build the items
    :param dependencies: Optional. The external module dependencies
    """
    if dependencies is not None:
      for d in dependencies:
        if d in Imports.JS_IMPORTS:
          self.page.jsImports.add(d)
        if d in Imports.CSS_IMPORTS:
          self.page.cssImport.add(d)
    self.style.css.padding_left = 0
    self.css({"list-style": 'none'})
    self.options.items_type = name
    if func_name is not None:
      self.__external_item = True
      item_type_name = "%s%s" % (self.options.prefix, self.options.items_type)
      self.page.properties.js.add_constructor(item_type_name, "function %s(htmlObj, data, options){%s}" % (
        item_type_name, JsHtmlList.JsItemsDef(self).custom("var item = %s(htmlObj, data, options)" % func_name)))
    else:
      item_type_name = "%s%s" % (self.options.prefix, self.options.items_type)
      self.page.properties.js.add_constructor(item_type_name, "function %s(htmlObj, data, options){%s}" % (
        item_type_name, JsHtmlList.JsItemsDef(self).custom(item_def)))
    return self

  def select_type(self, name: Optional[str] = None, style: Optional[dict] = None,
                  selected_style: Optional[dict] = None):
    """
    Set the CSS Style of the items in the list.
    
    It is possible to use predefined style or to pass bespoke ones.

    Style will be set at list type level so all the list in the page will be using it.

    :param name: Optional. The list type name to be used
    :param style: Optional. The CSS style to be applied to the item
    :param selected_style: Optional. The css style to be applied when selected
    """
    li_attrs = self.options.style
    if style is None:
      li_attrs["padding"] = "2px 5px"
    else:
      li_attrs.update(style)
    self.options.style = li_attrs
    self.style.add_custom_class(selected_style or self.style.defined.selected_text_background_color(),
                                classname="list_%s_selected" % (name or self.options.items_type))

  def __str__(self):
    item_type_name = "%s%s" % (self.options.prefix, self.options.items_type)
    self.options.style_select = "list_%s_selected" % self.options.items_type
    # add all the shape definitions
    if not self.page.properties.js.has_constructor(item_type_name) and not self.__external_item:
      shapes = JsHtmlList.JsItemsDef(self)
      self.page.properties.js.add_constructor(item_type_name, "function %s(htmlObj, data, options){%s}" % (
        item_type_name, getattr(shapes, self.options.items_type)(self.page)))
    self.page.properties.js.add_builders(self.refresh())
    return '<ul %s></ul>%s' % (self.get_attrs(css_class_names=self.style.get_classes()), self.helper)


class ListTournaments(Html.Html):
  name = 'Brackets'
  requirements = ('jquery-bracket', )
  _option_cls = OptList.OptionsListBrackets

  def __init__(self, page: primitives.PageModel, records, width: tuple, height: tuple, options: Optional[dict],
               profile: Optional[Union[bool, dict]]):
    super(ListTournaments, self).__init__(
      page, records, options=options, profile=profile, css_attrs={"width": width, "height": height})
    self.css({'overflow': 'auto', "padding": "auto", "margin": "auto"})

  def __str__(self):
    self.page.properties.js.add_builders(self.refresh())
    return "<div %s></div>" % self.get_attrs(css_class_names=self.style.get_classes())
