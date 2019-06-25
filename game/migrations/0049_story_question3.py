# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0048_auto_20190128_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='question3',
            field=models.CharField(default=b'', max_length=2),
        ),
    ]
