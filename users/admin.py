from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import RegisterForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = RegisterForm
    list_display = ("email", "name", "surname", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    ordering = ("email",)
    search_fields = ("email", "name", "surname")
    fieldsets = (
        (None, {"fields": ("email", "password")} ),
        (_("Personal info"), {"fields": ("name", "surname", "avatar", "phone", "github_url", "about")} ),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")} ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")} ),
        (_("Favorites"), {"fields": ("favorites",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "surname", "password"),
        }),
    )
    filter_horizontal = ("groups", "user_permissions", "favorites")
