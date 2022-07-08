from django import template
from django.template.defaultfilters import lower, stringfilter

# Custom filters
register = template.Library()

@register.filter
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def index(string, substring):
    start = lower(string).index(lower(substring))
    end = start+len(substring)
    array = list(range(start,end))
    return array