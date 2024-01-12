from typing import TYPE_CHECKING
import json

from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from urlshortener.forms.create_token import CreateTokenForm
from urlshortener.models.token import Token

if TYPE_CHECKING:
    from django.contrib.auth.models import User


USER_MODEL: 'User' = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class CreateTokenView(View):
    async def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf-8"))
        form = CreateTokenForm(body)

        if not form.is_valid():
            return HttpResponseBadRequest(json.dumps(form.errors, ensure_ascii=False, indent=4))

        try:
            user: 'User' = await USER_MODEL.objects.aget(username=form.cleaned_data['username'])
        except USER_MODEL.DoesNotExist as e:
            return HttpResponseBadRequest(e)

        if not await user.acheck_password(form.cleaned_data['password']):
            return HttpResponseBadRequest('invalid password')

        token = await Token.objects.acreate(user=user, ttl=86400)

        return JsonResponse(
            {
                'token': token.key
            }
        )
