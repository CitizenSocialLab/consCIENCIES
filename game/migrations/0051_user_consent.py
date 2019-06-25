# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0050_remove_user_partida'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='consent',
            field=models.BooleanField(default=False),
        ),
    ]
