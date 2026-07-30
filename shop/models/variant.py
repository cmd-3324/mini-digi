from django.db import models

class ProductVariant(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='variants'
    )
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)   
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, default="")
    color = models.CharField(max_length=50, blank=True, default="")
    
    
    stock = models.PositiveIntegerField(default=0)
    price_override = models.DecimalField(
        max_digits=12, decimal_places=0, blank=True, null=True,
        help_text="Leave blank to use the main product's price"
    )
    
    
    image = models.ImageField(upload_to="products/variants/", blank=True, null=True)
    
    def save(self, *args, **kwargs):
            if self.is_default:
                ProductVariant.objects.filter(
                    product=self.product, is_default=True
                ).exclude(pk=self.pk).update(is_default=False)
            super().save(*args, **kwargs)
            
    def __str__(self):
        # Example: "T-Shirt - Blue / Large"
        attrs = []
        if self.color: attrs.append(self.color)
        if self.size: attrs.append(self.size)
        attr_string = " / ".join(attrs) if attrs else "Default"
        return f"{self.product.name} - {attr_string}"

    @property
    def final_price(self):
        # If a specific price is set for this variant, use it. Otherwise, use the main product price.
        return self.price_override if self.price_override is not None else self.product.price

    @property
    def is_in_stock(self):
        return self.stock > 0