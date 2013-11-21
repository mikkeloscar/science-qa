from django import template
from django.utils.translation import ugettext as _
from django.utils.timezone import now as datetime_now

register = template.Library()

@register.filter
def is_active(key):
    now = datetime_now()
    active = key.date_expire > now and key.active
    if active:
        return _('yes')
    else:
        return _('no')
