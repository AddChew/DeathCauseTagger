from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Admin Class for User Model.
    """
    list_display = (
        "username", "date_joined", "is_staff", 
        "is_superuser", "is_active", "last_login",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    ordering = ("-last_login",)
    search_fields = ("username__icontains",)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )
