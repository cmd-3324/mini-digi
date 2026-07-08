from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext as _
from ..models import Newsletter


def subscribe(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": _("Only POST allowed")}, status=405)

    email = request.POST.get("email", "").strip()

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"ok": False, "error": _("Invalid email address")})

    if Newsletter.objects.filter(email=email).exists():
        return JsonResponse({"ok": True, "message": _("You are already subscribed!")})

    Newsletter.objects.create(email=email)

    try:
        send_mail(
            subject=_("Welcome to MiniDigi Newsletter!"),
            message=_("Hi there,\n\nThank you for subscribing to our newsletter!\n\nBest regards,\nMiniDigi Team"),
            from_email=settings.NEWSLETTER_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception:
        pass

    return JsonResponse({"ok": True, "message": _("Your email is subscribed!")})
