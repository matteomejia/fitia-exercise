from itertools import permutations
from typing import List, Union, Tuple

from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import QuerySet
from django.views import View

from ortools.linear_solver import pywraplp

from apps.core.choices import MacroTypeChoices
from apps.core.forms import FoodForm
from apps.core.models import Food

# Create your views here.
def get_vals(unit, vals: float) -> float:
    return unit * vals


def optimize(
    combo: Tuple[Food], target_cal, target_prot, target_carb, target_fat
) -> Tuple[dict, bool]:
    total_cal = 0.0
    total_prot = 0.0
    total_carb = 0.0
    total_fat = 0.0

    cal_min = target_cal * 0.8
    cal_max = target_cal * 1.1

    prot_min = target_prot * 0.8
    prot_max = target_prot * 1.1

    carb_min = target_carb * 0.8
    carb_max = target_carb * 1.1

    fat_min = target_fat * 0.8
    fat_max = target_fat * 1.1

    solver = pywraplp.Solver("Find Meal", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    units = [
        solver.IntVar(food.portion_min, food.portion_max, food.name) for food in combo
    ]

    cals = [food.calories for food in combo]
    prots = [food.protein for food in combo]
    carbs = [food.carbohydrates for food in combo]
    fats = [food.fat for food in combo]

    total_cal = sum(list(unit * cal for unit, cal in zip(units, cals)))
    total_prot = sum(list(unit * prot for unit, prot in zip(units, prots)))
    total_carb = sum(list(unit * carb for unit, carb in zip(units, carbs)))
    total_fat = sum(list(unit * fat for unit, fat in zip(units, fats)))

    solver.Add(total_cal >= cal_min)
    solver.Add(total_cal <= cal_max)

    solver.Add(total_prot >= prot_min)
    solver.Add(total_prot <= prot_max)

    solver.Add(total_carb >= carb_min)
    solver.Add(total_carb <= carb_max)

    solver.Add(total_fat >= fat_min)
    solver.Add(total_fat <= fat_max)

    solver.Minimize(total_cal)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        values = [unit.solution_value() for unit in units]
        meal = {
            "total_calories": 0.0,
            "total_proteins": 0.0,
            "total_carbohydrates": 0.0,
            "total_fats": 0.0,
            "items": [],
        }
        for i, _ in enumerate(units):
            value = values[i]

            name = combo[i].name
            calories = combo[i].calories * value
            proteins = combo[i].protein * value
            carbohydrates = combo[i].carbohydrates * value
            fats = combo[i].fat * value

            meal["total_calories"] += calories
            meal["total_proteins"] += proteins
            meal["total_carbohydrates"] += carbohydrates
            meal["total_fats"] += fats
            meal["items"].append(
                {
                    "name": name,
                    "quantity": int(value),
                    "calories": calories,
                    "proteins": proteins,
                    "carbohydrates": carbohydrates,
                    "fats": fats,
                }
            )
        return meal, True
    else:
        return {}, False


def find_meal(
    prot_list: List[Food],
    carb_list: List[Food],
    fat_list: List[Food],
    target_cal: float,
    target_prot: float,
    target_carb: float,
    target_fat: float,
) -> Tuple[dict, bool]:

    prot_permutations = list(permutations(prot_list, 1))
    carb_permutations = list(permutations(carb_list, 1)) + list(
        permutations(carb_list, 2)
    )
    fat_permutations = list(permutations(fat_list, 0)) + list(permutations(fat_list, 1))

    combos: List[Tuple[Food]] = []
    for prot_perm in prot_permutations:
        for carb_perm in carb_permutations:
            for fat_perm in fat_permutations:
                combos.append(prot_perm + carb_perm + fat_perm)

    for combo in combos:
        meal, res = optimize(combo, target_cal, target_prot, target_carb, target_fat)
        if res:
            return meal, True

    return {}, False


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

            foods: Union[QuerySet, List[Food]] = Food.objects.all()

            calories: int = 0
            protein: float = 0.0
            carbohydrates: float = 0.0
            fats: float = 0.0

            if meal == "breakfast":
                foods = foods.filter(breakfast=True)
                calories = self.caloriesBreakfast
                protein = self.macrosBreakfast[0]
                carbohydrates = self.macrosBreakfast[1]
                fats = self.macrosBreakfast[2]

            elif meal == "lunch":
                foods = foods.filter(lunch=True)
                calories = self.caloriesLunch
                protein = self.macrosLunch[0]
                carbohydrates = self.macrosLunch[1]
                fats = self.macrosLunch[2]

            elif meal == "dinner":
                foods = foods.filter(dinner=True)
                calories = self.caloriesDinner
                protein = self.macrosDinner[0]
                carbohydrates = self.macrosDinner[1]
                fats = self.macrosDinner[2]

            prot_list = list(foods.filter(macro_type=MacroTypeChoices.PROT))
            carb_list = list(foods.filter(macro_type=MacroTypeChoices.CARB))
            fat_list = list(foods.filter(macro_type=MacroTypeChoices.FFAT))

            sol, res = find_meal(
                prot_list, carb_list, fat_list, calories, protein, carbohydrates, fats
            )

            return render(
                request, "core/output.html", {"found": res, "meal": sol, "type": meal}
            )
        else:
            return render(request, "core/index.html")
