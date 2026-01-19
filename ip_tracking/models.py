from django.db import models

from django.utils import timezone
from django.core.cache import cache
from django_ipgeolocation.geolocation import get_geolocation
from .models import RequestLog


class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        location = f"{self.city}, {self.country}" if self.city or self.country else "Unknown location"
        return f"{self.ip_address} - {self.path} at {self.timestamp} ({location})"


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address
    

class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField()
    flagged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"


