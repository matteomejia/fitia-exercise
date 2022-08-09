from typing import List


class MealPlan:
    caloriesBreakfast: int = 500
    caloriesLunch: int = 600
    caloriesDinner: int = 600
    macrosBreakfast: List[float] = [25.0, 65.0, 15.0]
    macrosLunch: List[float] = [35.0, 75.0, 17.0]
    macrosDinner: List[float] = [35.0, 75.0, 17.0]


class Target:
    calories: float
    protein: float
    carbohydrates: float
    fat: float

    def __init__(self, calories: float, macros: List[float]):
        self.calories = calories
        self.protein = macros[0]
        self.carbohydrates = macros[1]
        self.fat = macros[2]
