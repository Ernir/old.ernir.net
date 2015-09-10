# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vanciantopsionics', '0002_chapter_section_subsection_subsubsection'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
