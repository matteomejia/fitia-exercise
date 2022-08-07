from django.db import models
from django.utils.translation import gettext_lazy as _


class MacroTypeChoices(models.TextChoices):
    PROT = ("Proteina", _("protein"))
    CARB = ("Carbohidrato", _("carbohydrate"))
    FFAT = ("Grasa", _("fat"))
