from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.profile_update, name="profile_update"),
    path("profile/password/", views.change_password, name="change_password"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("orders/", views.orders_list, name="orders"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("orders/<int:pk>/payment/", views.payment, name="payment"),
    path("orders/<int:pk>/payment/gateway/", views.payment_gateway, name="payment_gateway"),
    path("orders/<int:pk>/payment/return/", views.payment_return, name="payment_return"),
]