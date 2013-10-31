# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Degree.date_added'
        db.add_column(u'qa_degree', 'date_added',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 10, 31, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Degree.date_last_edit'
        db.add_column(u'qa_degree', 'date_last_edit',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 10, 31, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Category.date_added'
        db.add_column(u'qa_category', 'date_added',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 10, 31, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Category.date_last_edit'
        db.add_column(u'qa_category', 'date_last_edit',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 10, 31, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Rating.date_added'
        db.add_column(u'qa_rating', 'date_added',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 10, 31, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Question.date_added'
        db.add_column(u'qa_question', 'date_added',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 10, 31, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Question.date_last_edit'
        db.add_column(u'qa_question', 'date_last_edit',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 10, 31, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Degree.date_added'
        db.delete_column(u'qa_degree', 'date_added')

        # Deleting field 'Degree.date_last_edit'
        db.delete_column(u'qa_degree', 'date_last_edit')

        # Deleting field 'Category.date_added'
        db.delete_column(u'qa_category', 'date_added')

        # Deleting field 'Category.date_last_edit'
        db.delete_column(u'qa_category', 'date_last_edit')

        # Deleting field 'Rating.date_added'
        db.delete_column(u'qa_rating', 'date_added')

        # Deleting field 'Question.date_added'
        db.delete_column(u'qa_question', 'date_added')

        # Deleting field 'Question.date_last_edit'
        db.delete_column(u'qa_question', 'date_last_edit')


    models = {
        u'qa.category': {
            'Meta': {'object_name': 'Category'},
            'category_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
            'degree_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.Question']"}),
            'rating': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['qa']