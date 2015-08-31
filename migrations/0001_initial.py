# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MiscBonus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ModifierType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NumericalBonus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('bonus_value', models.IntegerField(choices=[(1, '+1'), (2, '+2'), (3, '+3'), (4, '+4'), (11, 'CL'), (12, 'CL/2'), (13, 'CL/3')])),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('short_name', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StatisticGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TempHPBonus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('die_number', models.IntegerField(choices=[(1, '+1'), (2, '+2'), (3, '+3'), (4, '+4'), (11, 'CL'), (12, 'CL/2'), (13, 'CL/3')])),
                ('die_size', models.IntegerField(default=0)),
                ('other_bonus', models.IntegerField(choices=[(1, '+1'), (2, '+2'), (3, '+3'), (4, '+4'), (11, 'CL'), (12, 'CL/2'), (13, 'CL/3')])),
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
            field=models.ManyToManyField(to='bufftracker.TempHPBonus'),
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
    ]
