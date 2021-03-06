# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-28 12:33
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_remove_homepage_carousel'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='carousel',
            field=wagtail.wagtailcore.fields.StreamField([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock()), (b'text', wagtail.wagtailcore.blocks.TextBlock())])), (b'video', wagtail.wagtailembeds.blocks.EmbedBlock())], blank=True, verbose_name='Carousels'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, verbose_name='Body'),
        ),
    ]
