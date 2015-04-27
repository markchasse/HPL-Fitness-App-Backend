# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150423_0602'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('subject', models.CharField(max_length=500)),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sender', models.ForeignKey(related_name='app_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['updated'],
            },
            bases=(models.Model,),
        ),
    ]
