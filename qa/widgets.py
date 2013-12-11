from django import forms
from django.contrib.admin.templatetags.admin_static import static
# from django.core.urlresolvers import reverse
# from django.forms.widgets import RadioFieldRenderer
# from django.forms.utils import flatatt
# from django.utils.html import escape, format_html, format_html_join, smart_urlquote
# from django.utils.text import Truncator
# from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
# from django.utils.encoding import force_text
# from django.utils import six


class FilteredSelectMultiple(forms.SelectMultiple):
    """
    A SelectMultiple with a JavaScript filter interface.

    Note that the resulting JavaScript assumes that the jsi18n
    catalog has been loaded in the page
    """
    @property
    def media(self):
        admin_js = ["core.js", "SelectBox.js"]
        js = ["SelectFilter2.js"]
        media_js = [static("admin/js/%s" % path) for path in admin_js]
        media_js += [static("js/%s" % path) for path in js]
        return forms.Media(js=media_js)

    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
        self.verbose_name = verbose_name
        self.is_stacked = is_stacked
        super(FilteredSelectMultiple, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'selectfilter'
        if self.is_stacked:
            attrs['class'] += 'stacked'
        output = [super(FilteredSelectMultiple, self).render(name, value, attrs, choices)]
        output.append('<script type="text/javascript">addEvent(window, "load", function(e) {')
        # TODO: "id_" is hard-coded here. This should instead use the correct
        # API to determine the ID dynamically.
        output.append('SelectFilter.init("id_%s", "%s", %s, "%s"); });</script>\n'
            % (name, self.verbose_name.replace('"', '\\"'), int(self.is_stacked), static('admin/')))
        return mark_safe(''.join(output))
