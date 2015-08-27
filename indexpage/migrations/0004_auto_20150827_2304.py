# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indexpage', '0003_auto_20150818_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsection',
            name='text',
            field=models.TextField(null=True),
        ),
    ]
