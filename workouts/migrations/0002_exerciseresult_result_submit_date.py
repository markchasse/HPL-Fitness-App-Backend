# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseresult',
            name='result_submit_date',
            field=models.DateField(default=datetime.date(2015, 4, 21), verbose_name=b'Result Submitted Date'),
            preserve_default=True,
        ),
    ]
