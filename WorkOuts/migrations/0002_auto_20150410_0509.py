# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('workout_header', models.CharField(max_length=500, verbose_name='WorkOut Header')),
                ('workout_content', models.CharField(max_length=800, null=True, verbose_name='WorkOut content', blank=True)),
                ('workout_notes', models.TextField(verbose_name='WorkOut Notes')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('workout_type', models.OneToOneField(to='workouts.WorkoutType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='workoutdefinition',
            name='description',
        ),
        migrations.RemoveField(
            model_name='workoutdefinition',
            name='workout_type',
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='cooldown_content',
            field=models.CharField(max_length=800, null=True, verbose_name='CoolDown content', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='cooldown_header',
            field=models.CharField(max_length=500, null=True, verbose_name='CoolDown Header', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='cooldown_notes',
            field=models.TextField(default=datetime.datetime(2015, 4, 10, 12, 6, 34, 283405, tzinfo=utc), verbose_name='CoolDown Notes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='extracredit_content',
            field=models.CharField(max_length=800, null=True, verbose_name='extra credit content', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='extracredit_header',
            field=models.CharField(max_length=500, null=True, verbose_name='Extra credit Header', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='extracredit_notes',
            field=models.TextField(default=datetime.datetime(2015, 4, 10, 12, 7, 2, 935557, tzinfo=utc), verbose_name='Extra Credit Notes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='homework_content',
            field=models.CharField(max_length=800, null=True, verbose_name='Home Work content', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='homework_header',
            field=models.CharField(max_length=500, null=True, verbose_name='Home Work Header', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='homework_notes',
            field=models.TextField(default=datetime.datetime(2015, 4, 10, 12, 7, 14, 858154, tzinfo=utc), verbose_name='Homework Notes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='introduction_header',
            field=models.CharField(default=datetime.datetime(2015, 4, 10, 12, 8, 40, 850550, tzinfo=utc), max_length=500, verbose_name='Introduction Header'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='introduction_textfield',
            field=models.TextField(default=datetime.datetime(2015, 4, 10, 12, 8, 49, 989908, tzinfo=utc), verbose_name='Introduction Text'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='substitution_content',
            field=models.CharField(max_length=800, null=True, verbose_name='Substitution content', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='substitution_header',
            field=models.CharField(max_length=500, null=True, verbose_name='substitution Header', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='substitution_notes',
            field=models.TextField(default=datetime.datetime(2015, 4, 10, 12, 9, 5, 808833, tzinfo=utc), verbose_name='Substitution Notes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='warmup_content',
            field=models.CharField(max_length=800, null=True, verbose_name='WarmUp content', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='warmup_header',
            field=models.CharField(max_length=500, null=True, verbose_name='WarmUp Header', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workoutdefinition',
            name='warmup_notes',
            field=models.TextField(default=datetime.datetime(2015, 4, 10, 12, 9, 14, 21766, tzinfo=utc), verbose_name='WarmUp Notes'),
            preserve_default=False,
        ),
    ]
