# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0045_auto_20190122_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='codi_postal',
        ),
        migrations.RemoveField(
            model_name='user',
            name='estat_civil',
        ),
        migrations.RemoveField(
            model_name='user',
            name='nivell_estudis',
        ),
        migrations.RemoveField(
            model_name='user',
            name='origen',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pais',
        ),
        migrations.RemoveField(
            model_name='user',
            name='residencia',
        ),
        migrations.RemoveField(
            model_name='user',
            name='situacio_laboral',
        ),
        migrations.AddField(
            model_name='user',
            name='postal_code',
            field=models.CharField(default=b'', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='studies',
            field=models.CharField(default=b'', max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.CharField(default=b'', max_length=2),
        ),
    ]
