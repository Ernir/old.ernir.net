# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bufftracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numericalbonus',
            name='bonus_value',
            field=models.IntegerField(choices=[(0, '+1'), (1, '+2'), (2, '+3'), (3, '+4'), (4, 'CL'), (5, 'CL/2'), (6, 'CL/3'), (7, 'CL, max 10')]),
        ),
        migrations.AlterField(
            model_name='temphpbonus',
            name='die_number',
            field=models.IntegerField(choices=[(0, '+1'), (1, '+2'), (2, '+3'), (3, '+4'), (4, 'CL'), (5, 'CL/2'), (6, 'CL/3'), (7, 'CL, max 10')]),
        ),
        migrations.AlterField(
            model_name='temphpbonus',
            name='other_bonus',
            field=models.IntegerField(choices=[(0, '+1'), (1, '+2'), (2, '+3'), (3, '+4'), (4, 'CL'), (5, 'CL/2'), (6, 'CL/3'), (7, 'CL, max 10')]),
        ),
    ]
