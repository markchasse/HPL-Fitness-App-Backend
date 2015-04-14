# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import FitnessApp.utils


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedWorkout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assigned_date', models.DateTimeField(verbose_name='Date to deliver workout')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(related_name='student_assigned_workout', to='accounts.AppStudent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkoutDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(verbose_name='Workout Description')),
                ('title', models.CharField(max_length=100, verbose_name='Workout title')),
                ('image', models.ImageField(default=b'default/default_image.png', null=True, upload_to=FitnessApp.utils.file_upload_to, blank=True)),
                ('caption', models.CharField(max_length=250, null=True, verbose_name='image caption', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('coach', models.ForeignKey(related_name='coach_defined_workout', to='accounts.AppCoach')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkoutResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.CharField(max_length=1000, null=True, verbose_name='Workout Note', blank=True)),
                ('time', models.PositiveIntegerField(null=True, verbose_name='Workout Time', blank=True)),
                ('rounds', models.PositiveSmallIntegerField(max_length=10, null=True, verbose_name='Workout Rounds')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('assigned_workout', models.ForeignKey(related_name='app_workout', to='workouts.AssignedWorkout')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkoutType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='workout_type',
            field=models.ForeignKey(to='workouts.WorkoutType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedworkout',
            name='workout',
            field=models.ForeignKey(related_name='defined_workout_id', to='workouts.WorkoutDefinition'),
            preserve_default=True,
        ),
    ]
