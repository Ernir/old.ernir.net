# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bufftracker', '0004_auto_20150527_1411'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='numericalbonus',
            options={'ordering': ('formula', 'bonus_value')},
        ),
    ]
