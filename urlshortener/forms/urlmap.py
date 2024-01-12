from django import forms
from urlshortener.models import URLMapRecord


class CreateURLMapRecordForm(forms.ModelForm):
    class Meta:
        model = URLMapRecord
        fields = (
            'target',
        )
