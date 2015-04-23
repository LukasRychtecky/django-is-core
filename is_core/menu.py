from django.core.exceptions import ImproperlyConfigured

class MenuItem(object):

    def __init__(self, title, collapsible, group, active=False, submenu_items=[]):
        self.title = title
        self.collapsible = collapsible
        self.submenu_items = submenu_items
        self.group = group
        self.active = active


class LinkMenuItem(MenuItem):

    def __init__(self, title, url, group=None, active=False, submenu_items=[]):
        super(LinkMenuItem, self).__init__(title, False, group, active, submenu_items)
        self.url = url

    def __unicode__(self):
        return self.title


class CollapsibleMenuItem(MenuItem):

    def __init__(self, title, url=None, group=None, active=False, submenu_items=[]):
        super(CollapsibleMenuItem, self).__init__(title, True, group, active, submenu_items)
        self.url = url


class MenuGenerator(object):

    def __init__(self, request, site, active_groups):
        self.request = request
        self.site = site
        self.active_groups = active_groups

    def get_menu_items(self, items):
        menu_items = []
        if self.active_groups:
            group = self.active_groups[0]
        else:
            group = None

        for item in items:
            if isinstance(item, MenuItem):
                menu_items.append(item)
            elif self.site.has_is_core(item):
                item = self.site.get_is_core(item)
                menu_item = item.get_menu_item(self.request, group)
                if menu_item:
                    menu_items.append(menu_item)
            else:
                raise ImproperlyConfigured('IS Core or Menu item not found for name "%s"' % item)
        return menu_items

    def get_menu_structure(self):
        return self.site.get_is_core_names()
