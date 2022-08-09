from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.choices import MacroTypeChoices

# Create your models here.

class Food(models.Model):
    external_id = models.IntegerField(_("external id"), unique=True, db_index=True)

    name = models.CharField(_("name"), max_length=255)
    macro_type = models.CharField(
        _("macro type"), max_length=255, choices=MacroTypeChoices.choices
    )

    calories = models.FloatField(_("calories"))
    protein = models.FloatField(_("protein"))
    carbohydrates = models.FloatField(_("carbohydrates"))
    fat = models.FloatField(_("fat"))

    portion_unit = models.CharField(_("portion unit"), max_length=255)
    portion_weight = models.FloatField(_("portion weight"))
    portion_min = models.IntegerField(_("minimum portions"))
    portion_max = models.IntegerField(_("maximum portions"))

    breakfast = models.BooleanField(_("breakfast"), default=True)
    lunch = models.BooleanField(_("lunch"), default=True)
    dinner = models.BooleanField(_("dinner"), default=True)

    class Meta:
        verbose_name = _("food")
        verbose_name_plural = _("foods")

    def __str__(self):
        return self.name
