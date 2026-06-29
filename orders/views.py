from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    items = cart.items.select_related("product").all() if cart else []
    total = sum(item.total_price for item in items)

    if request.method == "POST" and cart:
        order = Order.objects.create(user=request.user, total_price=total)
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
        cart.items.all().delete()
        return redirect("orders:confirmation", pk=order.pk)

    return render(request, "orders/checkout.html", {"items": items, "total": total})


@login_required
def confirmation(request, pk):
    from django.shortcuts import get_object_or_404

    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "orders/confirmation.html", {"order": order})
 
