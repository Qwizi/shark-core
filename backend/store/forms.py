from django import forms
from .models import Bonus
from .bonuses import bonus_manager
import sys


class StoreBonusFinalizeForm(forms.Form):
    bonus_id = forms.IntegerField(required=True, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(StoreBonusFinalizeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        initial = kwargs.get('initial', None)
        bonus_id = initial.get('bonus_id', None)
        bonus = Bonus.objects.filter(pk=bonus_id).first()
        bonus_class = bonus_manager.get_bonus(bonus.get_module_tag())
        bonus_instance = bonus_class()

        fields = bonus_instance.get_additional_form_fields()
        print(fields)
        if fields:
            for field in fields:
                field_name = field['name']
                field_type = field['type']
                field_required = field.get('required', None)
                field_widget = field.get('widget', None)
                field_queryset = field.get('queryset', None)
                field_max_length = field.get('max_length', None)
                field_min_length = field.get('min_length', None)

                field_type_class = getattr(forms, field_type)

                options_dict = {}

                if field_widget:
                    options_dict.update({'widget': getattr(forms, field_widget)})
                if field_required:
                    options_dict.update({'required': field_required})
                if field_max_length:
                    options_dict.update({'max_length': field_max_length})
                if field_min_length:
                    options_dict.update({'min_length': field_min_length})
                if field_queryset:
                    options_dict.update({'queryset': field_queryset})

                self.fields[field_name] = field_type_class(**options_dict)
