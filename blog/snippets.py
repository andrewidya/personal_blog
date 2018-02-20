from django.db import models
from django.utils.text import slugify

from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.fields import StreamField

from taggit.models import Tag as TaggitTag

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from smartstream.edit_handlers import StreamFieldPanel

from blog.fields import MenuItem
from blog.managers import NavigationMenuManager
from blog.blocks import CarouselBlock


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey('wagtailimages.Image', null=True, blank=True,
                             on_delete=models.SET_NULL, related_name='+')
    slug = models.CharField(max_length=255, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(BlogCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'


@register_snippet
class Tag(TaggitTag):

    class Meta:
        proxy = True


class NavigationMenuItem(Orderable, MenuItem):
    parent = ParentalKey('NavigationMenu', related_name='menu_items')


@register_snippet
class NavigationMenu(ClusterableModel):
    objects = NavigationMenuManager()
    menu_name = models.CharField(verbose_name="Menu Name", max_length=255)

    panels = [
        FieldPanel('menu_name', classname='full title'),
        InlinePanel('menu_items', label='Menu Items', help_text='Set the menu items for the current menu')
    ]

    class Meta:
        verbose_name = 'Navigation Menu'

    @property
    def items(self):
        return self.menu_items.all()

    def __str__(self):
        return self.menu_name


@register_snippet
class Carousel(models.Model):
    name = models.CharField(max_length=255)
    items = StreamField(CarouselBlock())

    panels = [
        FieldPanel('name', classname='full'),
        StreamFieldPanel('items')
    ]

    class Meta:
        verbose_name = 'Carousel Item'

    def __str__(self):
        return self.name

