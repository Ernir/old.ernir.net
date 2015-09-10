# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vanciantopsionics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('first_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('first_text', models.TextField()),
                ('order', models.IntegerField()),
                ('parent_chapter', models.ForeignKey(to='vanciantopsionics.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('first_text', models.TextField()),
                ('order', models.IntegerField()),
                ('parent_section', models.ForeignKey(to='vanciantopsionics.Section')),
            ],
        ),
        migrations.CreateModel(
            name='Subsubsection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('first_text', models.TextField()),
                ('order', models.IntegerField()),
                ('parent_subsection', models.ForeignKey(to='vanciantopsionics.Subsection')),
            ],
        ),
    ]
