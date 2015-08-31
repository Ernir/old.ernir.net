# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bufftracker', '0007_auto_20150530_0053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casterlevelformula',
            options={'ordering': ('displayed_formula',)},
        ),
    ]
