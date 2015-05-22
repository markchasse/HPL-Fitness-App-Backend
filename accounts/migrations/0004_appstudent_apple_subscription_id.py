# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_appstudent_parse_installation_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='appstudent',
            name='apple_subscription_id',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
