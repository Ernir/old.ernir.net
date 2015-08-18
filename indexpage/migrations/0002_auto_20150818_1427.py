# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indexpage', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ('priority',)},
        ),
        migrations.AlterModelOptions(
            name='subsection',
            options={'ordering': ('priority',)},
        ),
        migrations.AddField(
            model_name='section',
            name='priority',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subsection',
            name='priority',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
