from django.urls import path

from apps.core.views import IndexView

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
