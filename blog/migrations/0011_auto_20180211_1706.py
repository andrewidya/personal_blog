# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-11 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20180211_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagehitcounter',
            name='hit',
        ),
        migrations.AddField(
            model_name='pagehitcounter',
            name='date_visited',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
