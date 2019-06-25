# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0038_story'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dictator',
            name='rival1',
        ),
        migrations.RemoveField(
            model_name='dictator',
            name='rival2',
        ),
        migrations.RemoveField(
            model_name='dictator',
            name='user',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='rival1',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='rival2',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='rival3',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='user',
        ),
        migrations.RemoveField(
            model_name='ronda',
            name='partida',
        ),
        migrations.RemoveField(
            model_name='trust',
            name='rival1',
        ),
        migrations.RemoveField(
            model_name='trust',
            name='rival2',
        ),
        migrations.RemoveField(
            model_name='trust',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userronda',
            name='ronda',
        ),
        migrations.RemoveField(
            model_name='userronda',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_clima',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_dictator',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_prisoner',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_total',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_trust',
        ),
        migrations.RemoveField(
            model_name='user',
            name='vals',
        ),
        migrations.DeleteModel(
            name='Dictator',
        ),
        migrations.DeleteModel(
            name='Prisoner',
        ),
        migrations.DeleteModel(
            name='Ronda',
        ),
        migrations.DeleteModel(
            name='Trust',
        ),
        migrations.DeleteModel(
            name='UserRonda',
        ),
    ]
