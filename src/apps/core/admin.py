from django.contrib import admin

from apps.core.models import Food

# Register your models here.


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ["name", "external_id", "macro_type", "breakfast", "lunch", "dinner"]
    ordering = ["external_id"]
