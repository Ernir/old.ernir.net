# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bufftracker', '0005_auto_20150527_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='CasterLevelFormula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('displayed_formula', models.CharField(max_length=100)),
                ('function_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='numericalbonus',
            name='bonus_value',
            field=models.ForeignKey(to='bufftracker.CasterLevelFormula'),
        ),
        migrations.AlterField(
            model_name='temphpbonus',
            name='die_number',
            field=models.ForeignKey(to='bufftracker.CasterLevelFormula', related_name='die_number'),
        ),
        migrations.AlterField(
            model_name='temphpbonus',
            name='other_bonus',
            field=models.ForeignKey(to='bufftracker.CasterLevelFormula', related_name='other_bonus'),
        ),
    ]
