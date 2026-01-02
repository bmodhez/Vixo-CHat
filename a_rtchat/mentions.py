import re
from typing import Iterable

from django.contrib.auth import get_user_model


# Conservative @mention pattern: @username (letters, numbers, underscore, dot, dash)
# Examples: @bhavin, @john_doe, @dev.guy
_MENTION_RE = re.compile(r"(^|\s)@(?P<name>[A-Za-z0-9_.-]{1,32})\b")


def extract_mention_usernames(text: str) -> list[str]:
    if not text:
        return []
    found: list[str] = []
    for m in _MENTION_RE.finditer(text):
        name = (m.group('name') or '').strip()
        if not name:
            continue
        key = name.lower()
        if key not in {x.lower() for x in found}:
            found.append(name)
        if len(found) >= 10:
            break
    return found


def resolve_mentioned_users(usernames: Iterable[str]):
    """Resolve usernames to active users, case-insensitively."""
    User = get_user_model()
    users = []
    seen_ids = set()
    for u in usernames:
        if not u:
            continue
        user = User.objects.filter(is_active=True, username__iexact=u).first()
        if not user:
            continue
        if user.id in seen_ids:
            continue
        seen_ids.add(user.id)
        users.append(user)
        if len(users) >= 10:
            break
    return users
