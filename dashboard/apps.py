from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"
    def ready(self):
            from django.conf import settings
            from django.db.models.signals import post_save

            from .models import Profile

            def create_user_profile(sender, instance, created, **kwargs):
                if created:
                    Profile.objects.get_or_create(user=instance)

            post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)