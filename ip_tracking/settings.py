MIDDLEWARE = [
    # ... other middleware
    'ip_tracking.middleware.IPTrackingMiddleware',
    'ip_tracking.middleware.IPBlockMiddleware',
]


# settings.py

# Optional: configure default key for rate limiting
RATELIMIT_USE_CACHE = 'default'  # Uses default Django cache


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

GEOIP_PATH = BASE_DIR / "geoip"