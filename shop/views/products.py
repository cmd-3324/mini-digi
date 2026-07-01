from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from shop.models import Product, Category


def index(request):
    """Home page — featured categories and latest products."""
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by("-created")[:8]
    return render(
        request,
        "shop/index.html",
        {
            "categories": categories,
            "products": products,
        },
    )


def product_list(request):
    """Shop page — filter by category slug and/or search query."""
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by("-created")

    selected_category = request.GET.get("category", "")
    if selected_category:
        products = products.filter(category__slug=selected_category)

    q = request.GET.get("q", "")
    if q:
        products = products.filter(name__icontains=q)

    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "shop/product_list.html",
        {
            "categories": categories,
            "products": page_obj,
            "page_obj": page_obj,
            "selected_category": selected_category,
            "q": q,
        },
    )


def product_detail(request, pk):
    """Product detail page. FIX: was crashing because 'available' field didn't exist."""
    product = get_object_or_404(Product, pk=pk, available=True)
    return render(request, "shop/product_detail.html", {"product": product})


def contact(request):
    return render(request, "shop/contact.html")


def product_search_autocomplete(request):
    q = request.GET.get("q", "").strip()
    if len(q) < 1:
        return JsonResponse({"results": []})

    products = Product.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q),
        available=True,
    ).select_related("category")[:8]

    results = []
    for p in products:
        results.append(
            {
                "id": p.id,
                "name": p.name,
                "price": str(p.price),
                "category": p.category.name if p.category else "",
                "image": p.image.url if p.image else "",
                "url": reverse("shop:product_detail", args=[p.id]),
            }
        )
    return JsonResponse({"results": results})
 
