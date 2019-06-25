# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0041_story_date_ended'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='data_registre',
            new_name='date_created',
        ),
        migrations.RemoveField(
            model_name='user',
            name='data_creacio',
        ),
        migrations.AddField(
            model_name='user',
            name='date_register',
            field=models.DateTimeField(null=True),
        ),
    ]
