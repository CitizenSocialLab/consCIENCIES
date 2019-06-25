# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0039_auto_20190121_1149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partida',
            old_name='comentari',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='partida',
            old_name='data_fi_ronda',
            new_name='date_ended',
        ),
        migrations.RenameField(
            model_name='partida',
            old_name='data_finalitzacio',
            new_name='date_started',
        ),
        migrations.RenameField(
            model_name='partida',
            old_name='guanyen_igualment',
            new_name='goal_achieved',
        ),
        migrations.RenameField(
            model_name='partida',
            old_name='usuaris_registrats',
            new_name='registered',
        ),
        migrations.RenameField(
            model_name='partida',
            old_name='estat',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_finalitzacio',
            new_name='date_ended',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='data_creacio',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='data_inicialitzacio',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='num_rondes',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='objectiu_aconseguit',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='ronda_actual',
        ),
        migrations.AddField(
            model_name='partida',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='partida',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
