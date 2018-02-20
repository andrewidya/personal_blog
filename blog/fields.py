from django.db import models

from wagtail.wagtailadmin.edit_handlers import (MultiFieldPanel, FieldPanel, PageChooserPanel)
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel


class LinkField(models.Model):
    """Model field to handle link item
    """
    link_external = models.URLField(verbose_name='External Link', blank=True, null=True,
                                    help_text='Set external link if you want your \
                                     link points somewher outside this CMS System')
    link_page = models.ForeignKey('wagtailcore.Page', verbose_name='Internal Page',
                                  on_delete=models.SET_NULL, blank=True, null=True,
                                  help_text='Choose existing from existing page')
    link_document = models.ForeignKey('wagtaildocs.Document', verbose_name='Link to Document',
                                      on_delete=models.SET_NULL, blank=True, null=True)
    link_email = models.EmailField(verbose_name='Email Link', blank=True, null=True)

    panels = [
        MultiFieldPanel([
            PageChooserPanel('link_page'),
            FieldPanel('link_external'),
            DocumentChooserPanel('link_document'),
            FieldPanel('link_email'),
        ], heading="Link Type", classname="full"),
    ]

    class Meta:
        abstract = True

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_external:
            return self.link_external
        elif self.link_document:
            return self.link_document.url
        elif self.link_email:
            return 'mailto:{}'.format(self.link_email)
        else:
            return '#'


class MenuItem(LinkField):
    explisit_name = models.CharField(verbose_name='Link Name', max_length=64, blank=True,
                                     null=True, help_text='If you want to give different name than page name')
    short_name = models.CharField(verbose_name='Shortname', max_length=32, blank=True,
                                  null=True, help_text='If you need different custom name for responsive design')
    icon_class = models.CharField(verbose_name='Icon Class', max_length=255, blank=True,
                                  null=True, help_text='In case you need custom css icon class <i>')
    css_class = models.CharField(verbose_name='CSS Class', blank=True, null=True, max_length=255,
                                 help_text='Optional styling for menu item')

    panels = LinkField.panels + [
        FieldPanel('explisit_name'),
        FieldPanel('short_name'),
        FieldPanel('icon_class'),
        FieldPanel('css_class'),
    ]

    class Meta:
        verbose_name = "Menu Item"

    @property
    def title(self):
        if self.explisit_name:
            return self.explisit_name
        elif self.link_page:
            return self.link_page.title
        elif self.link_document:
            return self.link_document.title
        else:
            return None

    @property
    def url(self):
        return self.link

    def __str__(self):
        if self.explisit_name:
            title = self.explisit_name
        elif self.link_page:
            title = self.link_page.title
        else:
            title = ''
        return "{1} ({2})".format(title, self.short_name)
