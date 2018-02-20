# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-22 05:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='related_pages',
        ),
        migrations.AddField(
            model_name='relatedpage',
            name='page_from',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_page_from', to='blog.BlogPage', verbose_name='Page From'),
        ),
        migrations.AddField(
            model_name='relatedpage',
            name='page_to',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_page_to', to='blog.BlogPage', verbose_name='Page To'),
        ),
    ]