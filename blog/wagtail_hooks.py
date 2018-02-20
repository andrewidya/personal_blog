from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)

from blog.models import PageHitCounter


class PageHitCounterAdmin(ModelAdmin):
	model = PageHitCounter
	menu_label = 'Page Hit Counter'
	add_to_settings_menu = False
	menu_order = 400
	list_display = ['page', 'date_visited']
	search_fields = ('page',)
	
modeladmin_register(PageHitCounterAdmin)
