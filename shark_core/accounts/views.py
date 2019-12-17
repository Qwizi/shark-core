from django.shortcuts import render, redirect, reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
    logout
)

from .forms import (
    SignUpForm,
    SignInForm
)

Account = get_user_model()


class AccountSingUpView(View):
    form_class = SignUpForm
    template_name = 'accounts/sign-up.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/account/')

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:sign-up'))

        return render(request, self.template_name, {'form': form})


class AccountActivateView(View):
    template_name = 'accounts/activate.html'

    def get(self, request, aidb64=None, token=None):

        try:
            aid = force_text(urlsafe_base64_decode(aidb64))
            account = Account.objects.get(pk=aid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            account = None

        if account is not None and default_token_generator.check_token(account, token):
            print(account)
            account.activate()
            account.save()

        return render(request, self.template_name)


class AccountLogInView(View):
    form_class = SignInForm
    template_name = 'accounts/sign-in.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/account/')

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            account = authenticate(request, username=username, password=password)
            print(account)
            if account is not None:
                login(request, account)
                return redirect('http://localhost:8000/')
            else:
                return redirect(reverse('accounts:sign-in'))

        return render(request, self.template_name, {'form': form})


class AccountSignOutView(View):

    def get(self, request):
        logout(request)
        return redirect('/account/')
