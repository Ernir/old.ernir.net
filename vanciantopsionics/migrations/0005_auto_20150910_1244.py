# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vanciantopsionics', '0004_auto_20150910_1203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ('order',)},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ('parent__order', 'order')},
        ),
        migrations.AlterModelOptions(
            name='subsection',
            options={'ordering': ('parent__parent__order', 'parent__order', 'order')},
        ),
        migrations.AlterModelOptions(
            name='subsubsection',
            options={'ordering': ('parent__parent__parent__order', 'parent__parent__order', 'parent__order', 'order')},
        ),
    ]
