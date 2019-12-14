from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .models import Account

from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        account_instance = super().save(commit=False)
        account_instance.is_active = False
        account_instance.set_password(self.cleaned_data["password1"])
        if commit:
            account_instance.save()

            context = {
                'from_email': '500adrian2@gmail.com',
                'username': self.cleaned_data.get('username'),
                'aid': urlsafe_base64_encode(force_bytes(account_instance.pk)),
                'token': default_token_generator.make_token(account_instance),
            }

            subject = render_to_string('accounts/activation_subject.txt', context)
            email = render_to_string('accounts/activation_message.txt', context)
            account_instance.email_user(subject, email)

        return account_instance
