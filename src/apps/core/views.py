from typing import Any, Dict

from django.shortcuts import render
from django.http import HttpRequest
from django.views import View

from apps.core.choices import MacroTypeChoices
from apps.core.forms import FoodForm
from apps.core.models import Food

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
            meal = form.cleaned_data.get("food")

            foods = Food.objects.all()

            target_calories: int = 0
            target_prots: float = 0.0
            target_carbs: float = 0.0
            target_fats: float = 0.0

            if meal == "breakfast":
                foods = foods.filter(breakfast=True)
                target_calories = self.caloriesBreakfast
                target_prots = self.macrosBreakfast[0]
                target_carbs = self.macrosBreakfast[1]
                target_fats = self.macrosBreakfast[2]

            elif meal == "lunch":
                foods = foods.filter(lunch=True)
                target_calories = self.caloriesLunch
                target_prots = self.macrosLunch[0]
                target_carbs = self.macrosLunch[1]
                target_fats = self.macrosLunch[2]

            elif meal == "dinner":
                foods = foods.filter(dinner=True)
                target_calories = self.caloriesDinner
                target_prots = self.macrosDinner[0]
                target_carbs = self.macrosDinner[1]
                target_fats = self.macrosDinner[2]

            foods_protein = foods.filter(macro_type=MacroTypeChoices.PROT)
            foods_carb = foods.filter(macro_type=MacroTypeChoices.CARB)
            foods_fat = foods.filter(macro_type=MacroTypeChoices.FFAT)

            target_calories_min = target_calories * 0.8
            target_calories_min = target_calories * 1.1

            target_prots_min = target_prots * 0.8
            target_prots_max = target_prots * 1.1

            target_carbs_min = target_carbs * 0.8
            target_carbs_max = target_carbs * 1.1

            target_fats_min = target_fats * 0.8
            target_fats_max = target_fats * 1.1

            return render(request, "core/output.html")
        else:
            return render(request, "core/index.html")
