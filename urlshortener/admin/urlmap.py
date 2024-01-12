from urlshortener.models import URLMapRecord
from django.contrib import admin


@admin.register(URLMapRecord)
class URLMapRecordAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "target",
        "creation_date",
        "author",
    )
    list_display_links = None
