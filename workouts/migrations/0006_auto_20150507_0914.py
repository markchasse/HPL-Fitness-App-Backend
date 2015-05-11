# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0005_auto_20150426_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkoutResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.CharField(max_length=1000, null=True, verbose_name='Workout Result Note', blank=True)),
                ('time_taken', models.PositiveIntegerField(null=True, verbose_name='Workout Time In Seconds', blank=True)),
                ('rounds', models.PositiveSmallIntegerField(max_length=10, null=True, verbose_name='Workout Rounds', blank=True)),
                ('result_submit_date', models.DateField(default=datetime.date(2015, 5, 7), verbose_name=b'Result Submitted Date')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('result_workout_assign_date', models.ForeignKey(related_name='workout_result', to='workouts.AssignedWorkoutDate')),
            ],
            options={
                'ordering': ['result_workout_assign_date'],
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='ExerciseType',
            new_name='WorkoutType',
        ),
        migrations.RemoveField(
            model_name='exerciseresult',
            name='exercise',
        ),
        migrations.RemoveField(
            model_name='exerciseresult',
            name='exercise_result_workout_date',
        ),
        migrations.DeleteModel(
            name='ExerciseResult',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='exercise_header',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='exercise_notes',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='exercise_type',
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='workout_content',
            field=models.CharField(max_length=500, null=True, verbose_name='Workout Content', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='workout_header',
            field=models.CharField(max_length=500, null=True, verbose_name='WarmUp Header', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='workout_nick_name',
            field=models.CharField(max_length=200, null=True, verbose_name='Workout Nick Name', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='workout_type',
            field=models.ForeignKey(related_name='type_of_workout', default=None, to='workouts.WorkoutType'),
            preserve_default=True,
        ),
    ]
