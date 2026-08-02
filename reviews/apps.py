from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    name = 'reviews'
 
    def ready(self):
        from django.db.models import Avg
        from django.db.models.signals import post_save, post_delete
        from reviews.models import Comment

        def sync_variant_ratings(sender, instance, **kwargs):
            if instance.parent_id is not None:
                return
            avg = Comment.objects.filter(product=instance.product, parent__isnull=True).aggregate(avg=Avg("rate"))["avg"] or 0
            instance.product.variants.update(rate=round(avg, 1))

        post_save.connect(sync_variant_ratings, sender=Comment)
        post_delete.connect(sync_variant_ratings, sender=Comment)