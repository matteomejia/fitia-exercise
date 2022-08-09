from typing import List, Union

from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import QuerySet
from django.views import View

from apps.core.choices import MacroTypeChoices
from apps.core.forms import FoodForm
from apps.core.models import Food
from apps.core.interfaces import Target
from apps.core.services import find_meal

# Create your views here.


class IndexView(View):
    caloriesBreakfast = 500
    caloriesLunch = 600
    caloriesDinner = 600
    macrosBreakfast = [25.0, 65.0, 15.0]
    macrosLunch = [35.0, 75.0, 17.0]
    macrosDinner = [35.0, 75.0, 17.0]

    def get(self, request: HttpRequest):
        return render(request, "core/index.html")

    def post(self, request: HttpRequest):
        form = FoodForm(request.POST)
        if form.is_valid():
            meal_type = form.cleaned_data.get("food")

            foods: Union[QuerySet, List[Food]] = Food.objects.all()
            target = None

            if meal_type == "breakfast":
                foods = foods.filter(breakfast=True)
                target = Target(self.caloriesBreakfast, self.macrosBreakfast)

            elif meal_type == "lunch":
                foods = foods.filter(lunch=True)
                target = Target(self.caloriesLunch, self.macrosLunch)

            elif meal_type == "dinner":
                foods = foods.filter(dinner=True)
                target = Target(self.caloriesDinner, self.macrosDinner)

            prot_list = list(foods.filter(macro_type=MacroTypeChoices.PROT))
            carb_list = list(foods.filter(macro_type=MacroTypeChoices.CARB))
            fat_list = list(foods.filter(macro_type=MacroTypeChoices.FFAT))

            meal, found = find_meal(prot_list, carb_list, fat_list, target)

            return render(
                request,
                "core/output.html",
                {"found": found, "meal": meal, "type": meal_type},
            )
        else:
            return render(request, "core/index.html")
