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
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(related_name='student_assigned_workout', to='accounts.AppStudent')),
            ],
            options={
                'ordering': ['updated'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssignedWorkoutDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assigned_date', models.DateTimeField(verbose_name='Date to deliver workout')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('assigned_workout', models.ForeignKey(related_name='assigned_dates', to='workouts.AssignedWorkout')),
            ],
            options={
                'ordering': ['assigned_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exercise_header', models.CharField(max_length=500, verbose_name='Exercise Header')),
                ('exercise_content', models.CharField(max_length=800, null=True, verbose_name='Exercise content', blank=True)),
                ('exercise_notes', models.TextField(verbose_name='Exercise Notes')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['updated'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExerciseResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.CharField(max_length=1000, null=True, verbose_name='Exercise Note', blank=True)),
                ('time_taken', models.PositiveIntegerField(null=True, verbose_name='Exercise Time In Seconds', blank=True)),
                ('rounds', models.PositiveSmallIntegerField(max_length=10, null=True, verbose_name='Exercise Rounds', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('exercise', models.ForeignKey(related_name='exercise_result', to='workouts.Exercise')),
                ('exercise_result_workout', models.ForeignKey(related_name='workout_exercise_result', to='workouts.AssignedWorkout')),
            ],
            options={
                'ordering': ['updated'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExerciseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_name', models.CharField(unique=True, max_length=100)),
                ('type_description', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkoutDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=b'default/default_image.png', null=True, upload_to=FitnessApp.utils.file_upload_to, blank=True)),
                ('caption', models.CharField(max_length=250, null=True, verbose_name='Image Caption', blank=True)),
                ('introduction_header', models.CharField(max_length=500, verbose_name='Introduction Header')),
                ('introduction_textfield', models.TextField(verbose_name='Introduction Text')),
                ('warmup_header', models.CharField(max_length=500, null=True, verbose_name='WarmUp Header', blank=True)),
                ('warmup_content', models.CharField(max_length=800, null=True, verbose_name='WarmUp content', blank=True)),
                ('warmup_notes', models.TextField(null=True, verbose_name='WarmUp Notes', blank=True)),
                ('substitution_header', models.CharField(max_length=500, null=True, verbose_name='Substitution Header', blank=True)),
                ('substitution_content', models.CharField(max_length=800, null=True, verbose_name='Substitution content', blank=True)),
                ('substitution_notes', models.TextField(null=True, verbose_name='Substitution Notes', blank=True)),
                ('cooldown_header', models.CharField(max_length=500, null=True, verbose_name='CoolDown Header', blank=True)),
                ('cooldown_content', models.CharField(max_length=800, null=True, verbose_name='CoolDown content', blank=True)),
                ('cooldown_notes', models.TextField(null=True, verbose_name='CoolDown Notes', blank=True)),
                ('extracredit_header', models.CharField(max_length=500, null=True, verbose_name='Extra credit Header', blank=True)),
                ('extracredit_content', models.CharField(max_length=800, null=True, verbose_name='extra credit content', blank=True)),
                ('extracredit_notes', models.TextField(null=True, verbose_name='Extra Credit Notes', blank=True)),
                ('homework_header', models.CharField(max_length=500, null=True, verbose_name='Home Work Header', blank=True)),
                ('homework_content', models.CharField(max_length=800, null=True, verbose_name='Home Work content', blank=True)),
                ('homework_notes', models.TextField(null=True, verbose_name='Homework Notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ManyToManyField(related_name='assigned_workout', through='workouts.AssignedWorkout', to='accounts.AppStudent')),
                ('coach', models.ForeignKey(related_name='coach_defined_workout', to='accounts.AppCoach')),
                ('exercises', models.ManyToManyField(related_name='exercise_workout', to='workouts.Exercise')),
            ],
            options={
                'ordering': ['updated'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='exercise',
            name='exercise_type',
            field=models.ForeignKey(related_name='type_of_exercise', to='workouts.ExerciseType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignedworkout',
            name='workout',
            field=models.ForeignKey(related_name='assigned_workouts', to='workouts.WorkoutDefinition'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='assignedworkout',
            unique_together=set([('student', 'workout')]),
        ),
    ]
