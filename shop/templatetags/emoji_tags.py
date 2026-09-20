import html

from django import template

register = template.Library()


@register.filter
def decode_emoji(value):
    if value:
        return html.unescape(value)
    return value
