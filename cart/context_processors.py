from .models import Cart


def cart_item_count(request):
    """
    Injects `cart_count` into every template context.
    FIX: this function was referenced in settings.py but never existed,
         causing a 500 error on every single page load.
    """
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.items.count()
        except Cart.DoesNotExist:
            count = 0
    return {"cart_count": count}
 
