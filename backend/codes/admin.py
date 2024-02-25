from django.contrib import admin
from django.utils import timezone

from base.admin import BaseAdmin
from codes.models import Code


@admin.register(Code)
class CodeAdmin(BaseAdmin):
    """
    Admin Class for Code Model.
    """
    actions = ["mark_active", "mark_inactive"]

    @admin.action(description = "Mark selected Codes as active")
    def mark_active(self, request, queryset):
        """
        Mark selected codes as active.
        """
        self.action(
            request, queryset, action = "active", 
            update_fields = {
                "is_active": True,
                "is_active_updated_by": request.user.id,
                "is_active_updated_on": timezone.now(),
        })

    @admin.action(description = "Mark selected Codes as inactive")
    def mark_inactive(self, request, queryset):
        """
        Mark selected codes as inactive.
        """
        self.action(
            request, queryset, action = "inactive", 
            update_fields = {
                "is_active": False,
                "is_active_updated_by": request.user.id,
                "is_active_updated_on": timezone.now(),
        })