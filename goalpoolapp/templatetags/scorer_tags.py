from django import template
import itertools

register = template.Library()

@register.filter(name='zip')
def zip_lists(a, b):
    return itertools.zip_longest(a, b)
