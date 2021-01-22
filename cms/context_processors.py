from django.conf import settings
from django.core.cache import cache

from .models import Menu


def menu(request):
    cached_menus = cache.get(settings.MENU_CACHE_KEY)
    if cached_menus is not None:
        return cached_menus
    menus = Menu.objects.filter()
    context = {'menu': {}}
    for menu in menus:
        context['menu'][menu.slug] = menu
    cache.set(settings.MENU_CACHE_KEY, context, settings.MENU_CACHE_TIMEOUT)
    return context
