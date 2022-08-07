from django import forms
from django.utils.translation import gettext_lazy as _

FOOD_CHOICES = [
    ("breakfast", _("Breakfast")),
    ("lunch", _("Lunch")),
    ("dinner", _("Dinner")),
]


class FoodForm(forms.Form):
    food = forms.ChoiceField(choices=FOOD_CHOICES)
