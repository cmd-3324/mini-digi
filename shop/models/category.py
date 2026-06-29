from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to="categories/", blank=True, null=True
    )  # ADD THIS

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
 
