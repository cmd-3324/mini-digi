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