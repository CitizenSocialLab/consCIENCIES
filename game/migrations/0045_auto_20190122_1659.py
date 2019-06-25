# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0044_auto_20190122_1634'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='rang_edat',
            new_name='age',
        ),
    ]
