from django.db import models
from django.conf import settings
from django.utils.translation import get_language
from .category import Category


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200, blank=True, default="")
    name_ru = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True)
    description_fr = models.TextField(blank=True, default="")
    description_ru = models.TextField(blank=True, default="")
    price = models.DecimalField(
        max_digits=12, decimal_places=0, help_text="Price in Toman"
    )
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=50, blank=True, default="")
    size = models.CharField(max_length=10, blank=True, default="")
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="favorite_products"
    )
    favorites_count = models.PositiveIntegerField(default=0)

    @property
    def translated_name(self):
        lang = get_language()
        if lang == "fr" and self.name_fr:
            return self.name_fr
        if lang == "ru" and self.name_ru:
            return self.name_ru
        return self.name

    @property
    def translated_description(self):
        lang = get_language()
        if lang == "fr" and self.description_fr:
            return self.description_fr
        if lang == "ru" and self.description_ru:
            return self.description_ru
        return self.description

    def __str__(self):
        return self.name
 
