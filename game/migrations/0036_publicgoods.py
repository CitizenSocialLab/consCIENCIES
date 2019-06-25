# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0035_auto_20170411_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicGoods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selection', models.CharField(default=b'', max_length=1)),
                ('is_robot', models.BooleanField(default=True)),
                ('data_selection', models.DateTimeField(null=True)),
                ('game', models.ForeignKey(to='game.Partida', null=True)),
                ('user', models.ForeignKey(to='game.User')),
            ],
        ),
    ]
