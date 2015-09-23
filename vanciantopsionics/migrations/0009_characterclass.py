# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vanciantopsionics', '0008_auto_20150921_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterClass',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('short_name', models.CharField(max_length=200)),
                ('long_name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('slug', models.SlugField()),
                ('is_new', models.BooleanField(default=False)),
                ('class_type', models.CharField(choices=[('base', 'Base Class'), ('prestige', 'Prestige Class'), ('npc', 'NPC Class')], max_length=20)),
            ],
            options={
                'ordering': ('short_name',),
            },
        ),
    ]
