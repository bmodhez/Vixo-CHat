from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    """Authenticate against either `username` or `email`.

    This is intentionally simple and exists to support logging in via email even
    when an allauth `EmailAddress` row is missing (e.g. users created via admin
    or legacy data).
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        login = (username or kwargs.get("login") or "").strip()
        if not login or password is None:
            return None

        User = get_user_model()

        try:
            user = (
                User._default_manager.filter(Q(username__iexact=login) | Q(email__iexact=login))
                .order_by("id")
                .first()
            )
        except Exception:
            return None

        if not user:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
