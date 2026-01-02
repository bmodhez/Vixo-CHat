from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth import get_user_model


@dataclass(frozen=True)
class NotifyTarget:
    user_id: int
    online_in_chats: bool


def _is_user_online_in_any_chat(user) -> bool:
    """Best-effort online check.

    Uses ChatGroup.users_online M2M which is updated by websocket connects.
    """
    try:
        # Avoid circular import at module load.
        from a_rtchat.models import ChatGroup

        return ChatGroup.objects.filter(users_online=user).exists()
    except Exception:
        return False


def _is_user_online_in_chat(*, user, chatroom_name: str) -> bool:
    """Best-effort check if a user is online in a specific chatroom."""
    try:
        if not chatroom_name:
            return False
        from a_rtchat.models import ChatGroup

        return ChatGroup.objects.filter(group_name=chatroom_name, users_online=user).exists()
    except Exception:
        return False


def should_persist_notification(*, user_id: int, chatroom_name: str | None = None) -> bool:
    """Persist in-app notification if user won't see it live.

    - If chatroom_name is provided: persist only if user is NOT online in that chat.
    - Otherwise: persist only if user is offline (not in any chat WS).
    """
    User = get_user_model()
    user = User.objects.filter(id=user_id, is_active=True).first()
    if not user:
        return False
    if chatroom_name:
        return not _is_user_online_in_chat(user=user, chatroom_name=chatroom_name)
    return not _is_user_online_in_any_chat(user)
