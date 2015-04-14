# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0003_remove_workoutdefinition_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutdefinition',
            name='cooldown_notes',
            field=models.TextField(null=True, verbose_name='CoolDown Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workoutdefinition',
            name='extracredit_notes',
            field=models.TextField(null=True, verbose_name='Extra Credit Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workoutdefinition',
            name='homework_notes',
            field=models.TextField(null=True, verbose_name='Homework Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workoutdefinition',
            name='substitution_notes',
            field=models.TextField(null=True, verbose_name='Substitution Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workoutdefinition',
            name='warmup_notes',
            field=models.TextField(null=True, verbose_name='WarmUp Notes', blank=True),
            preserve_default=True,
        ),
    ]
