# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0036_publicgoods'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='current_game',
            field=models.ForeignKey(related_name='current_game', to='game.Partida', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='partida',
            field=models.ForeignKey(related_name='partida', to='game.Partida', null=True),
        ),
    ]
