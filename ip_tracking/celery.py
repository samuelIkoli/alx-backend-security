app.conf.beat_schedule = {
    'detect-suspicious-ips-hourly': {
        'task': 'ip_tracking.tasks.detect_suspicious_ips',
        'schedule': crontab(minute=0),  # Every hour on the hour
    },
}