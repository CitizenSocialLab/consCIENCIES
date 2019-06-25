# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0047_auto_20190122_1741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='diners_actuals',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_inicials',
        ),
        migrations.RemoveField(
            model_name='user',
            name='guany_final',
        ),
    ]
