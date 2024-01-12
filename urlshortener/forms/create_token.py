from django import forms


class CreateTokenForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
