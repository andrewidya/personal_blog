# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-28 15:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('home', '0019_homepage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='image_cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homepage_image_cover', to='wagtailimages.Image'),
        ),
    ]
