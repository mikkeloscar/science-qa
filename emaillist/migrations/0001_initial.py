# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailReceiver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, verbose_name='Email address')),
                ('receiver_id', models.CharField(max_length=100, verbose_name='Receiver ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'email receiver',
                'verbose_name_plural': 'email receivers',
            },
            bases=(models.Model,),
        ),
    ]
