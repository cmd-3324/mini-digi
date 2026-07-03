from django.contrib import admin
from .models import Product, Category, Newsletter


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "name_fr", "name_ru", "price", "available")
    list_editable = ("price", "available")
    prepopulated_fields = {"slug": ("name",)} if hasattr(Product, "slug") else {}
    fieldsets = (
        ("English", {"fields": ("name", "description")}),
        ("Fran\u00e7ais", {"fields": ("name_fr", "description_fr")}),
        ("\u0420\u0443\u0441\u0441\u043a\u0438\u0439", {"fields": ("name_ru", "description_ru")}),
        ("Meta", {"fields": ("category", "price", "stock", "available", "image")}),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "name_fr", "name_ru")
    fieldsets = (
        ("English", {"fields": ("name", "slug")}),
        ("Fran\u00e7ais", {"fields": ("name_fr",)}),
        ("\u0420\u0443\u0441\u0441\u043a\u0438\u0439", {"fields": ("name_ru",)}),
        ("Meta", {"fields": ("image",)}),
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Newsletter)
 
