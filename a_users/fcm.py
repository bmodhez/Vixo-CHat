import base64
import json
from typing import Optional

from django.conf import settings


_firebase_app = None


def _get_credentials_json() -> Optional[dict]:
    raw = (getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_JSON', '') or '').strip()
    b64 = (getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_B64', '') or '').strip()

    if raw:
        try:
            return json.loads(raw)
        except Exception:
            return None

    if b64:
        try:
            decoded = base64.b64decode(b64.encode('utf-8')).decode('utf-8')
            return json.loads(decoded)
        except Exception:
            return None

    return None


def _ensure_firebase_admin():
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app

    if not bool(getattr(settings, 'FIREBASE_ENABLED', False)):
        _firebase_app = False
        return _firebase_app

    creds = _get_credentials_json()
    if not creds:
        _firebase_app = False
        return _firebase_app

    try:
        import firebase_admin
        from firebase_admin import credentials

        if firebase_admin._apps:
            _firebase_app = firebase_admin.get_app()
            return _firebase_app

        cred = credentials.Certificate(creds)
        _firebase_app = firebase_admin.initialize_app(cred)
        return _firebase_app
    except Exception:
        _firebase_app = False
        return _firebase_app


def send_push_to_tokens(tokens: list[str], title: str, body: str, url: str = '/') -> bool:
    """Send an FCM web push notification to a list of tokens (best-effort)."""
    if not tokens:
        return False

    app = _ensure_firebase_admin()
    if not app:
        return False

    try:
        from firebase_admin import messaging

        msg = messaging.MulticastMessage(
            tokens=tokens,
            data={
                'title': title or 'Vixo Connect',
                'body': body or '',
                'url': url or '/',
            },
        )
        resp = messaging.send_multicast(msg)
        return bool(resp and resp.success_count)
    except Exception:
        return False


def send_mention_push(user, from_username: str, chatroom_name: str, preview: str = '') -> None:
    """Send a push notification to `user` for an @mention (best-effort)."""
    if not bool(getattr(settings, 'FIREBASE_ENABLED', False)):
        return

    try:
        from a_users.models import FCMToken

        tokens = list(
            FCMToken.objects.filter(user=user)
            .order_by('-last_seen')
            .values_list('token', flat=True)[:10]
        )
    except Exception:
        return

    if not tokens:
        return

    title = 'You were mentioned'
    body = f"@{from_username}: {preview}".strip()
    url = f"/chat/room/{chatroom_name}"
    send_push_to_tokens(tokens, title=title, body=body[:140], url=url)
