# from django import template
#
# register = template.library()
#
#
# # @register.filter
#
#
#
# register.range_filter('range_filter', range_filter)
import datetime
from django import template

register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


def range_filter(value):
    return value[0:500] + ".........."


register.filter('range_filter', range_filter)
