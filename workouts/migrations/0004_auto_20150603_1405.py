# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0003_auto_20150526_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutresult',
            name='result_submit_date',
            field=models.DateField(default=datetime.date(2015, 6, 3), verbose_name=b'Result Submitted Date'),
            preserve_default=True,
        ),
    ]
