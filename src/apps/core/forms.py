from django import forms
from django.utils.translation import gettext_lazy as _

FOOD_CHOICES = [
    ("breakfast", _("breakfast")),
    ("lunch", _("lunch")),
    ("dinner", _("dinner")),
]


class FoodForm(forms.Form):
    food = forms.ChoiceField(choices=FOOD_CHOICES)
