from typing import Tuple, List, Any, Dict

from apps.core.models import Food
from apps.core.interfaces import MealPlan


def get_default_meal_plam() -> MealPlan:
    calories = [500, 600, 600]
    macros = [[25.0, 65.0, 15.0], [35.0, 75.0, 17.0], [35.0, 75.0, 17.0]]

    return MealPlan(calories, macros)


def generate_meal_dict(combo: Tuple[Food], values: List[Any]) -> Dict:
    meal = {
        "total_calories": 0.0,
        "total_proteins": 0.0,
        "total_carbohydrates": 0.0,
        "total_fats": 0.0,
        "items": [],
    }
    for i, val in enumerate(values):
        name = combo[i].name
        calories = combo[i].calories * val
        proteins = combo[i].protein * val
        carbohydrates = combo[i].carbohydrates * val
        fats = combo[i].fat * val

        meal["total_calories"] += calories
        meal["total_proteins"] += proteins
        meal["total_carbohydrates"] += carbohydrates
        meal["total_fats"] += fats
        meal["items"].append(
            {
                "name": name,
                "quantity": val,
                "calories": calories,
                "proteins": proteins,
                "carbohydrates": carbohydrates,
                "fats": fats,
            }
        )
    return meal
