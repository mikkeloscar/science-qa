# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', uuidfield.fields.UUIDField(verbose_name='API key', unique=True, max_length=32, editable=False, blank=True)),
                ('domain', models.CharField(max_length=200, verbose_name='domain')),
                ('active', models.BooleanField(default=False, verbose_name='active')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_expire', models.DateTimeField(null=True, verbose_name='expire date', blank=True)),
                ('never_expire', models.BooleanField(default=False, verbose_name='never expire')),
            ],
            options={
                'verbose_name': 'API key',
                'verbose_name_plural': 'API keys',
            },
            bases=(models.Model,),
        ),
    ]
