from django.contrib import admin
from django.utils import timezone

from base.admin import BaseAdmin
from codes.models import Code


@admin.register(Code)
class CodeAdmin(BaseAdmin):
    """
    Admin Class for Code Model.
    """
    list_display = (
        "description", 
        "category",
        "created_by", "created_on", 
        "updated_by", "updated_on", 
        "is_active", "is_active_updated_by", "is_active_updated_on",
    )
    list_filter = ("is_active", "category")
    ordering = ("description", "category")
    actions = ("mark_active", "mark_inactive")

    @admin.action(description = "Mark selected Codes as active")
    def mark_active(self, request, queryset):
        """
        Mark selected codes as active.
        """
        super().mark_active(request, queryset)

    @admin.action(description = "Mark selected Codes as inactive")
    def mark_inactive(self, request, queryset):
        """
        Mark selected codes as inactive.
        """
        super().mark_inactive(request, queryset)
