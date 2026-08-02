from django.urls import reverse
from django import template
from urllib.parse import urlencode
register = template.Library()

@register.inclusion_tag('reviews/_review_form.html')
def review_form(product_slug):
    """Render a review submission form for a given product."""
    return {
        'create_url': reverse('reviews:comment_create', args=[product_slug])
    }


@register.filter
def star_range(rate):
    rate = float(rate or 0)
    full = int(rate)
    half = 1 if (rate - full) >= 0.5 else 0
    empty = 5 - full - half
    return {"full": range(full), "half": range(half), "empty": range(empty)}