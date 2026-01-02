from __future__ import annotations

try:
    from a_rtchat.models import Notification
except Exception:  # pragma: no cover
    Notification = None


def notifications_badge(request):
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {'NAV_NOTIF_UNREAD': 0}
    if Notification is None:
        return {'NAV_NOTIF_UNREAD': 0}
    try:
        c = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'NAV_NOTIF_UNREAD': int(c or 0)}
    except Exception:
        return {'NAV_NOTIF_UNREAD': 0}
