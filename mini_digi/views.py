from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit 

@ratelimit(key='ip', rate='10/m', block=True)
def ratelimited_error(request, exception=None):
    return JsonResponse({'error': 'Too many requests'}, status=429)


