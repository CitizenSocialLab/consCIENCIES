# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0052_auto_20190204_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='threshold',
            field=models.FloatField(default=0),
        ),
    ]
