from django.db import models
from django.utils.translation import ugettext_lazy as _

from uuidfield import UUIDField

class APIKey(models.Model):
    key = UUIDField(auto=True, verbose_name=_('API key'))
    domain = models.CharField(_('domain'), max_length=200)
    active = models.BooleanField(_('active'))
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_expire = models.DateTimeField(_('expire date'))

    class Meta:
        verbose_name = _('API key')
        verbose_name_plural = _('API keys')

    def __unicode__(self):
        return self.domain

    def valid(self, request):
        return True
