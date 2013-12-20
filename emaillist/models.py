from django.db import models

from django.utils.translation import ugettext_lazy as _

# Create your models here.
class EmailReceiver(models.Model):
    email = models.EmailField(_('Email address'))
    receiver_id = models.CharField(_('Receiver ID'), max_length=100)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('email receiver')
        verbose_name_plural = _('email receivers')

    def __unicode__(self):
        return self.email
