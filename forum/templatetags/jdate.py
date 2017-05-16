from django import template
from persian_tools import get_jalali_string

register = template.Library()

@register.filter
def jdate(gregorian_date):
    return get_jalali_string(gregorian_date)
