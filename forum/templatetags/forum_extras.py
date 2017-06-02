from django import template


register = template.Library()


@register.filter(name='persian_number')
def persian_number(value):
    try:
        int_value = int(value)
        return unichr(int_value + 1776)
    except ValueError:
        return value


@register.filter(name='rtl_list')
def rtl_list(input_list):
    output_list = []
    for i in range(0, len(input_list) / 2):
        output_list.append(input_list[i * 2 + 1])
        output_list.append(input_list[i * 2])
    if len(input_list) % 2 == 1:
        output_list.append(None)
        output_list.append(input_list[-1])
    return output_list
