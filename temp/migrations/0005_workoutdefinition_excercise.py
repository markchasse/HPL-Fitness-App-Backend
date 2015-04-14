# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0004_auto_20150410_0545'),
    ]

    operations = [
        migrations.AddField(
            model_name='workoutdefinition',
            name='excercise',
            field=models.ForeignKey(related_name='exercise', default=1, to='workouts.Exercise'),
            preserve_default=False,
        ),
    ]
