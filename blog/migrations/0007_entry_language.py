# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20150818_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='language',
            field=models.CharField(choices=[('IS', 'Icelandic'), ('EN', 'English')], max_length=2, default='EN'),
        ),
    ]
