from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    
    list_display = (
        "user", 
        "phone_number", 
        "address", 
        "created_at", 
        "updated_at", 
        "has_avatar"
    )
    
    
    search_fields = ("user__username", "user__email", "phone_number")
    
    
    readonly_fields = ("user", "created_at", "updated_at")
    
    
    list_filter = ("created_at",)

    # Custom column to show if they have an avatar
    @admin.display(description="Avatar")
    def has_avatar(self, obj):
        return "✅" if obj.avatar else "❌"