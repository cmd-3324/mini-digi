from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
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
