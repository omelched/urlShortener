from typing import TYPE_CHECKING
import binascii
import os
from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

if TYPE_CHECKING:
    from django.contrib.auth.models import User

_USER_MODEL: 'User' = get_user_model()


class Token(models.Model):
    """
    DRF-like token with TTL and M2M owners.
    """

    class Meta:
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')

    key = models.CharField(_("Key"), max_length=40, primary_key=True)

    user = models.ForeignKey(
        _USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='session_tokens',
        verbose_name=_('user'),
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    ttl = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('token TTL (in seconds)'),
    )

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    @property
    def expired(self):

        if not self.ttl:
            return False

        return self.created < (timezone.now() - timedelta(seconds=self.ttl))

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)
