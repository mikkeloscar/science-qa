from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import utc

import datetime

from uuidfield import UUIDField

class APIKey(models.Model):
    key = UUIDField(auto=True, verbose_name=_('API key'))
    domain = models.CharField(_('domain'), max_length=200)
    active = models.BooleanField(_('active'))
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_expire = models.DateTimeField(_('expire date'), blank=True, null=True)
    never_expire = models.BooleanField(_('never expire'))

    class Meta:
        verbose_name = _('API key')
        verbose_name_plural = _('API keys')

    def __unicode__(self):
        return self.domain

    def expire(self):
        if self.never_expire:
            return _('Never')
        else:
            return self.date_expire

    def valid(self, referere):
        # TODO properly handle referere
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if referere == domain and active:
            if never_expire or date_expire > now:
                return True
        return False
