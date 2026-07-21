import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext as _
from orders.models import Order
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from support.models import Ticket
@login_required
def home(request):
    orders = request.user.orders.order_by("-created_at")[:5]
    stats = {
        "total_orders": request.user.orders.count(),
        "pending_orders": request.user.orders.filter(is_paid=False).count(),
        "completed_orders": request.user.orders.filter(is_paid=True).count(),
        "favorites_count": request.user.favorite_products.count(),
    }
    return render(request, "dashboard/home.html", {
        "orders": orders,
        "stats": stats,
    })


@login_required
def profile(request):
    profile = request.user.profile
    return render(request, "dashboard/profile.html", {
        "profile": profile,
    })


@login_required
@require_POST
def profile_update(request):
    data = json.loads(request.body)
    user = request.user
    profile = user.profile
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.email = data.get("email", user.email)
    profile.phone = data.get("phone", profile.phone)
    profile.address_line1 = data.get("address_line1", profile.address_line1)
    profile.address_line2 = data.get("address_line2", profile.address_line2)
    profile.city = data.get("city", profile.city)
    profile.state = data.get("state", profile.state)
    profile.zip_code = data.get("zip_code", profile.zip_code)
    user.save()
    profile.save()
    return JsonResponse({"ok": True, "message": _("Profile updated successfully!")})


@login_required
@require_POST
def change_password(request):
    form = PasswordChangeForm(request.user, json.loads(request.body))
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return JsonResponse({"ok": True, "message": _("Password changed successfully!")})
    errors = []
    for field_errors in form.errors.values():
        errors.extend(field_errors)
    return JsonResponse({"ok": False, "error": " ".join(errors)})


@login_required
def wishlist(request):
    products = request.user.favorite_products.select_related("category").order_by("-id")

    q = request.GET.get("q", "").strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(name_fr__icontains=q) | Q(name_ru__icontains=q)
        )

    sort = request.GET.get("sort", "-id")
    if sort not in ("-id", "id", "price", "-price"):
        sort = "-id"
    products = products.order_by(sort)

    page_obj = Paginator(products, 12).get_page(request.GET.get("page"))
    return render(request, "dashboard/wishlist.html", {
        "products": page_obj, "page_obj": page_obj,
        "q": q, "sort": sort,
    })


@login_required
def wishlist_search_ajax(request):
    q = request.GET.get("q", "").strip()
    results = []
    if q:
        products = request.user.favorite_products.filter(
            Q(name__icontains=q) | Q(name_fr__icontains=q) | Q(name_ru__icontains=q)
        )[:8]
        for p in products:
            results.append({
                "id": p.pk,
                "name": p.translated_name,
                "price": f"{p.price:,.0f}",
                "image": p.image.url if p.image else "",
                "url": reverse("shop:product_detail", args=[p.pk]),
            })
    return JsonResponse({"results": results})

@login_required
def orders_list(request):
    orders = request.user.orders.prefetch_related("items__product").order_by("-created_at")

    q = request.GET.get("q", "").strip()
    if q:
        filters = Q(items__product__name__icontains=q)
        if q.isdigit():
            filters |= Q(pk=int(q))
        orders = orders.filter(filters).distinct()

    status = request.GET.get("status", "")
    if status == "paid":
        orders = orders.filter(is_paid=True)
    elif status == "pending":
        orders = orders.filter(is_paid=False)

    sort = request.GET.get("sort", "-created_at")
    if sort not in ("-created_at", "created_at", "-total_price", "total_price"):
        sort = "-created_at"
    orders = orders.order_by(sort)

    page_obj = Paginator(orders, 10).get_page(request.GET.get("page"))
    return render(request, "dashboard/orders.html", {
        "orders": page_obj, "page_obj": page_obj,
        "q": q, "status": status, "sort": sort,
    })


@login_required
def orders_search_ajax(request):
    q = request.GET.get("q", "").strip()
    results = []
    if q:
        filters = Q(items__product__name__icontains=q)
        if q.isdigit():
            filters |= Q(pk=int(q))
        for o in request.user.orders.filter(filters).distinct().order_by("-created_at")[:8]:
            results.append({
                "id": o.pk,
                "date": o.created_at.strftime("%b %d, %Y"),
                "total": f"{o.total_price:,.0f}",
                "is_paid": o.is_paid,
                "url": reverse("dashboard:order_detail", args=[o.pk]),
            })
    return JsonResponse({"results": results})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "dashboard/order_detail.html", {
        "order": order,
    })


@login_required
def payment(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.is_paid:
        return redirect("dashboard:order_detail", pk=order.pk)
    return render(request, "dashboard/payment.html", {
        "order": order,
    })


@login_required
def payment_gateway(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "dashboard/payment_gateway.html", {
        "order": order,
    })


@login_required
def payment_return(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    status = request.GET.get("status", "failed")
    if status == "success":
        order.is_paid = True
        order.save()
    return render(request, "dashboard/payment_return.html", {
        "order": order,
        "success": status == "success",
    })

@login_required
def dashboard_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/tickets.html', {'tickets': tickets})