# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FitnessAppCoach',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('accounts.appuser',),
        ),
        migrations.CreateModel(
            name='FitnessAppStudent',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('accounts.appuser',),
        ),
        migrations.RemoveField(
            model_name='appstudent',
            name='subscription',
        ),
        migrations.AddField(
            model_name='appcoach',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 25, 15, 32, 55, 658472, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appcoach',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 25, 15, 32, 55, 658533, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appstudent',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 25, 15, 32, 55, 657249, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appstudent',
            name='subscription_choices',
            field=models.PositiveSmallIntegerField(default=1, max_length=10, verbose_name='Subscription Choices', choices=[(1, 'free'), (2, 'paid')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appstudent',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 25, 15, 32, 55, 657316, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
