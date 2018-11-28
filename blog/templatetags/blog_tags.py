from django import template
from django.db.models import Count, Q

from blog.models import BlogPage, PageHitCounter


register = template.Library()

@register.simple_tag()
def has_recent_posts():
    pages = BlogPage.objects.live().order_by('date_published')
    return pages.exists()

@register.inclusion_tag("blog/tags/recent_posts.html", takes_context=False)
def get_recent_posts(items=0):
    pages = BlogPage.objects.live().order_by('date_published')
    if items > 0:
        pages = pages[:items]
    else:
        pages = pages[:4]

    return {
        'pages': pages
    }

@register.inclusion_tag("blog/tags/popular_posts.html", takes_context=False)
def get_popular_posts(max=10):
    hit_list = PageHitCounter.objects.values('page').annotate(Count('page')).order_by('-page__count')[:max]
    page_id = [ x['page'] for x in hit_list ]

    filters = Q(pk=page_id[0])
    for x in page_id[1:]:
        filters |= Q(pk=x)

    posts = BlogPage.objects.filter(filters)

    return {
        'pages' : posts
    }
