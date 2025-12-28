import secrets
import time

from django.conf import settings
from agora_token_builder import RtcTokenBuilder


def build_rtc_token(*, channel_name: str, uid: int | None = None) -> tuple[str, int]:
    """Return (token, uid) for an Agora RTC channel."""
    app_id = getattr(settings, 'AGORA_APP_ID', '')
    app_certificate = getattr(settings, 'AGORA_APP_CERTIFICATE', '')
    expire = int(getattr(settings, 'AGORA_TOKEN_EXPIRE_SECONDS', 3600))

    if not app_id or not app_certificate:
        raise RuntimeError('Agora is not configured. Set AGORA_APP_ID and AGORA_APP_CERTIFICATE.')

    if uid is None:
        # Agora allows uint32; keep it simple
        uid = secrets.randbelow(2_000_000_000) + 1

    privilege_expire_ts = int(time.time()) + expire

    token = RtcTokenBuilder.buildTokenWithUid(
        app_id,
        app_certificate,
        channel_name,
        uid,
        1,  # role: publisher
        privilege_expire_ts,
    )
    return token, uid
