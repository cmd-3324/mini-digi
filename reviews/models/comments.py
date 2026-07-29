from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from shop.models import Product


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    rating = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
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
        return f"{self.user} on {self.product} ({'review' if self.rating else 'comment'})"

    @property
    def is_review(self):
        return self.parent_id is None and self.rating is not None

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def dislike_count(self):
        return self.dislikes.count()

    @property
    def rating_score(self):
        return self.rating or 0