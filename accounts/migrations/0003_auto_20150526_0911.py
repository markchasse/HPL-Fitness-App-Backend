# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150525_1532'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserSubscription',
        ),
        migrations.RemoveField(
            model_name='appcoach',
            name='id',
        ),
        migrations.RemoveField(
            model_name='appstudent',
            name='id',
        ),
        migrations.AlterField(
            model_name='appcoach',
            name='app_user',
            field=models.OneToOneField(related_name='coach_user', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appcoach',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 26, 9, 11, 3, 992548, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appcoach',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 26, 9, 11, 3, 992582, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appstudent',
            name='app_user',
            field=models.OneToOneField(related_name='student_user', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appstudent',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 26, 9, 11, 3, 991875, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appstudent',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 26, 9, 11, 3, 991923, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
