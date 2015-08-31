# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bufftracker', '0002_auto_20150524_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spell',
            name='misc_bonuses',
            field=models.ManyToManyField(blank=True, to='bufftracker.MiscBonus'),
        ),
        migrations.AlterField(
            model_name='spell',
            name='numerical_bonuses',
            field=models.ManyToManyField(blank=True, to='bufftracker.NumericalBonus'),
        ),
        migrations.AlterField(
            model_name='spell',
            name='temp_hp_bonuses',
            field=models.ManyToManyField(blank=True, to='bufftracker.TempHPBonus'),
        ),
    ]
