import time
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse


class GlobalRateLimitMiddleware:
    RATE_LIMIT = 25
    WINDOW = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(("/static/", "/media/")):
            return self.get_response(request)

        ip = self._get_client_ip(request)
        cache_key = f"ratelimit:{ip}"
        data = cache.get(cache_key, {"count": 0, "start": time.time()})

        if time.time() - data["start"] > self.WINDOW:
            data = {"count": 0, "start": time.time()}

        data["count"] += 1
        cache.set(cache_key, data, self.WINDOW)

        if data["count"] > self.RATE_LIMIT:
            return JsonResponse(
                {"error": "Rate limit exceeded. Try again later."},
                status=429,
            )

        return self.get_response(request)

    @staticmethod
    def _get_client_ip(request):
        return request.META.get("REMOTE_ADDR")

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Content-Type-Options"] = "nosniff"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        if not settings.DEBUG:
            response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = getattr(settings, "SESSION_COOKIE_AGE", 86400)

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get("last_activity")
            now = time.time()
            if last_activity and (now - last_activity) > self.timeout:
                from django.contrib.auth import logout
                logout(request)
                return redirect(reverse("account_login"))
            request.session["last_activity"] = now
        return self.get_response(request)
