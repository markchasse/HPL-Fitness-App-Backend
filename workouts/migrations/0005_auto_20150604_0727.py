# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0004_auto_20150603_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalbest',
            name='workout_assigned_date',
            field=models.ForeignKey(related_name='assigned_date_personal_best', to='workouts.AssignedWorkoutDate'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workoutresult',
            name='result_submit_date',
            field=models.DateField(default=datetime.date(2015, 6, 4), verbose_name=b'Result Submitted Date'),
            preserve_default=True,
        ),
    ]
