# -*- coding: utf-8 -*-
from django.forms.utils import flatatt
from django.forms.widgets import TextInput
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

try:
    import json
except ImportError:
    from django.utils import simplejson as json
try:
    from django.utils.encoding import force_unicode as force_text
except ImportError:  # python3
    from django.utils.encoding import force_text


class DurationPicker(TextInput):
    class Media:
        class JsFiles(object):
            def __iter__(self):
                yield 'bootstrap3_duration/js/jquery-duration-picker.js'

        js = JsFiles()
        css = {'all': ('bootstrap3_duration/css/jquery-duration-picker.css',), }

    html_template = '''
        <div%(div_attrs)s>
            <input%(input_attrs)s/>
        </div>'''

    js_template = '''
        <script>
            (function(window) {
                var callback = function() {
                    $(function(){$("#%(picker_id)s").durationPicker();});
                };
                if(window.addEventListener)
                    window.addEventListener("load", callback, false);
                else if (window.attachEvent)
                    window.attachEvent("onload", callback);
                else window.onload = callback;
            })(window);
        </script>'''

    def __init__(self, attrs=None):
        div_attrs = {'class': 'input-group date'}

        super(TextInput, self).__init__(attrs)

        if 'class' not in self.attrs:
            self.attrs['class'] = 'form-control'
        self.div_attrs = div_attrs and div_attrs.copy() or {}
        self.picker_id = self.div_attrs.get('id') or None

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        input_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            input_attrs['value'] = force_text(self._format_value(value))
        input_attrs = dict([(key, conditional_escape(val)) for key, val in input_attrs.items()])  # python2.6 compatible
        if not self.picker_id:
            self.picker_id = (input_attrs.get('id', '') +
                              '_pickers').replace(' ', '_')
        self.div_attrs['id'] = self.picker_id
        div_attrs = dict(
            [(key, conditional_escape(val)) for key, val in self.div_attrs.items()])  # python2.6 compatible
        html = self.html_template % dict(div_attrs=flatatt(div_attrs),
                                         input_attrs=flatatt(input_attrs))
        js = self.js_template % dict(picker_id=input_attrs.get('id', ''))

        return mark_safe(force_text(html + js))
