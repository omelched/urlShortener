import json

from django.views import View
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from urlshortener.forms.urlmap import CreateURLMapRecordForm
from urlshortener.models import URLMapRecord
from urlshortener.utils import apermission_required


@method_decorator(apermission_required('urlshortener.add_urlmaprecord', raise_exception=True), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class CreateURLMapRecordView(View):
    async def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf-8"))
        form = CreateURLMapRecordForm(body)

        if not form.is_valid():
            return HttpResponseBadRequest(form.errors)

        try:
            new_record = await URLMapRecord.objects.acreate(
                target=form.cleaned_data['target']
            )
        except IntegrityError as e:
            return HttpResponseBadRequest(e)

        return JsonResponse(
            {
                'short_url': settings.DOMAIN + '/' + new_record.key
            }
        )
