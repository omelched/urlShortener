from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import HashIndex

from urlshortener.utils import generate_key


USER_MODEL = get_user_model()


class URLMapRecord(models.Model):
    class Meta:
        verbose_name = _('URL map record')
        verbose_name_plural = _('URL map')
        indexes = (
            HashIndex(fields=('key',)),
            models.Index(fields=('creation_date',)),
        )

    key = models.CharField(
        max_length=6,
        null=False,
        blank=False,
        editable=False,
        default=generate_key,
        unique=True,
    )
    target = models.URLField(
        max_length=2000,
        null=False,
        blank=False,
        editable=True,
        verbose_name=_('target URL')
    )
    creation_date = models.DateTimeField(
        null=False,
        blank=False,
        editable=False,
        auto_now_add=True,
        verbose_name=_('creation date'),
    )
    author = models.ForeignKey(
        USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        editable=False,
    )
