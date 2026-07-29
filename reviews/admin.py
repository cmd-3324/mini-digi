from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "is_review", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("body", "user__username", "product__name")
    readonly_fields = ("created_at", "updated_at") 
