from django.contrib import admin

from apps.core.models import Food

# Register your models here.


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "calories",
        "protein",
        "carbohydrates",
        "fat",
        "portion_unit",
        "portion_weight",
        "portion_min",
        "portion_max",
    ]
    list_filter = ["macro_type", "breakfast", "lunch", "dinner"]
    ordering = ["external_id"]
