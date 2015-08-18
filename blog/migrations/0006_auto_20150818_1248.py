# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150818_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='excerpt',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(max_length=400),
        ),
    ]
