from __future__ import annotations

import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_core.settings')

app = Celery('a_core')

# Reads CELERY_* settings from Django settings, e.g. CELERY_BROKER_URL
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks.py in installed apps
app.autodiscover_tasks()
