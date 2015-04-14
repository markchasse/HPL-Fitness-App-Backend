# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0005_workoutdefinition_excercise'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workoutdefinition',
            old_name='excercise',
            new_name='exercise',
        ),
    ]
