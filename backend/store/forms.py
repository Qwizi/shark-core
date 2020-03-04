from django import forms
from servers.models import Server


class VipForm(forms.Form):
    servers = forms.ModelChoiceField(queryset=Server.objects.all())
