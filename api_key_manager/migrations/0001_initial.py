# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'APIKey'
        db.create_table(u'api_key_manager_apikey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_expire', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'api_key_manager', ['APIKey'])


    def backwards(self, orm):
        # Deleting model 'APIKey'
        db.delete_table(u'api_key_manager_apikey')


    models = {
        u'api_key_manager.apikey': {
            'Meta': {'object_name': 'APIKey'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_expire': ('django.db.models.fields.DateTimeField', [], {}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['api_key_manager']