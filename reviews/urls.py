from django.urls import path 
from reviews import views

app_name = "reviews"

urlpatterns = [
    path("product/<slug:product_slug>/", views.comment_list, name="comment_list"),
    path("product/<slug:product_slug>/post/", views.comment_create, name="comment_create"),
    path("<int:pk>/edit/", views.comment_update, name="comment_update"),
    path("<int:pk>/delete/", views.comment_delete, name="comment_delete"),
    path("<int:pk>/like/", views.comment_like, name="comment_like"),
    path("<int:pk>/dislike/", views.comment_dislike, name="comment_dislike"),
]



