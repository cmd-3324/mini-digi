from django.db import models
from .category import Category


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=12, decimal_places=0, help_text="Price in Toman"
    )
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)  # FIX: was missing, caused FieldError
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
 
