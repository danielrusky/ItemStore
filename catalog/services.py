from django.core.cache import cache

from catalog.models import Category
from config import settings


def get_category_list():
    if settings.CACHE_ENABLED:
        key = 'categories'
        categories = cache.get(key)
        if categories is None:
            categories = Category.objects.all()
            cache.set(key, categories)
    else:
        categories = Category.objects.all()
    return categories
