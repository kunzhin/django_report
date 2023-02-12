from django import template

register = template.Library()


@register.filter
def index(index, i):
    return index[i]

