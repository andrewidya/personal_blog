from django.db import models


class NavigationMenuManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(menu_name=name)
