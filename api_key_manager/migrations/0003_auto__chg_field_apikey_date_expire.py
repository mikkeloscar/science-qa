# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'APIKey.date_expire'
        db.alter_column(u'api_key_manager_apikey', 'date_expire', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'APIKey.date_expire'
        db.alter_column(u'api_key_manager_apikey', 'date_expire', self.gf('django.db.models.fields.DateTimeField')(default=None))

    models = {
        u'api_key_manager.apikey': {
            'Meta': {'object_name': 'APIKey'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_expire': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'}),
            'never_expire': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['api_key_manager']