from django.db import models
from django.conf import settings
from django.utils.translation import get_language
from .category import Category
from django.utils.text import slugify

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=220, blank=True, default="", unique=True)
    meta_title = models.CharField(max_length=70, blank=True, default="")
    meta_description = models.CharField(max_length=160, blank=True, default="")
    price = models.DecimalField(
        max_digits=12, decimal_places=0, help_text="Price in Toman"
    )
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    
    created = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=50, blank=True, default="")
    size = models.CharField(max_length=10, blank=True, default="")
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="favorite_products"
    )
    favorites_count = models.PositiveIntegerField(default=0)
    tasting_notes = models.TextField(blank=True, default="")
    food_pairing = models.TextField(blank=True, default="")

    @property
    def display_image(self):
        variant = self.variants.filter(is_active=True, is_default=True).exclude(image="").first()
        if not variant:
            variant = self.variants.filter(is_active=True).exclude(image="").first()
        return variant.image if variant else None
    @property
    def translated_name(self):
        # Since you use .po files, we just return the name.
        # If you want Django to check the .po file for a translation of this exact string:
        from django.utils.translation import gettext as _
        return _(self.name)

    @property
    def translated_description(self):
        from django.utils.translation import gettext as _
        return _(self.description)
    @property
    def translated_tasting_notes(self):
        from django.utils.translation import gettext as _
        return _(self.tasting_notes)

    @property
    def translated_food_pairing(self):
        from django.utils.translation import gettext as _
        return _(self.food_pairing)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
 
