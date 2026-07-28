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
    path("orders/search/", views.orders_search_ajax, name="orders_search_ajax"),
    path("wishlist/search/", views.wishlist_search_ajax, name="wishlist_search_ajax"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("orders/<int:pk>/payment/", views.payment, name="payment"),
    path("orders/<int:pk>/payment/gateway/", views.payment_gateway, name="payment_gateway"),
    path("orders/<int:pk>/payment/return/", views.payment_return, name="payment_return"),
    path("notifications/", views.notifications_list, name="notifications"),
    path("notifications/<int:pk>/read/", views.notification_mark_read, name="notification_mark_read"),
    path("notifications/read-all/", views.notification_mark_all_read, name="notification_mark_all_read"),
    path("notifications/<int:pk>/delete/", views.notification_delete, name="notification_delete"),
    path("notifications/delete-all/", views.notification_delete_all, name="notification_delete_all"),
    path("notifications/unread-count/", views.notification_unread_count, name="notification_unread_count"),
]