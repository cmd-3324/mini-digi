from django.conf import settings
from .models import Category, Product


def categories(request):
    return {"categories": Category.objects.all()}


def clean_next_path(request):
    path = request.path
    for code, _ in settings.LANGUAGES:
        prefix = f"/{code}/"
        if path.startswith(prefix):
            path = "/" + path[len(prefix) :]
            break
    return {"clean_next": path}


def favorite_count(request):
    count = 0
    if request.user.is_authenticated:
        count = Product.objects.filter(favorited_by=request.user).count()
    return {"favorite_count": count}

def currency(request):
    """Make currency available in templates"""
    code = request.GET.get('currency')
    if code and code in ('USD', 'EUR', 'GBP', 'CAD'):
        request.session['currency'] = code
    return {
        'CURRENCY_CODE': request.session.get('currency', 'USD'),
    }

def all_count(request):
    count = Product.objects.filter(available=True).count()
    return {"all_count": count}