import json

from django.conf import settings


def firebase_config(request):
    """Expose Firebase public config to templates when enabled."""
    enabled = bool(getattr(settings, 'FIREBASE_ENABLED', False))
    cfg = {
        'apiKey': getattr(settings, 'FIREBASE_API_KEY', ''),
        'authDomain': getattr(settings, 'FIREBASE_AUTH_DOMAIN', ''),
        'projectId': getattr(settings, 'FIREBASE_PROJECT_ID', ''),
        'storageBucket': getattr(settings, 'FIREBASE_STORAGE_BUCKET', ''),
        'messagingSenderId': getattr(settings, 'FIREBASE_MESSAGING_SENDER_ID', ''),
        'appId': getattr(settings, 'FIREBASE_APP_ID', ''),
        'measurementId': getattr(settings, 'FIREBASE_MEASUREMENT_ID', ''),
    }

    # Only expose when all required public fields are present.
    required = ['apiKey', 'authDomain', 'projectId', 'messagingSenderId', 'appId']
    ready = enabled and all((cfg.get(k) or '').strip() for k in required)

    return {
        'FIREBASE_ENABLED': bool(ready),
        'FIREBASE_CONFIG_JSON': json.dumps(cfg if ready else {}),
        'FIREBASE_VAPID_PUBLIC_KEY': getattr(settings, 'FIREBASE_VAPID_PUBLIC_KEY', '') if ready else '',
    }
