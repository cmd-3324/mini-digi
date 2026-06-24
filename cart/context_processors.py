def cart_item_count(request):
    count = 0
    if request.user.is_authenticated:
        from cart.models import Cart

        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            count = cart.items.count()
    return {"cart_item_count": count}
