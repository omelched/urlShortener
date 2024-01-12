import base64
from functools import partial
from typing import TYPE_CHECKING

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

from urlshortener.models import Token

if TYPE_CHECKING:
    from django.contrib.auth.models import User

USER_MODEL: 'User' = get_user_model()


def bearer_auth(request, token) -> USER_MODEL:
    if not hasattr(request, "_cached_user_bearer"):

        try:
            token = Token.objects.get(key=token)
            user = token.user
        except Token.DoesNotExist:
            user = None

        request._cached_user_bearer = user or AnonymousUser()

    return request._cached_user_bearer


async def abearer_auth(request, token) -> USER_MODEL:
    if not hasattr(request, "_acached_user_bearer"):

        try:
            token = await Token.objects.prefetch_related('user').aget(key=token)
            user = token.user
        except Token.DoesNotExist:
            user = None

        request._acached_user_bearer = user or AnonymousUser()

    return request._acached_user_bearer


class BearerAuthMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request: HttpRequest):
        user: 'User' = await request.auser()

        if user.is_anonymous:
            header_value = request.headers.get('Authorization')
            if header_value:
                token = header_value.split(' ')[1]
                if token:
                    request.user = SimpleLazyObject(lambda: bearer_auth(request, token))
                    request.auser = partial(abearer_auth, request, token)

        response = await self.get_response(request)

        return response
