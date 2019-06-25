# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0042_auto_20190121_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publicgoods',
            old_name='data_selection',
            new_name='date_selection',
        ),
    ]
