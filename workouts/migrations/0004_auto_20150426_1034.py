# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150423_0602'),
        ('workouts', '0003_auto_20150423_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalBest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(related_name='student_personal_best', to='accounts.AppStudent')),
                ('workout_assigned_date', models.ForeignKey(related_name='assigned_date_personal_best', to='workouts.AssignedWorkoutDate', unique=True)),
            ],
            options={
                'ordering': ['updated'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='exerciseresult',
            name='result_submit_date',
            field=models.DateField(default=datetime.date(2015, 4, 26), verbose_name=b'Result Submitted Date'),
            preserve_default=True,
        ),
    ]
