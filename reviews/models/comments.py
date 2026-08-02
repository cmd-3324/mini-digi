from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from shop.models import Product,ProductVariant


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    rate = models.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
        )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        blank=True, 
        related_name="liked_comments"
    )
    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        blank=True, 
        related_name="disliked_comments"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} on {self.product} ({'review' if self.rate else 'comment'})"

    @property
    def is_review(self):
        return self.parent_id is None and self.rate is not None

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def dislike_count(self):
        return self.dislikes.count()

    @property
    def rating_score(self):
        return self.rate or 0