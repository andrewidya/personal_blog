# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.db import models
from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase


from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                                InlinePanel,
                                                PageChooserPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route

from smartstream.edit_handlers import StreamFieldPanel

from blog.snippets import (BlogCategory, Tag, Carousel)
from blog.blocks import BodyStreamBlock


class SinglePage(Page):
    intro = models.TextField(blank=True)
    image_cover = models.ForeignKey('wagtailimages.Image', null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name='+')
    body = StreamField(BodyStreamBlock(), verbose_name='Page body', blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('image_cover'),
        FieldPanel('intro', classname="full"),
        StreamFieldPanel('body'),
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


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items',
                                 on_delete=models.CASCADE)


class RelatedPage(models.Model):
    page_from = ParentalKey('BlogPage', verbose_name='Page From', related_name='related_page_from')
    page_to = ParentalKey('BlogPage', verbose_name='Page To', related_name='related_page_to')
    

class PageHitCounter(models.Model):
    page = ParentalKey('blog.BlogPage')
    date_visited = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.page.title


class BlogPage(Page):
    date_published = models.DateTimeField('Post Date')
    image_cover = models.ForeignKey('wagtailimages.Image', null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='blog_post_image_cover')
    intro = models.TextField()
    body = StreamField(BodyStreamBlock(), verbose_name='Page Body', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField(BlogCategory, blank=True)

    subpage_type = ['blog.BlogPage']
    parent_page_type = ['blog.BlogIndexPage']

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date_published'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            InlinePanel('related_page_from', label='Related Pages',
                        panels=[PageChooserPanel('page_to')])
        ], heading="Blog Information"),
        ImageChooserPanel('image_cover'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Blog Post'

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['parent_page'] = self.parent_page
        return context
    
    def serve(self, request, *args, **kwargs):
        hit = PageHitCounter(page=self)
        hit.save()
        
        return super(BlogPage, self).serve(request, *args, **kwargs)
    
    @property
    def parent_page(self):
        return self.get_parent().specific

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/' + '/'.join(s.strip('/') for s in [
                self.get_parent().url, 'tags', tag.slug
            ])
        return tags

    @property
    def cover(self):
        return self.image_cover

    @property
    def related_pages(self):
        return [related.page_to for related in self.related_page_from.all()]

    @property
    def has_related_page(self):
        return self.related_page_from.count() > 0

    
    @property
    def date(self):
        """
        Return date of the publication page
        """
        return self.date_published.strftime('%b %d, %Y')
    
    @property
    def datetime(self):
        """
        Return datetime of the publication page
        """
        return self.date_published.strftime('%Y-%m-%d %H:%M:%S')


class BlogIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(blank=True)
    image_cover = models.ForeignKey('wagtailimages.Image', null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='blog_index_image_cover')

    parent_page_type = ['home.HomePage']
    subpage_type = ['blog.BlogPage']

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('image_cover')
    ]

    class Meta:
        verbose_name = 'Blog Index'

    @route('^tags/$', name='tag_archive')
    @route('^tags/(\w+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):
        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no blog posts tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        context = super(BlogIndexPage, self).get_context(request)
        posts = self.get_posts(tag=tag)
        context['posts'] = posts
        context['tag'] = tag
        context['page'] = self

        return render(request, 'blog/blog_index_page.html', context)

    @route('^categories/$', name='category_archive')
    @route('^categories/(\w+)/$', name='category_archive')
    def category_archive(self, request, category=None):
        context = super(BlogIndexPage, self).get_context(request)
        try:
            category = BlogCategory.objects.get(slug=category)
        except ObjectDoesNotExist:
            if category:
                msg = 'There are no categories of "{}"'.format(category)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(category=category)
        context['posts'] = posts
        context['category'] = category
        context['page'] = self

        return render(request, 'blog/blog_index_page.html', context)

    def get_context(self, request, *args, **kwargs):
        context = super(BlogIndexPage, self).get_context(request, *args, **kwargs)
        # context['posts'] = BlogPage.objects.descendant_of(self).live().order_by('-date_published')
        # posts = BlogIndexPage.objects.descendant_of(self).live().order_by('-date_published')
        # context['posts'] = self.paginate(request, posts, page_number=5)
        posts = self.get_posts()
        context['posts'] = self.paginate(request, posts)
        return context

    def children(self):
        return self.get_children().specific().live()

    def get_posts(self, tag=None, category=None):
        posts = BlogPage.objects.descendant_of(self).live().order_by('-date_published')
        if tag:
            posts = posts.filter(tags=tag)
        if category:
            posts = posts.filter(categories=category)
        return posts

    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags
    
    def paginate(self, request, posts, page_number=2):
        page = request.GET.get('page')
        paginator = Paginator(posts, page_number)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return posts


class BlogTagIndexPage(Page):

    class meta:
        verbose_name = 'Tag Page'
        verbose_name_plural = 'Tags Page'

    def get_context(self, request):
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        context = super(BlogTagIndexPage, self).get_context(request)
        context['blogpages'] = blogpages
        return context
