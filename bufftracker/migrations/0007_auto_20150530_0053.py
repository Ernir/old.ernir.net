# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bufftracker', '0006_auto_20150530_0036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='numericalbonus',
            options={'ordering': ('bonus_formula__displayed_formula',)},
        ),
        migrations.RemoveField(
            model_name='numericalbonus',
            name='bonus_value',
        ),
        migrations.RemoveField(
            model_name='numericalbonus',
            name='formula',
        ),
        migrations.RemoveField(
            model_name='temphpbonus',
            name='die_number',
        ),
        migrations.RemoveField(
            model_name='temphpbonus',
            name='other_bonus',
        ),
        migrations.AddField(
            model_name='numericalbonus',
            name='bonus_formula',
            field=models.ForeignKey(to='bufftracker.CasterLevelFormula', null=True),
        ),
        migrations.AddField(
            model_name='temphpbonus',
            name='die_number_formula',
            field=models.ForeignKey(to='bufftracker.CasterLevelFormula', null=True, related_name='die_number'),
        ),
        migrations.AddField(
            model_name='temphpbonus',
            name='other_bonus_formula',
            field=models.ForeignKey(to='bufftracker.CasterLevelFormula', null=True, related_name='other_bonus'),
        ),
    ]
