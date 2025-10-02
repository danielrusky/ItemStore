import os

from django import template
from django.conf import settings

from config.settings import MEDIA_URL

register = template.Library()


@register.filter()
def media_tager(value):
    if value:
        return f'/media/{value}'
    return ''


@register.simple_tag()
def media_tager(value):
    if value:
        return f'/media/{value}'
    return ''
