import locale
from jdatetime import datetime as jdatetime


CHARACTER_REPLACE_DICT = {}
for english_number, persian_number in [(x - 1728, x) for x in range(1776, 1776 + 10)]:
    CHARACTER_REPLACE_DICT[chr(english_number)] = unichr(persian_number)


def convert_english_digits_to_persian(string):
    persian_string = u''
    for english_character in string:
        if english_character in CHARACTER_REPLACE_DICT:
            persian_string += CHARACTER_REPLACE_DICT[english_character]
        else:
            persian_string += english_character
    return persian_string


def get_jalali_string(gregorian_date):
    locale.setlocale(locale.LC_ALL, "fa_IR")
    jalali_string = jdatetime.fromgregorian(datetime=gregorian_date).strftime("%d %b %Y %H:%M:%S")
    return convert_english_digits_to_persian(jalali_string)
