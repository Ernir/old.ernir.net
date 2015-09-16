# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20150827_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
