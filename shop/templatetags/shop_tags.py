from django import template
from urllib.parse import urlencode
# from shop.models import Products
# from shop.models.product import Product
register = template.Library()
CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'CAD': 'C$',
}


@register.simple_tag(takes_context=True)
def qs(context, **kwargs):
    request = context["request"]
    params = request.GET.copy()
    for key, value in kwargs.items():
        if value is None or value == "":
            params.pop(key, None)
        else:
            params[key] = value
    return params.urlencode()



@register.filter
def currency_symbol(currency_code):
    return CURRENCY_SYMBOLS.get(currency_code, '$')


# @register.simple_tag(takes_context=True)
# def available_product_count():
#     return Product.objects.filter(available=True).count()