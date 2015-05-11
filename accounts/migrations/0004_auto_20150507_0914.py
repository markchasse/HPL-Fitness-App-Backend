# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_contactus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'ordering': ['updated'], 'verbose_name': 'Contact Us', 'verbose_name_plural': 'Contact Us'},
        ),
    ]
