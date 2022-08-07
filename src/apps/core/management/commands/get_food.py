from typing import Optional

import requests

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.core.models import Food


class Command(BaseCommand):
    help: str = _("Fetches and parses the food data from the API.")

    def handle(self, *args, **options) -> Optional[str]:
        # Remove all items
        Food.objects.all().delete()

        # fetch list of items
        r = requests.get(url=settings.FOOD_API_URL)

        if r.status_code != 200:
            raise CommandError(_("Could not fetch foods from API."))

        foods = r.json()

        for food in foods:
            Food.objects.create(
                external_id=food["id"],
                name=food["nombre"],
                macro_type=food["tipoMacro"],
                calories=float(food["cal"]),
                protein=float(food["prot"]),
                carbohydrates=float(food["carb"]),
                fat=float(food["fat"]),
                portion_unit=food["unidadPorcion"],
                portion_weight=float(food["porcionPeso"]),
                portion_min=food["porcionMin"],
                portion_max=food["porcionMax"],
                breakfast=food["desayuno"],
                lunch=food["almuerzo"],
                dinner=food["cena"],
            )
