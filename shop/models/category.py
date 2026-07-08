from django.db import models
from django.utils.translation import get_language


class Category(models.Model):
    name = models.CharField(max_length=100)
    name_fr = models.CharField(max_length=100, blank=True, default="")
    name_ru = models.CharField(max_length=100, blank=True, default="")
    name_es = models.CharField(max_length=100, blank=True, default="")
    name_de = models.CharField(max_length=100, blank=True, default="")
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    @property
    def translated_name(self):
        lang = get_language()
        if lang == "fr" and self.name_fr:
            return self.name_fr
        if lang == "ru" and self.name_ru:
            return self.name_ru
        if lang == "es" and self.name_es:
            return self.name_es
        if lang == "de" and self.name_de:
            return self.name_de
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
 
