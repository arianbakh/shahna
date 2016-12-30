from django import template


register = template.Library()


@register.filter(name='persian_number')
def persian_number(value):
    try:
        int_value = int(value)
        return unichr(int_value + 1776)
    except ValueError:
        return value
