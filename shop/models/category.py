from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext as _

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    @property
    def translated_name(self):
        return _(self.name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
 
