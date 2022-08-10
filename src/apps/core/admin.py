from django.contrib import admin

from apps.core.models import Food

# Register your models here.


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "calories",
        "portion_unit",
    ]
    list_filter = ["macro_type", "breakfast", "lunch", "dinner"]
    ordering = ["external_id"]
    readonly_fields = ["external_id"]
    search_fields = ["name"]
