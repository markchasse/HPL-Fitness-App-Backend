# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='Email')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('is_active', models.BooleanField(default=True)),
                ('profile_image', models.ImageField(null=True, upload_to=utils.file_upload_to, blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('user_role', models.PositiveSmallIntegerField(default=0, max_length=10, verbose_name='User Role', choices=[(0, 'user'), (1, 'coach'), (2, 'admin')])),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Fitness Application User',
                'verbose_name_plural': 'Fitness Application Users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AppCoach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_user', models.OneToOneField(related_name='coach_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AppStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parse_installation_id', models.CharField(max_length=100, null=True, blank=True)),
                ('apple_subscription_id', models.CharField(max_length=100, null=True, blank=True)),
                ('app_user', models.OneToOneField(related_name='student_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('subject', models.CharField(max_length=500)),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sender', models.ForeignKey(related_name='app_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['updated'],
                'verbose_name': 'Contact Us',
                'verbose_name_plural': 'Contact Us',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordResetRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscription_choices', models.PositiveSmallIntegerField(default=1, max_length=10, verbose_name='Subscription Choices', choices=[(1, 'free'), (2, 'paid')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='appstudent',
            name='subscription',
            field=models.OneToOneField(related_name='subscription_student', to='accounts.UserSubscription'),
            preserve_default=True,
        ),
    ]
