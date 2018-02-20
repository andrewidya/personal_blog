from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from smartstream.edit_handlers import StreamFieldPanel

from blog.blocks import BodyStreamBlock
from blog.snippets import Carousel


class SinglePage(Page):
    intro = models.TextField(blank=True)
    image_cover = models.ForeignKey('wagtailimages.Image', null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name='+')
    body = StreamField(BodyStreamBlock(), verbose_name='Page body', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        StreamFieldPanel('body'),
        ImageChooserPanel('image_cover')
    ]


class HomePage(Page):
    carousel = models.ForeignKey(Carousel, verbose_name='Carousel', blank=True,
                                 null=True, on_delete=models.SET_NULL)
    body = StreamField(BodyStreamBlock(), verbose_name='Body', blank=True, null=True)
    image_cover = models.ForeignKey('wagtailimages.Image', null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='homepage_image_cover')

    content_panels = Page.content_panels + [
        FieldPanel('carousel'),
        StreamFieldPanel('body'),
    ]
