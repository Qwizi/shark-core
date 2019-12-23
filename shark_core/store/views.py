from django.shortcuts import render, reverse, redirect
from django.views import View
from .mixins import MyLoginRequiredMixin
from django.core import serializers
import json

from .models import Bonus, Category, Log as LogModel
from .forms import StoreBonusFinalizeForm
from .bonuses import bonus_manager


class StoreBonusesView(MyLoginRequiredMixin, View):
    template_name = 'store/index.html'

    def get(self, request):
        return render(request, self.template_name)


class StoreBonusDetailView(MyLoginRequiredMixin, View):
    form_class = StoreBonusFinalizeForm
    template_name = 'store/detail.html'

    def post(self, request, bonus_id):
        form = self.form_class(request.POST, initial={'bonus_id': bonus_id}, )

        if form.is_valid():
            if bonus_id == form.cleaned_data.get('bonus_id'):
                bonus = Bonus.objects.get(pk=form.cleaned_data['bonus_id'])
                account = request.user

                bonus_class = bonus_manager.get_bonus(bonus.get_module_tag())
                bonus_log_instance = LogModel(
                    bonus=bonus,
                    account=account
                )
                bonus_instance = bonus_class()
                bonus_instance.set_account(account)
                bonus_instance.set_bonus(bonus)
                bonus_instance.set_log(bonus_log_instance)

                print(bonus_instance)
                status = bonus_instance.add_bonus()

                if status is False:
                    return redirect('error/')

                return redirect(reverse('store:index'))
            return redirect('store/error/')
        else:
            return redirect('store/error/')

    def get(self, request, bonus_id):
        bonus = Bonus.objects.get(pk=bonus_id)
        desc_list = bonus.get_split_description()
        form_dict = {}

        form_dict.update({'initial': {'bonus_id': bonus_id}})

        form = self.form_class(**form_dict)

        return render(request, self.template_name, {
            'account': request.user,
            'bonus': bonus,
            'desc_list': desc_list,
            'form': form
        })