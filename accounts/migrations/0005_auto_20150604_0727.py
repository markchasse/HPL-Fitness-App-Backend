# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150603_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appcoach',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 4, 7, 27, 51, 314579, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appcoach',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 4, 7, 27, 51, 314676, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appstudent',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 4, 7, 27, 51, 312986, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appstudent',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 4, 7, 27, 51, 313035, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
