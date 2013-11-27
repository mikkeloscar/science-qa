# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table(u'qa_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('question_da', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('answer_da', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('question_en', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('answer_en', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('degree_all_bsc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('degree_all_msc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_last_edit', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'qa', ['Question'])

        # Adding M2M table for field categories on 'Question'
        m2m_table_name = db.shorten_name(u'qa_question_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'qa.question'], null=False)),
            ('category', models.ForeignKey(orm[u'qa.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'category_id'])

        # Adding M2M table for field degrees on 'Question'
        m2m_table_name = db.shorten_name(u'qa_question_degrees')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'qa.question'], null=False)),
            ('degree', models.ForeignKey(orm[u'qa.degree'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'degree_id'])

        # Adding model 'Category'
        db.create_table(u'qa_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_da', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('category_id_da', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category_id_en', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_last_edit', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'qa', ['Category'])

        # Adding model 'Degree'
        db.create_table(u'qa_degree', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_da', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('degree_id_da', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('degree_id_en', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_last_edit', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('level', self.gf('django.db.models.fields.CharField')(default='bsc', max_length=3)),
        ))
        db.send_create_signal(u'qa', ['Degree'])

        # Adding model 'Rating'
        db.create_table(u'qa_rating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qa.Question'])),
            ('rating', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ku_user', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'qa', ['Rating'])


    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table(u'qa_question')

        # Removing M2M table for field categories on 'Question'
        db.delete_table(db.shorten_name(u'qa_question_categories'))

        # Removing M2M table for field degrees on 'Question'
        db.delete_table(db.shorten_name(u'qa_question_degrees'))

        # Deleting model 'Category'
        db.delete_table(u'qa_category')

        # Deleting model 'Degree'
        db.delete_table(u'qa_degree')

        # Deleting model 'Rating'
        db.delete_table(u'qa_rating')


    models = {
        u'qa.category': {
            'Meta': {'object_name': 'Category'},
            'category_id_da': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'category_id_en': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cat+'", 'symmetrical': 'False', 'to': u"orm['qa.Category']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'degree_all_bsc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'degree_all_msc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'degrees': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'degree+'", 'symmetrical': 'False', 'to': u"orm['qa.Degree']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_da': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'question_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        u'qa.rating': {
            'Meta': {'object_name': 'Rating'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ku_user': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.Question']"}),
            'rating': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['qa']