from __future__ import annotations

from django.conf import settings
from django.db import models


class ChatReadState(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_read_states')
    group = models.ForeignKey('a_rtchat.ChatGroup', on_delete=models.CASCADE, related_name='read_states')
    last_read_message_id = models.PositiveBigIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'group'], name='unique_read_state'),
        ]
        indexes = [
            models.Index(fields=['group', 'user'], name='readstate_group_user_idx'),
        ]

    def __str__(self):
        return f"ReadState(u={self.user_id}, g={self.group_id}, last={self.last_read_message_id})"
