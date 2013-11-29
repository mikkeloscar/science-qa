from django.contrib import admin
from api_key_manager.models import APIKey

class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('domain', 'key', 'active', 'date_added', 'expire')

admin.site.register(APIKey, APIKeyAdmin)
