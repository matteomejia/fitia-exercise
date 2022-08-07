from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.forms import CustomUserCreationForm, CustomUserChangeForm
from apps.users.models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "first_name", "last_name", "is_active", "date_joined")
    fieldsets = (
        (
            None,
            {
                "fields": ("first_name", "last_name", "email", "password"),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_superuser", "is_staff", "is_active"),
            },
        ),
    )
    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "first_name",
                "last_name",
                "email",
                "password1",
                "password2",
                "is_superuser",
                "is_staff",
                "is_active",
            ),
        },
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ["last_name"]
