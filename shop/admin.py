from django.contrib import admin
from .models import Product, Category, ProductImage, Newsletter

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    
    fieldsets = (
        ("Category Info", {"fields": ("name", "slug", "image")}),
    )
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_primary')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "available")
    list_editable = ("price", "available")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created",)
    
    fieldsets = (
        ("English", {"fields": ("name", "description")}),
        ("Details", {"fields": ("category", "price", "stock", "available", "image")}),
        ("Attributes", {"fields": ("color", "size")}),
        ("SEO", {"fields": ("slug", "meta_title", "meta_description")}),
        ("System", {"fields": ("favorited_by", "favorites_count")}),
    )