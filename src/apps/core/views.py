from typing import Any, Dict

from django.shortcuts import render
from django.http import HttpRequest
from django.views import View

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
            foods = Food.objects.all()
            meal = form.cleaned_data.get("food")

            if meal == "breakfast":
                prots = self.macrosBreakfast[0]
                carbs = self.macrosBreakfast[1]
                fats = self.macrosBreakfast[2]
            elif meal == "lunch":
                prots = self.macrosLunch[0]
                carbs = self.macrosLunch[1]
                fats = self.macrosLunch[2]
            elif meal == "dinner":
                prots = self.macrosDinner[0]
                carbs = self.macrosDinner[1]
                fats = self.macrosDinner[2]

            context = {}
            return render(request, "core/output.html", context)
        else:
            return render(request, "core/index.html")
