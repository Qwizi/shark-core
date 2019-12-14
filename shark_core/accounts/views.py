from django.shortcuts import render, redirect, reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from .forms import SignUpForm
from .models import Account


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
            aid = force_text(urlsafe_base64_encode(aidb64))
            account = Account.objects.get(pk=aid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            account = None

        if account is not None and default_token_generator.check_token(account, token):
            account.activate()
            account.save()

        return render(request, self.template_name)
