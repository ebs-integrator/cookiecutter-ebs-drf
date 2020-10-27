def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


CACHE_12H = 60 * 60 * 12
CACHE_24H = 60 * 60 * 24
CACHE_5M = 60 * 5
