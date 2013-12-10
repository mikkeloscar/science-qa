# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field parent on 'Category'
        db.delete_table(db.shorten_name(u'qa_category_parent'))


    def backwards(self, orm):
        # Adding M2M table for field parent on 'Category'
        m2m_table_name = db.shorten_name(u'qa_category_parent')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_category', models.ForeignKey(orm[u'qa.category'], null=False)),
            ('to_category', models.ForeignKey(orm[u'qa.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_category_id', 'to_category_id'])


    models = {
        u'qa.category': {
            'Meta': {'object_name': 'Category'},
            'category_id_da': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'category_id_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_da': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'qa.degree': {
            'Meta': {'object_name': 'Degree'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'degree_id_da': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'degree_id_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'default': "'bsc'", 'max_length': '3'}),
            'name_da': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'qa.question': {
            'Meta': {'object_name': 'Question'},
            'answer_da': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'answer_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'questions'", 'symmetrical': 'False', 'to': u"orm['qa.Category']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'degree_all_bsc': ('django.db.models.fields.BooleanField', [], {}),
            'degree_all_msc': ('django.db.models.fields.BooleanField', [], {}),
            'degrees': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'questions'", 'symmetrical': 'False', 'to': u"orm['qa.Degree']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_da': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'question_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'qa.rating': {
            'Meta': {'unique_together': "(('question', 'ku_user'),)", 'object_name': 'Rating'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ku_user': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.Question']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['qa']