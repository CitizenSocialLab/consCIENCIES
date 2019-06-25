# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0043_auto_20190121_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='genere',
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default=b'', max_length=2),
        ),
    ]
