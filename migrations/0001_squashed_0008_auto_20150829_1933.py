# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [('bufftracker', '0001_initial'), ('bufftracker', '0002_auto_20150524_1154'), ('bufftracker', '0003_auto_20150524_1218'), ('bufftracker', '0004_auto_20150527_1411'), ('bufftracker', '0005_auto_20150527_1417'), ('bufftracker', '0006_auto_20150530_0036'), ('bufftracker', '0007_auto_20150530_0053'), ('bufftracker', '0008_auto_20150829_1933')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MiscBonus',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ModifierType',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NumericalBonus',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('bonus_value', models.IntegerField(choices=[(1, '+1'), (2, '+2'), (3, '+3'), (4, '+4'), (11, 'CL'), (12, 'CL/2'), (13, 'CL/3')])),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('short_name', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('real_spell', models.BooleanField(default=True)),
                ('varies_by_cl', models.BooleanField(default=False)),
                ('size_modifying', models.BooleanField(default=False)),
                ('misc_bonuses', models.ManyToManyField(to='bufftracker.MiscBonus')),
                ('numerical_bonuses', models.ManyToManyField(to='bufftracker.NumericalBonus')),
                ('source', models.ForeignKey(to='bufftracker.Source')),
            ],
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StatisticGroup',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TempHPBonus',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('die_size', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='statistic',
            name='group',
            field=models.ForeignKey(to='bufftracker.StatisticGroup'),
        ),
        migrations.AddField(
            model_name='spell',
            name='temp_hp_bonuses',
            field=models.ManyToManyField(blank=True, to='bufftracker.TempHPBonus'),
        ),
        migrations.AddField(
            model_name='numericalbonus',
            name='applies_to',
            field=models.ForeignKey(to='bufftracker.Statistic'),
        ),
        migrations.AddField(
            model_name='numericalbonus',
            name='modifier_type',
            field=models.ForeignKey(to='bufftracker.ModifierType'),
        ),
        migrations.AlterField(
            model_name='numericalbonus',
            name='bonus_value',
            field=models.IntegerField(choices=[(0, '+1'), (1, '+2'), (2, '+3'), (3, '+4'), (4, 'CL'), (5, 'CL/2'), (6, 'CL/3'), (7, 'CL, max 10')]),
        ),
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
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='numericalbonus',
            name='bonus_value',
            field=models.IntegerField(choices=[(0, '+1'), (1, '+2'), (2, '+3'), (3, '+4'), (4, 'CL'), (5, 'CL/2'), (6, 'CL/3'), (7, 'CL, max 10'), (8, '2 + CL/3, max 5'), (9, '+25'), (10, 'CL/3, min 1, max 3'), (11, '-2'), (12, '-1')]),
        ),
        migrations.AlterModelOptions(
            name='numericalbonus',
            options={'ordering': ('formula', 'bonus_value')},
        ),
        migrations.CreateModel(
            name='CasterLevelFormula',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('displayed_formula', models.CharField(max_length=100)),
                ('function_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='numericalbonus',
            name='bonus_value',
            field=models.ForeignKey(to='bufftracker.CasterLevelFormula'),
        ),
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
        migrations.AddField(
            model_name='numericalbonus',
            name='bonus_formula',
            field=models.ForeignKey(null=True, to='bufftracker.CasterLevelFormula'),
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
        migrations.AlterModelOptions(
            name='casterlevelformula',
            options={'ordering': ('displayed_formula',)},
        ),
    ]
