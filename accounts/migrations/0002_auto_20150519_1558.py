# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appuser',
            options={'verbose_name': 'Fitness Application User', 'verbose_name_plural': 'Fitness Application Users'},
        ),
    ]