# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bufftracker', '0003_auto_20150524_1218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='miscbonus',
            options={'ordering': ('description',)},
        ),
        migrations.AlterModelOptions(
            name='modifiertype',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='spell',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='statistic',
            options={'ordering': ('group__name', 'name')},
        ),
        migrations.AlterModelOptions(
            name='statisticgroup',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='numericalbonus',
            name='formula',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spell',
            name='additional_note',
            field=models.CharField(default='', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='numericalbonus',
            name='bonus_value',
            field=models.IntegerField(choices=[(0, '+1'), (1, '+2'), (2, '+3'), (3, '+4'), (4, 'CL'), (5, 'CL/2'), (6, 'CL/3'), (7, 'CL, max 10'), (8, '2 + CL/3, max 5'), (9, '+25'), (10, 'CL/3, min 1, max 3'), (11, '-2'), (12, '-1')]),
        ),
        migrations.AlterField(
            model_name='temphpbonus',
            name='die_number',
            field=models.IntegerField(choices=[(0, '+1'), (1, '+2'), (2, '+3'), (3, '+4'), (4, 'CL'), (5, 'CL/2'), (6, 'CL/3'), (7, 'CL, max 10'), (8, '2 + CL/3, max 5'), (9, '+25'), (10, 'CL/3, min 1, max 3'), (11, '-2'), (12, '-1')]),
        ),
        migrations.AlterField(
            model_name='temphpbonus',
            name='other_bonus',
            field=models.IntegerField(choices=[(0, '+1'), (1, '+2'), (2, '+3'), (3, '+4'), (4, 'CL'), (5, 'CL/2'), (6, 'CL/3'), (7, 'CL, max 10'), (8, '2 + CL/3, max 5'), (9, '+25'), (10, 'CL/3, min 1, max 3'), (11, '-2'), (12, '-1')]),
        ),
    ]
