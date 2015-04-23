# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appstudent',
            name='subscription',
            field=models.OneToOneField(related_name='subscription_student', to='accounts.UserSubscription'),
            preserve_default=True,
        ),
    ]
