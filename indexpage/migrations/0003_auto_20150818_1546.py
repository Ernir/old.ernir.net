# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indexpage', '0002_auto_20150818_1427'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subsection',
            options={'ordering': ('parent_section__priority', 'priority')},
        ),
    ]
