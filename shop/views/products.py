from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from shop.models import Product, Category

def index(request):
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
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    selected_category = request.GET.get("category", "")
    if selected_category:
        products = products.filter(category__slug=selected_category)

    q = request.GET.get("q", "").strip()
    if q:
        products = products.filter(name__icontains=q)

    price = request.GET.get("price", "")
    if price and "-" in price:
        try:
            min_p, max_p = price.split("-")
            products = products.filter(price__gte=min_p, price__lte=max_p)
        except (ValueError, TypeError):
            pass

    color_list = request.GET.getlist("color")
    if color_list:
        products = products.filter(color__in=color_list)

    size_list = request.GET.getlist("size")
    if size_list:
        products = products.filter(size__in=size_list)

    sort = request.GET.get("sort", "latest")
    if sort == "popular":
        products = products.order_by("-favorites_count", "-created")
    elif sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    else:
        products = products.order_by("-created")

    per_page = request.GET.get("per_page", "9")
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 9

    paginator = Paginator(products, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    available_colors = (
        Product.objects.filter(available=True)
        .exclude(color="")
        .values_list("color", flat=True)
        .distinct()
        .order_by("color")
    )
    available_sizes = (
        Product.objects.filter(available=True)
        .exclude(size="")
        .values_list("size", flat=True)
        .distinct()
        .order_by("size")
    )

    return render(
        request,
        "shop/product_list.html",
        {
            "categories": categories,
            "products": page_obj,
            "page_obj": page_obj,
            "selected_category": selected_category,
            "q": q,
            "current_price": price,
            "current_colors": color_list,
            "current_sizes": size_list,
            "current_sort": sort,
            "current_per_page": str(per_page),
            "available_colors": available_colors,
            "available_sizes": available_sizes,
        },
    )

def product_detail(request, pk):
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
 
def about(request):
    return render(request, "shop/about.html")

def toggle_favorite(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not request.user.is_authenticated:
        return redirect("account_login")
    if request.user in product.favorited_by.all():
        product.favorited_by.remove(request.user)
        product.favorites_count = max(product.favorites_count - 1, 0)
    else:
        product.favorited_by.add(request.user)
        product.favorites_count += 1
    product.save(update_fields=["favorites_count"])
    return redirect(request.GET.get("next", "shop:product_list"))