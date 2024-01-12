import base64
from functools import partial
from typing import TYPE_CHECKING

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

if TYPE_CHECKING:
    from django.contrib.auth.models import User

USER_MODEL: 'User' = get_user_model()


def basic_auth(request, username, password) -> USER_MODEL:
    if not hasattr(request, "_cached_user"):

        try:
            user = USER_MODEL.objects.get(username=username)
        except USER_MODEL.DoesNotExist:
            user = None

        if user:
            if not user.check_password(password):
                user = None

        request._cached_user = user or AnonymousUser()
    return request._cached_user


async def abasic_auth(request, username, password) -> USER_MODEL:
    if not hasattr(request, "_acached_user"):

        try:
            user = await USER_MODEL.objects.aget(username=username)
        except USER_MODEL.DoesNotExist:
            user = None

        if user:
            if not await user.acheck_password(password):
                user = None

        request._acached_user = user or AnonymousUser()
    return request._acached_user


class BasicAuthMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    @staticmethod
    def decode_header(header_value: str) -> tuple[str, str] | None:
        try:
            decoded = base64.b64decode(header_value.split(' ')[1]).decode()
        except (AssertionError, ValueError):
            return None

        splitted = decoded.split(':')

        if not len(splitted) == 2:
            return None

        username, password = splitted

        return username, password

    async def __call__(self, request: HttpRequest):
        user: 'User' = await request.auser()

        if user.is_anonymous:
            header_value = request.headers.get('Authorization')
            if header_value:
                auth_pair = self.decode_header(header_value)
                if auth_pair:
                    request.user = SimpleLazyObject(lambda: basic_auth(request, *auth_pair))
                    request.auser = partial(abasic_auth, request, *auth_pair)

        response = await self.get_response(request)

        return response
