from django.contrib import admin
from emaillist.models import EmailReceiver

class EmailReceiverAdmin(admin.ModelAdmin):
    list_display = ('email', 'receiver_id', 'active', 'date_added')
    list_filter = ('active',)

admin.site.register(EmailReceiver, EmailReceiverAdmin)
