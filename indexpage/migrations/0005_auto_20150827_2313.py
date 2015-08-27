# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indexpage', '0004_auto_20150827_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsection',
            name='text',
            field=models.TextField(default='', blank=True),
        ),
    ]
