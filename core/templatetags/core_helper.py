import re
from random import randint
from urllib.parse import parse_qs

from constance import config
from django import template
from django.conf import settings
from django.db.models import Q

from core.models import Category

register = template.Library()
numeric_test = re.compile("^\d+$")

@register.filter
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

@register.filter
def youtube(value, args):
    """
     returns youtube thumb url
    args s, l (small, large)

    """
    qs = value.split('?')
    video_id = parse_qs(qs[1])['v'][0]

    if args == 's':
        return "http://img.youtube.com/vi/%s/2.jpg" % video_id
    elif args == 'l':
        return "http://img.youtube.com/vi/%s/0.jpg" % video_id
    else:
        return None


@register.filter()
def get_seo_name(content):
    if hasattr(content, 'seo_name') and content.seo_name:
        return content.seo_name
    
    return config.INDEX_TITLE

@register.filter()
def get_seo_image(content):
    if hasattr(content, 'image') and content.image:
        return content.image.url

    return '/files/' + config.LOGO_IMAGE

@register.filter()
def get_seo_desc(content):
    if hasattr(content, 'seo_desc') and content.seo_desc:
        return content.seo_desc

    return config.INDEX_DESC

@register.filter()
def display_not_none(value):
    if value is not None:
        return value
    return ''

@register.simple_tag
def random_number(length=4):
    """
    Create a random integer with given length.
    For a length of 3 it will be between 100 and 999.
    For a length of 4 it will be between 1000 and 9999.
    """
    return randint(10**(length-1), (10**(length)-1))

@register.simple_tag
def header_categories():
    """
    Create a random integer with given length.
    For a length of 3 it will be between 100 and 999.
    For a length of 4 it will be between 1000 and 9999.
    """
    return Category.objects.filter(Q(status=True) and Q(parent=None)).order_by("display_order")

@register.simple_tag
def footer_categories():
    """
    Create a random integer with given length.
    For a length of 3 it will be between 100 and 999.
    For a length of 4 it will be between 1000 and 9999.
    """
    return Category.objects.filter(Q(status=True) and ~Q(parent=None)).order_by("display_order")
