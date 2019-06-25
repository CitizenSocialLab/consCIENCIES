# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0046_auto_20190122_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='enquesta_final_pr1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='enquesta_final_pr2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='enquesta_final_pr3',
        ),
        migrations.RemoveField(
            model_name='user',
            name='enquesta_final_pr4',
        ),
        migrations.RemoveField(
            model_name='user',
            name='enquesta_final_pr5',
        ),
        migrations.RemoveField(
            model_name='user',
            name='enquesta_final_pr6',
        ),
        migrations.RemoveField(
            model_name='user',
            name='enquesta_final_pr7',
        ),
        migrations.RemoveField(
            model_name='user',
            name='enquesta_final_pr8',
        ),
        migrations.RemoveField(
            model_name='user',
            name='enquesta_final_pr9',
        ),
        migrations.AddField(
            model_name='story',
            name='question1',
            field=models.CharField(default=b'', max_length=2),
        ),
        migrations.AddField(
            model_name='story',
            name='question2',
            field=models.CharField(default=b'', max_length=2),
        ),
    ]
