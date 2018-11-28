from django import template

from wagtail.wagtailcore.models import Page


register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


def has_children(page):
    return page.get_children().live().exists()


def is_active(page, current_page):
    return current_page.url.startwith(page.url) if current_page else False


@register.inclusion_tag("blog/tags/top_menu.html", takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = (calling_page.url.startswith(menuitem.url) if calling_page else False)

    return {
        'calling_page': calling_page,
        'menus': menuitems,
        'request': context['request']
    }


@register.inclusion_tag("blog/tags/sub_menu.html", takes_context=True)
def sub_menu(context, parent, calling_page=None):
    sub_menus = parent.get_children().live().in_menu()
    for sub_menu in sub_menus:
        sub_menu.has_dropdown = has_menu_children(sub_menu)
        sub_menu.active = (calling_page.url.startswith(sub_menu.url) if calling_page else False)

    return {
        'parent': parent,
        'sub_menus': sub_menus,
        'request': context['request']
    }


@register.inclusion_tag("blog/tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 2:
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gt=1)

    return {
        'ancestors': ancestors,
        'request': context['request']
    }
