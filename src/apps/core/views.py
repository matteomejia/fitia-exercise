from typing import Any, Dict

from django.shortcuts import render
from django.views.generic import TemplateView

from apps.core.models import Food

# Create your views here.


class IndexView(TemplateView):
    template_name: str = "core/index.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["foods"] = Food.objects.all()
        return context
