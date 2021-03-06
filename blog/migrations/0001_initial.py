# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-22 05:05
from __future__ import unicode_literals

import blog.blocks
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.contrib.table_block.blocks
import wagtail.contrib.wagtailroutablepage.models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtaildocs', '0007_merge'),
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailimages', '0019_delete_filter'),
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'Blog Category',
                'verbose_name_plural': 'Blog Categories',
            },
        ),
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('image_cover', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_index_image_cover', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'Blog Index',
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('date_published', models.DateField(verbose_name='Post Date')),
                ('intro', models.TextField()),
                ('body', wagtail.wagtailcore.fields.StreamField([(b'heading', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'size', wagtail.wagtailcore.blocks.ChoiceBlock(blank=True, choices=[(b'h2', b'H2'), (b'h3', b'H3'), (b'h4', b'H4'), (b'h5', b'H5'), (b'h6', b'H6')], required=False))])), (b'paragraph', blog.blocks.CustomRichTextBlock(features=[b'bold', b'italic', b'ol', b'ul', b'hr', b'link', b'document-link'])), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=True)), (b'caaption', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'attribute', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'blockquote', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.TextBlock()), (b'attribute', wagtail.wagtailcore.blocks.CharBlock(blank=True, required=False))])), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock()), (b'document', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), (b'code', wagtail.wagtailcore.blocks.StructBlock([(b'language', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'python', b'Python'), (b'html', b'HTML'), (b'css', b'CSS'), (b'scss', b'SCSS'), (b'json', b'JSON')])), (b'style', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'syntax', b'default'), (b'monokai', b'monokai'), (b'xcode', b'xcode')])), (b'code', wagtail.wagtailcore.blocks.TextBlock())])), (b'raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock()), (b'table', wagtail.contrib.table_block.blocks.TableBlock())], blank=True, verbose_name='Page Body')),
                ('categories', modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.BlogCategory')),
                ('image_cover', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_post_image_cover', to='wagtailimages.Image')),
                ('related_pages', modelcluster.fields.ParentalManyToManyField(blank=True, related_name='_blogpage_related_pages_+', to='blog.BlogPage')),
            ],
            options={
                'verbose_name': 'Blog Post',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='blog.BlogPage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogTagIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_external', models.URLField(blank=True, help_text=b'Set external link if you want your                                      link points somewher outside this CMS System', null=True, verbose_name=b'External Link')),
                ('link_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name=b'Email Link')),
                ('explisit_name', models.CharField(blank=True, help_text=b'If you want to give different name than page name', max_length=64, null=True, verbose_name=b'Link Name')),
                ('short_name', models.CharField(blank=True, help_text=b'If you need different custom name for responsive design', max_length=32, null=True, verbose_name=b'Shortname')),
                ('icon_class', models.CharField(blank=True, help_text=b'In case you need custom css icon class <i>', max_length=255, null=True, verbose_name=b'Icon Class')),
                ('css_class', models.CharField(blank=True, help_text=b'Optional styling for menu item', max_length=255, null=True, verbose_name=b'CSS Class')),
            ],
            options={
                'verbose_name': 'Menu Item',
            },
        ),
        migrations.CreateModel(
            name='NavigationMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=255, verbose_name=b'Menu Name')),
            ],
            options={
                'verbose_name': 'Navigation Menu',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('taggit.tag',),
        ),
        migrations.CreateModel(
            name='NavigationMenuItem',
            fields=[
                ('menuitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.MenuItem')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('parent', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='blog.NavigationMenu')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=('blog.menuitem', models.Model),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='link_document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtaildocs.Document', verbose_name=b'Link to Document'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='link_page',
            field=models.ForeignKey(blank=True, help_text=b'Choose existing from existing page', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailcore.Page', verbose_name=b'Internal Page'),
        ),
        migrations.AddField(
            model_name='blogpagetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_blogpagetag_items', to='taggit.Tag'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blog.BlogPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
