# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vanciantopsionics', '0007_spell'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spell',
            options={'ordering': ('title',)},
        ),
        migrations.AddField(
            model_name='spell',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
    ]
