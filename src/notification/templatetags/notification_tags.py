from django import template

register = template.Library()


@register.filter
def unread(notifications):
    return notifications.filter(is_read=False)
