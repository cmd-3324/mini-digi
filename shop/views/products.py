from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from shop.models import Product, Category , ProductVariant
from django.http import HttpResponseRedirect
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
            # Check if ANY variant's price OR the base product price falls in the range
            products = products.filter(
                Q(variants__price_override__gte=min_p, variants__price_override__lte=max_p) |
                Q(price__gte=min_p, price__lte=max_p)
            ).distinct()
        except (ValueError, TypeError):
            pass

    color_list = request.GET.getlist("color")
    if color_list:
        products = products.filter(variants__color__in=color_list, 
        variants__is_active=True
        ).distinct()

    size_list = request.GET.getlist("size")
    if size_list:
        products = products.filter(
        variants__size__in=size_list, 
        variants__is_active=True
        ).distinct()

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
        ProductVariant.objects.filter(
            product__available=True,
            is_active=True
        )
        .exclude(color="")
        .values_list("color", flat=True)
        .distinct()
        .order_by("color")
    )
    available_sizes = (
        ProductVariant.objects.filter(
            product__available=True,
            is_active=True
        )
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

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = product.variants.filter(is_active=True)
    gallery = variants.exclude(image="")
    return render(request, "shop/product_detail.html", {
        "product": product,
        "variants": variants,
        "gallery": gallery,
    })

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
                "url": reverse("shop:product_detail", args=[p.slug]),
            }
        )
    return JsonResponse({"results": results})
def FAQs(request):
    return render(request,"components/FAQs.html")
def about(request):
    return render(request, "shop/about.html")
def help(request):
    return render(request, "components/helps.html")

def toggle_favorite(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if not request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "login_required": True}, status=401)
        return redirect("account_login")
    is_favorited = request.user in product.favorited_by.all()
    if is_favorited:
        product.favorited_by.remove(request.user)
        product.favorites_count = max(product.favorites_count - 1, 0)
    else:
        product.favorited_by.add(request.user)
        product.favorites_count += 1
    product.save(update_fields=["favorites_count"])
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "is_favorited": not is_favorited,
            "favorites_count": product.favorites_count,
            "user_favorite_count": Product.objects.filter(favorited_by=request.user).count(),
        })
    return redirect(request.GET.get("next", "shop:product_list"))



def set_currency(request):
    code = request.GET.get("currency", "USD")
    if code in ("USD", "EUR", "GBP", "CAD"):
        request.session["currency"] = code
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))