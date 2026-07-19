from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cart, CartItem
from shop.models import Product


def cart_detail(request):
    cart = None
    items = []
    total = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.items.select_related("product").all()
        total = sum(item.total_price for item in items)
    return render(
        request,
        "cart/cart_detail.html",
        {
            "cart": cart,
            "items": items,
            "total": total,
        },
    )


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "login_required": True}, status=401)
        return redirect("account_login")
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += int(request.POST.get("quantity", 1))
        item.save()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "cart_count": cart.items.count()})
    return redirect("cart:detail")


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get("quantity", 1))
    cart = item.cart

    if quantity > 0:
        item.quantity = quantity
        item.save()
        item_total = int(item.total_price)
        removed = False
    else:
        item.delete()
        item_total = 0
        removed = True

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        items = cart.items.select_related("product").all()
        return JsonResponse({
            "success": True,
            "item_total": item_total,
            "cart_total": int(sum(i.total_price for i in items)),
            "cart_count": cart.items.count(),
            "removed": removed,
        })
    return redirect("cart:detail")


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart = item.cart
    item.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        items = cart.items.select_related("product").all()
        return JsonResponse({
            "success": True,
            "cart_total": int(sum(i.total_price for i in items)),
            "cart_count": cart.items.count(),
        })
    return redirect("cart:detail")
