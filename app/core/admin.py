from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (  # modify user page configuration
        (_("Fields"), {"fields": ("email", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    readonly_fields = ["last_login"]
    add_fieldsets = (  # add user page configuration
        (
            None,  # no title
            {
                "classes": ("wide",),  # css configuration
                "fields": ("email", "password1", "password2", "name", "is_active", "is_staff", "is_superuser"),
            }
        ),
    )

admin.site.register(User, UserAdmin)  # UserAdmin is added to overrite default model manager