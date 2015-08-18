# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_entry_excerpt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ('-published',), 'verbose_name_plural': 'entries'},
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='associated_with',
            field=models.ForeignKey(to='blog.Entry', related_name='comments'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', related_name='entries'),
        ),
    ]
