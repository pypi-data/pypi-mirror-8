#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import six

from django.contrib.admin.widgets import AdminTextareaWidget
from django.forms.util import flatatt
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from bootstrap3_wysihtml5x.conf import settings
from bootstrap3_wysihtml5x.utils import get_function

render_cmd_icon = {}
render_cmd_dialog = {}

def render_blank(id):
    return ''

def render_createLink_dialog(id):
    return '\
<div data-bootstrap3_wysihtml5x-dialog="createLink" style="display:none">\
  <label>%(_link_)s:</label>&nbsp;\
  <input data-bootstrap3_wysihtml5x-dialog-field="href" value="http://">\
  <a data-bootstrap3_wysihtml5x-dialog-action="save" class="button">%(_ok_)s</a>&nbsp;\
  <a data-bootstrap3_wysihtml5x-dialog-action="cancel" class="button">%(_cancel_)s</a>\
</div>' % { "_link_": _("Link"),
            "_ok_": _("Ok"),
            "_cancel_": _("Cancel")
        }


def render_insertImage_dialog(id):
    return '\
<div data-bootstrap3_wysihtml5x-dialog="insertImage" style="display:none">\
  <label>%(_link_)s:</label>&nbsp;\
  <input data-bootstrap3_wysihtml5x-dialog-field="src" value="http://">\
  <a data-bootstrap3_wysihtml5x-dialog-action="save" class="button">%(_ok_)s</a>&nbsp;\
  <a data-bootstrap3_wysihtml5x-dialog-action="cancel" class="button">%(_cancel_)s</a>\
</div>' % { "_link_": _("Image"),
            "_ok_": _("Ok"),
            "_cancel_": _("Cancel")
        }


def render_formatBlockHeader_icon(id):
    return '\
    <span data-bootstrap3_wysihtml5x-command-group="%(command_name)s" title="Format text header" class="heading-selector">\
      <div>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="h1">H1</span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="h2">H2</span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="h3">H3</span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="h4">H4</span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="h5">H5</span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="h6">H6</span>\
      </div>\
    </span>' % { "command_name": settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['formatBlockHeader']['command_name'] }

def render_formatBlockParagraph_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Make a paragraph block" data-bootstrap3_wysihtml5x-command-value="p" class="command format-block-p"></span>' % { "command_name": settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['formatBlockParagraph']['command_name'] }

def render_bold_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Make text bold (CTRL + B)" class="command"></span>' % { "command_name": settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['bold']['command_name'] }

def render_italic_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Make text italic (CTRL + I)" class="command"></span>' % { "command_name": settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['italic']['command_name'] }

def render_underline_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Underline text (CTRL + U)" class="command"></span>' % { "command_name": settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['underline']['command_name'] }

def render_justifyLeft_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Paragraph left justified" class="command"></span>' % { "command_name": settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['justifyLeft']['command_name'] }

def render_justifyCenter_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Paragraph center justified" class="command"></span>' % { "command_name": settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['justifyCenter']['command_name'] }

def render_justifyRight_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Paragraph right justified" class="command"></span>' % { "command_name": settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['justifyRight']['command_name'] }

def render_insertOrderedList_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Insert an ordered list" class="command"></span>' % { "command_name": settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['insertOrderedList']['command_name'] }

def render_insertUnorderedList_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Insert an unordered list" class="command"></span>' % { "command_name": settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['insertUnorderedList']['command_name'] }

def render_insertImage_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Insert an image" class="command insert-image"></span>' % { 'command_name': settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['insertImage']['command_name'] }

def render_createLink_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Insert a link" class="command create-link"></span>' % { 'command_name': settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['createLink']['command_name'] }

def render_insertHTML_icon(id):
    return '<span data-bootstrap3_wysihtml5x-command="%(command_name)s" title="Insert a quote" class="command" data-bootstrap3_wysihtml5x-command-value="%(command_value)s"></span>'  % {  'command_name': settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['insertHTML']['command_name'] , 'command_value': settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['insertHTML']['command_value'] }

def render_foreColor_icon(id):
    return '\
      <span data-bootstrap3_wysihtml5x-command-group="%(command_name)s" title="Color the selected text" class="fore-color">\
      <div>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="silver" unselectable="on"></span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="gray" unselectable="on"></span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="maroon" unselectable="on"></span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="red" unselectable="on"></span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="purple" unselectable="on"></span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="green" unselectable="on"></span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="olive" unselectable="on"></span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="navy" unselectable="on"></span>\
        <span data-bootstrap3_wysihtml5x-command="%(command_name)s" data-bootstrap3_wysihtml5x-command-value="blue" unselectable="on"></span>\
      </div>\
    </span>' % { 'command_name': settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['foreColor']['command_name'] }

def render_changeView_icon(id):
    return '<span data-bootstrap3_wysihtml5x-action="%(command_name)s" title="Show HTML" class="action" unselectable="on"></span>' % { 'command_name': settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR['changeView']['command_name'] }


class Wysihtml5xTextareaWidget(AdminTextareaWidget):

    class Media:
        css = {
            'all': ('bootstrap3_wysihtml5x/css/toolbar.css',)
        }
        js = ('bootstrap3_wysihtml5x/js/wysihtml5x.min.js',)

    def __init__(self, attrs=None, editor_settings=None, toolbar_settings=None):
        if not attrs:
            attrs = {"rows": 25}
        elif not attrs.get("rows", False):
            attrs.update({"rows": 25})

        if editor_settings:
            self.editor_settings = editor_settings
        else: 
            self.editor_settings = settings.BOOTSTRAP3_WYSIHTML5X_EDITOR

        if toolbar_settings:
            self.toolbar_settings = toolbar_settings
        else:
            self.toolbar_settings = settings.BOOTSTRAP3_WYSIHTML5X_TOOLBAR

        self.render_cmd_icon = {}
        self.render_cmd_dialog = {}
        for k, v in six.iteritems(self.toolbar_settings):
            if v.get("active", False):
                self.render_cmd_icon[k] = v.get("render_icon", "bootstrap3_wysihtml5x.widgets.render_blank")
                if v.get("render_dialog", False):
                    self.render_cmd_dialog[k] = v["render_dialog"]
            else: 
                self.render_cmd_icon[k] = "bootstrap3_wysihtml5x.widgets.render_blank"
                if v.get("render_dialog", False):
                    self.render_cmd_dialog[k] = "bootstrap3_wysihtml5x.widgets.render_blank"

        super(Wysihtml5xTextareaWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        textarea_widget = '<textarea%s>%s</textarea>' % (
            flatatt(final_attrs),
            conditional_escape(force_text(value)))
        wid = final_attrs.get('id', 'unknown')
        toolbar_widget = self.render_toolbar_widget(wid)
        pos = wid.find('__prefix__')
        if pos != -1:
            js_widget = self.render_js_delay_widget(wid, pos)
        else:
            js_widget = self.render_js_init_widget(wid) 
            return mark_safe('<div style="display:inline-block">' +
                         toolbar_widget + 
                         textarea_widget + 
                         '</div>' +
                         js_widget)

    def render_toolbar_widget(self, id):
        widget = '\
<div id="%(id)s-toolbar" class="bootstrap3_wysihtml5x-editor-toolbar">\
  <div class="commands">' % { "id": id }
        widget += get_function(self.render_cmd_icon['formatBlockHeader'])(id)
        widget += get_function(self.render_cmd_icon['formatBlockParagraph'])(id)
        widget += get_function(self.render_cmd_icon['bold'])(id)
        widget += get_function(self.render_cmd_icon['italic'])(id)
        widget += get_function(self.render_cmd_icon['underline'])(id)
        widget += get_function(self.render_cmd_icon['justifyLeft'])(id)
        widget += get_function(self.render_cmd_icon['justifyCenter'])(id)
        widget += get_function(self.render_cmd_icon['justifyRight'])(id)
        widget += get_function(self.render_cmd_icon['insertOrderedList'])(id)
        widget += get_function(self.render_cmd_icon['insertUnorderedList'])(id)
        widget += get_function(self.render_cmd_icon['insertImage'])(id)
        widget += get_function(self.render_cmd_icon['createLink'])(id)
        widget += get_function(self.render_cmd_icon['insertHTML'])(id)
        widget += get_function(self.render_cmd_icon['foreColor'])(id)
        widget += get_function(self.render_cmd_icon['changeView'])(id)
        widget += '\
  </div>\
  <div class="bootstrap3_wysihtml5x-dialogs">'
        widget += get_function(self.render_cmd_dialog['createLink'])(id)
        widget += get_function(self.render_cmd_dialog['insertImage'])(id)
        widget += '\
  </div>\
</div>'
        return widget

    def render_js_delay_widget(self, id, position):
        options = {"id": id}
        options.update(self.editor_settings)
        if not options.get('name', None) or options['name'] == 'null':
            options['name'] = '"%s"' % id[3:]
        if not options.get('toolbar', None) or options['toolbar'] == 'null':
            options['toolbar'] = '"%s-toolbar"' % id
        options['prefixid'] = id[0:position]
        widget = '''
<script>
  setTimeout(function() {
    var id = '%(id)s';
    var name = '%(name)s';
    var toolbar = %(toolbar)s;
    if(typeof(window._wysihtml5x_inited) == 'undefined') {
      window._wysihtml5x_inited = []
    }
    if(typeof(window._wysihtml5x_inited[id]) == 'undefined') {
      window._wysihtml5x_inited[id] = true;
    } else {
      var totforms = parseInt(document.getElementById('%(prefixid)sTOTAL_FORMS').value)-1;
      var newid = id.replace(/__prefix__/, totforms);
      var name = name.replace(/__prefix__/, totforms);
      var newtoolbar = toolbar.replace(/__prefix__/, totforms);
      django.jQuery('#'+toolbar).attr('id', newtoolbar);
      console.log(newid);
      if(document.getElementById(newid)) {
        new bootstrap3_wysihtml5x.Editor(newid,{
          name:                 name,
          style:                %(style)s,
          toolbar:              newtoolbar,
          autoLink:             %(autoLink)s,
          parserRules:          %(parserRules)s,
          parser:               %(parser)s,
          composerClassName:    %(composerClassName)s,
          bodyClassName:        %(bodyClassName)s,
          useLineBreaks:        %(useLineBreaks)s,
          stylesheets:          %(stylesheets)s,
          placeholderText:      %(placeholderText)s,
          allowObjectResizing:  %(allowObjectResizing)s,
          supportTouchDevices:  %(supportTouchDevices)s
        });
      }
    }
  }, 0);
</script>''' % options
        return widget

    def render_js_init_widget(self, id):
        options = {"id": id}
        options.update(self.editor_settings)
        if options.get('toolbar', 'null') == 'null':
            options['toolbar'] = '"%s-toolbar"' % id
        widget = '''
<script>
  new bootstrap3_wysihtml5x.Editor("%(id)s",{
    name:                 %(name)s,
    style:                %(style)s,
    toolbar:              %(toolbar)s,
    autoLink:             %(autoLink)s,
    parserRules:          %(parserRules)s,
    parser:               %(parser)s,
    composerClassName:    %(composerClassName)s,
    bodyClassName:        %(bodyClassName)s,
    useLineBreaks:        %(useLineBreaks)s,
    stylesheets:          %(stylesheets)s,
    placeholderText:      %(placeholderText)s,
    allowObjectResizing:  %(allowObjectResizing)s,
    supportTouchDevices:  %(supportTouchDevices)s
  });
</script>''' % options
        return widget
