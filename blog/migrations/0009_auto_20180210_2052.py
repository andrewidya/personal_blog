# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-10 20:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_homepage_singlepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='date_published',
            field=models.DateTimeField(verbose_name='Post Date'),
        ),
    ]
