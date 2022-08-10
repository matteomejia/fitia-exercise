from typing import List, Tuple
from itertools import permutations

from ortools.linear_solver import pywraplp

from apps.core.models import Food
from apps.core.interfaces import Target
from apps.core.utils import generate_meal_dict


def optimize_meal(combo: Tuple[Food], target: Target) -> Tuple[dict, bool]:
    solver = pywraplp.Solver("Find Meal", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    units = [
        solver.IntVar(food.portion_min, food.portion_max, food.name) for food in combo
    ]

    calories = [food.calories for food in combo]
    proteins = [food.protein for food in combo]
    carbohydrates = [food.carbohydrates for food in combo]
    fats = [food.fat for food in combo]

    total_calories = sum(list(unit * cal for unit, cal in zip(units, calories)))
    total_proteins = sum(list(unit * prot for unit, prot in zip(units, proteins)))
    total_carbohydrates = sum(
        list(unit * carb for unit, carb in zip(units, carbohydrates))
    )
    total_fats = sum(list(unit * fat for unit, fat in zip(units, fats)))

    solver.Add(total_calories >= target.calories * 0.8)
    solver.Add(total_calories <= target.calories * 1.1)

    solver.Add(total_proteins >= target.protein * 0.8)
    solver.Add(total_proteins <= target.protein * 1.1)

    solver.Add(total_carbohydrates >= target.carbohydrates * 0.8)
    solver.Add(total_carbohydrates <= target.carbohydrates * 1.1)

    solver.Add(total_fats >= target.fat * 0.8)
    solver.Add(total_fats <= target.fat * 1.1)

    solver.Minimize(total_calories)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        values = [unit.solution_value() for unit in units]
        meal = generate_meal_dict(combo, values)
        return meal, True
    else:
        return {}, False


def find_meal(
    prot_list: List[Food], carb_list: List[Food], fat_list: List[Food], target: Target
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
        meal, res = optimize_meal(combo, target)
        if res:
            return meal, True

    return {}, False
