# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vanciantopsionics', '0003_chapter_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='parent_chapter',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='subsection',
            old_name='parent_section',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='subsubsection',
            old_name='parent_subsection',
            new_name='parent',
        ),
    ]
