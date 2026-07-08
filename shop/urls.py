from django.urls import path
from shop.views import products
from shop.views import newsletter

app_name = "shop"

urlpatterns = [
    path("", products.index, name="index"),
    path("shop/", products.product_list, name="product_list"),
    path("shop/<int:pk>/", products.product_detail, name="product_detail"),
    path("contact/", products.contact, name="contact"),
    path("search/autocomplete/", products.product_search_autocomplete, name="product_search_autocomplete"),
    path("newsletter/subscribe/", newsletter.subscribe, name="newsletter_subscribe"),
    path("about/", products.about, name="about"),
    path("favorite/<int:pk>/", products.toggle_favorite, name="toggle_favorite"),
]
 
