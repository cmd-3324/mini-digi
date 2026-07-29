from django.contrib import admin
from .models import Profile, Notification


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone",
        "address_line1",
        "address_line2",
        "city",
        "state",
        "zip_code",
        "created_at",
        "has_avatar",
    )
    search_fields = ("user__username", "user__email", "phone", "city", "state")
    readonly_fields = ("user", "created_at", "updated_at")
    list_filter = ("state", "city", "created_at")

    @admin.display(description="Avatar")
    def has_avatar(self, obj):
        return "✅" if obj.avatar else "❌"

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "notification_type",
        "is_read",
        "created_at",
    )
    search_fields = ("title", "message", "user__username")
    list_filter = ("notification_type", "is_read", "created_at")
    readonly_fields = ("created_at",)