from django.views import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from urlshortener.models import URLMapRecord


class URLRedirectView(View):

    @staticmethod
    async def get_redirect_url(*args, **kwargs):
        key = kwargs.get('key')
        try:
            urlmap_record: URLMapRecord = await URLMapRecord.objects.aget(key=key)
        except URLMapRecord.DoesNotExist:
            return None

        return urlmap_record.target

    async def get(self, request, *args, **kwargs):
        url = await self.get_redirect_url(*args, **kwargs)

        if not url:
            return TemplateResponse(request, 'urlshortener/not-found.html')

        return HttpResponseRedirect(url)
