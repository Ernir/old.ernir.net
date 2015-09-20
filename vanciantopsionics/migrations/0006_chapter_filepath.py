# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vanciantopsionics', '0005_auto_20150910_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='filepath',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
    ]
