from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from shop.models import Product, Category

def index(request):
    """Home page — passes all categories and recent products to template."""
    categories = Category.objects.all()
    products = Product.objects.order_by("-created")
    return render(
        request,
        "shop/index.html",
        {
            "categories": categories,
            "products": products,
        },
    )


def product_list(request):
    """Shop page — supports filtering by category slug and search query."""
    categories = Category.objects.all()
    products = Product.objects.order_by("-created")

    # Filter by category slug from sidebar radio buttons (?category=<slug>)
    selected_category = request.GET.get("category", "")
    if selected_category:
        products = products.filter(category__slug=selected_category)

    # Filter by search query (?q=<search term>)
    q = request.GET.get("q", "")
    if q:
        products = products.filter(name__icontains=q)

    # Pagination — 9 products per page
    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "shop/product_list.html",
        {
            "categories": categories,
            "products": page_obj,  # paginated queryset
            "page_obj": page_obj,  # needed by pagination controls in template
            "selected_category": selected_category,
            "q": q,
        },
    )


def product_detail(request, pk):
    """Product detail page."""
    product = get_object_or_404(Product, pk=pk, available=True)
    return render(
        request,
        "shop/product_detail.html",
        {
            "product": product,
        },
    )


def contact(request):
    """Contact page."""
    return render(request, "shop/contact.html")
