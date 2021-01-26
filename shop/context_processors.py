from django.core.cache import cache
from .models import Category


def categories(request):
    cached_categories = cache.get('categories')
    if cached_categories is not None:
        return cached_categories
    context = {'categories': Category.objects.filter(active=True)}
    cache.set('categories', context, 60 * 3)
    return context
