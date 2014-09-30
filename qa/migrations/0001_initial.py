# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_da', models.CharField(max_length=200, verbose_name='Category name (da)', blank=True)),
                ('name_en', models.CharField(max_length=200, verbose_name='Category name (en)', blank=True)),
                ('category_id_da', models.CharField(help_text='The category ID is used to refrence category in the url @ kunet.dk', max_length=200, verbose_name='Category ID (da)', blank=True)),
                ('category_id_en', models.CharField(help_text='The category ID is used to refrence category in the url @ kunet.dk', max_length=200, verbose_name='Category ID (en)', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_last_edit', models.DateTimeField(auto_now=True, verbose_name='last edit')),
                ('parents', models.ManyToManyField(to='qa.Category', null=True, verbose_name='Parent categories', blank=True)),
            ],
            options={
                'ordering': ['name_da', 'name_en'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'permissions': (('view_category', 'Can view category'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_da', models.CharField(max_length=200, verbose_name='Degree name (da)', blank=True)),
                ('name_en', models.CharField(max_length=200, verbose_name='Degree name (en)', blank=True)),
                ('degree_id_da', models.CharField(help_text='The degree ID is used to refrence degree in the url @ kunet.dk', max_length=200, verbose_name='Degree ID (da)')),
                ('degree_id_en', models.CharField(help_text='The degree ID is used to refrence degree in the url @ kunet.dk', max_length=200, verbose_name='Degree ID (en)', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_last_edit', models.DateTimeField(auto_now=True, verbose_name='last edit')),
                ('level', models.CharField(default=b'bsc', max_length=3, choices=[(b'bsc', b'Bsc'), (b'msc', b'Msc')])),
            ],
            options={
                'ordering': ['name_da', 'name_en'],
                'verbose_name': 'degree',
                'verbose_name_plural': 'degrees',
                'permissions': (('view_degree', 'Can view degree'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_da', models.CharField(max_length=200, verbose_name='question da', blank=True)),
                ('answer_da', models.TextField(verbose_name='answer da', blank=True)),
                ('question_en', models.CharField(max_length=200, verbose_name='question en', blank=True)),
                ('answer_en', models.TextField(verbose_name='answer en', blank=True)),
                ('degree_all_bsc', models.BooleanField(default=False, verbose_name='All Bsc degrees')),
                ('degree_all_msc', models.BooleanField(default=False, verbose_name='All Msc degrees')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_last_edit', models.DateTimeField(auto_now=True, verbose_name='last edit')),
                ('categories', models.ManyToManyField(related_name=b'questions', verbose_name='Categories', to='qa.Category')),
                ('degrees', models.ManyToManyField(related_name=b'questions', verbose_name='Degrees', to='qa.Degree')),
            ],
            options={
                'ordering': ['question_da', 'question_en'],
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
                'permissions': (('view_question', 'Can view question'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(verbose_name='rating')),
                ('ku_user', models.CharField(max_length=6, verbose_name='KU user')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('question', models.ForeignKey(verbose_name='question', to='qa.Question')),
            ],
            options={
                'verbose_name': 'rating',
                'verbose_name_plural': 'ratings',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('question', 'ku_user')]),
        ),
    ]
