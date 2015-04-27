# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0002_exerciseresult_result_submit_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exerciseresult',
            name='exercise_result_workout',
        ),
        migrations.AddField(
            model_name='exerciseresult',
            name='exercise_result_workout_date',
            field=models.ForeignKey(related_name='workout_exercise_result', default=1, to='workouts.AssignedWorkoutDate'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exerciseresult',
            name='result_submit_date',
            field=models.DateField(default=datetime.date(2015, 4, 24), verbose_name=b'Result Submitted Date'),
            preserve_default=True,
        ),
    ]
