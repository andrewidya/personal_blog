# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-28 14:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_carousel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carousel',
            options={'verbose_name': 'Carousel Item'},
        ),
    ]
