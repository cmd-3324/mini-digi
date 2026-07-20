from django.db import models
from .product import Product 

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=200, blank=True, default="")
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["order"]