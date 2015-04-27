# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0004_auto_20150426_1034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exerciseresult',
            options={'ordering': ['exercise_result_workout_date']},
        ),
    ]
