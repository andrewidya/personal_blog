# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-22 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogcategory_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategory',
            name='slug',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
