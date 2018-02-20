from django import template


register = template.Library()

@register.simple_tag
def get_recent_posts(items=0):
    from blog.models import BlogPage
    if items > 0:
        return BlogPage.objects.live()[:items]
    return BlogPage.objects.live()[:5]


@register.simple_tag
def get_popular_posts(max=10):
    from django.db.models import Count, Q
    from blog.models import PageHitCounter, BlogPage
    
    hit_list = PageHitCounter.objects.values('page').annotate(Count('page')).order_by('-page__count')[:max]
    page_id = [ x['page'] for x in hit_list ]
    filters = Q(pk=page_id[0])
    for x in page_id[1:]:
        filters |= Q(pk=x)
    posts = BlogPage.objects.filter(filters)
    return posts
