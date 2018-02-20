# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-28 13:39
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20180128_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='carousel',
            field=wagtail.wagtailcore.fields.StreamField([(b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), (b'caption', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'text', wagtail.wagtailcore.blocks.TextBlock(required=False))]))], required=False)), (b'video', wagtail.wagtailcore.blocks.StructBlock([(b'video', wagtail.wagtailembeds.blocks.EmbedBlock(required=False)), (b'caption', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'text', wagtail.wagtailcore.blocks.TextBlock(required=False))]))], required=False))], blank=True, null=True, verbose_name='Carousels'),
        ),
    ]
