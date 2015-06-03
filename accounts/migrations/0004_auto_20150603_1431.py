# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150526_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='appstudent',
            name='apple_subscription_created_date',
            field=models.DateTimeField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appcoach',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 3, 14, 31, 2, 781908, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appcoach',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 3, 14, 31, 2, 781967, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appstudent',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 3, 14, 31, 2, 780924, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appstudent',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 3, 14, 31, 2, 780962, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
