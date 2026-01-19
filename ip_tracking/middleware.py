from .models import RequestLog

from django.http import HttpResponseForbidden
from .models import BlockedIP

import os
from django.core.cache import cache
from django.contrib.gis.geoip2 import GeoIP2
from .models import RequestLog

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geo = None
        # Initialize GeoIP2 if the GEOIP_PATH setting exists
        try:
            self.geo = GeoIP2()
        except Exception:
            self.geo = None

    def __call__(self, request):
        ip = self.get_client_ip(request)
        country, city = self.lookup_geo(ip)

        # Create log entry
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            country=country,
            city=city
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def lookup_geo(self, ip):
        if not self.geo:
            return None, None

        cache_key = f"geo_{ip}"
        cached = cache.get(cache_key)
        if cached:
            return cached["country"], cached["city"]

        try:
            data = self.geo.city(ip)
            country = data.get("country_name")
            city = data.get("city")
        except Exception:
            country = None
            city = None

        # Cache for 24h
        cache.set(cache_key, {"country": country, "city": city}, 86400)
        return country, city



class IPBlockMiddleware:
    """
    Middleware to block requests from blacklisted IPs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied: Your IP is blocked.")
        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Retrieves the client's IP address from the request headers.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
