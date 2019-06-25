# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0040_auto_20190121_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='date_ended',
            field=models.DateTimeField(null=True),
        ),
    ]
