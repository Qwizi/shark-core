from django.contrib.auth.mixins import LoginRequiredMixin


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/account/sign-in/'
