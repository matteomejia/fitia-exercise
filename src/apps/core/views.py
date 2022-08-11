from typing import List, Union

from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import QuerySet
from django.views import View

from apps.core.models import Food
from apps.core.forms import FoodForm
from apps.core.choices import MacroTypeChoices
from apps.core.interfaces import Target, MealPlan
from apps.core.services import find_meal
from apps.core.utils import get_default_meal_plam

# Create your views here.


class IndexView(View):
    def get(self, request: HttpRequest):
        return render(request, "core/index.html")

    def post(self, request: HttpRequest):
        """Checks the requested meal, filters the Food queryset,
        calls the find_meal function and sends the result to
        the template."""

        meal_plan: MealPlan = get_default_meal_plam()
        form = FoodForm(request.POST)

        if form.is_valid():
            meal_type = form.cleaned_data.get("food")

            foods: Union[QuerySet, List[Food]] = Food.objects.all()
            target: Target = None

            if meal_type == "breakfast":
                foods = foods.filter(breakfast=True)
                target = Target(meal_plan.caloriesBreakfast, meal_plan.macrosBreakfast)

            elif meal_type == "lunch":
                foods = foods.filter(lunch=True)
                target = Target(meal_plan.caloriesLunch, meal_plan.macrosLunch)

            elif meal_type == "dinner":
                foods = foods.filter(dinner=True)
                target = Target(meal_plan.caloriesDinner, meal_plan.macrosDinner)

            prot_list = list(foods.filter(macro_type=MacroTypeChoices.PROT))
            carb_list = list(foods.filter(macro_type=MacroTypeChoices.CARB))
            fat_list = list(foods.filter(macro_type=MacroTypeChoices.FFAT))

            meal, found = find_meal(prot_list, carb_list, fat_list, target)

            meal_label = dict(form.fields["food"].choices)[meal_type]

            return render(
                request,
                "core/output.html",
                {
                    "found": found,
                    "meal": meal,
                    "type": meal_label,
                },
            )
        else:
            return render(request, "core/index.html")
