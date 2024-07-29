from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["username"]
    fieldsets = (  # modify user page configuration
        ("Fields", {"fields": ("username", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    readonly_fields = ["last_login"]
    add_fieldsets = (  # add user page configuration
        (
            None,  # no title
            {
                "classes": ("wide",),  # css configuration
                "fields": ("username", "password1", "password2", "is_active", "is_staff", "is_superuser"),
            }
        ),
    )

admin.site.register(User, UserAdmin)  # UserAdmin is added to overrite default model manager
