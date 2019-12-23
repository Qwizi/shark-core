from django.shortcuts import render
from django.views import View


class MainPageIndex(View):
    template_name = 'mainpage/index.html'

    def get(self, request):
        return render(request, self.template_name)