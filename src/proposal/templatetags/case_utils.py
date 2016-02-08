from django import template

register = template.Library()


@register.filter
def lowerfirst(x):
    return x[0].lower() + x[1:]
