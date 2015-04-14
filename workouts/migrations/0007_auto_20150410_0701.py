# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0006_auto_20150410_0615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutdefinition',
            name='exercise',
        ),
        migrations.AddField(
            model_name='exercise',
            name='workout',
            field=models.ForeignKey(related_name='workout', default=1, to='workouts.WorkoutDefinition'),
            preserve_default=False,
        ),
    ]
