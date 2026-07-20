import time
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse


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

        try:
            data = cache.get(cache_key, {"count": 0, "start": time.time()})
            if time.time() - data["start"] > self.WINDOW:
                data = {"count": 0, "start": time.time()}
            data["count"] += 1
            cache.set(cache_key, data, self.WINDOW)

            if data["count"] > self.RATE_LIMIT:
                return JsonResponse({"error": "Rate limit exceeded. Try again later."}, status=429)
        except Exception:
            pass  # cache down -> fail open, don't 500 the whole site

        return self.get_response(request)

    @staticmethod
    def _get_client_ip(request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")