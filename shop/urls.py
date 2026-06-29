from django.urls import path
from shop.views import products

app_name = "shop"

urlpatterns = [
    path("", products.index, name="index"),
    path("shop/", products.product_list, name="product_list"),
    path("shop/<int:pk>/", products.product_detail, name="product_detail"),
    path("contact/", products.contact, name="contact"),
]
 
