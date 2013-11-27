from django import template
from django.utils.translation import ugettext as _
from django.utils.timezone import now as datetime_now

register = template.Library()

@register.filter
def degrees_to_js(degrees):
    bsc = 'bsc: [\n'
    msc = 'msc: [\n'
    for degree in degrees:
        if degree.level == 'bsc':
            bsc = bsc + str(degree.id) + ',\n'
        if degree.level == 'msc':
            msc = msc + str(degree.id) + ',\n'
    bsc = bsc + '],'
    msc = msc + ']'

    degrees = 'var degrees = {\n' + bsc + '\n' + msc + '\n};'
    return degrees
