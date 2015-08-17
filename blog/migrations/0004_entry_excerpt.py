# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150817_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='excerpt',
            field=models.CharField(default='This is an excerpt', max_length=100),
            preserve_default=False,
        ),
    ]
