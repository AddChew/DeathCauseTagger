from django.contrib import admin
from django.utils import timezone

from base.admin import BaseAdmin
from periods.models import Period


@admin.register(Period)
class PeriodAdmin(BaseAdmin):
    """
    Admin Class for Period Model.
    """
    list_display = (
        "code_input",
        "threshold",
        "code_below",
        "code_equal",
        "code_above"
        "created_by", "created_on", 
        "updated_by", "updated_on", 
        "is_active", "is_active_updated_by", "is_active_updated_on",
    )
    search_fields = (
        "code_input__description__icontains", 
        "code_below__description__icontains", 
        "code_equal__description__icontains",  
        "code_above__description__icontains", 
        "threshold"
    )
    ordering = ("code_input",)
    actions = ["mark_active", "mark_inactive"]

    @admin.action(description = "Mark selected Periods as active")
    def mark_active(self, request, queryset):
        """
        Mark selected periods as active.
        """
        self.action(
            request, queryset, action = "active", 
            update_fields = {
                "is_active": True,
                "is_active_updated_by": request.user.id,
                "is_active_updated_on": timezone.now(),
        })

    @admin.action(description = "Mark selected Periods as inactive")
    def mark_inactive(self, request, queryset):
        """
        Mark selected periods as inactive.
        """
        self.action(
            request, queryset, action = "inactive", 
            update_fields = {
                "is_active": False,
                "is_active_updated_by": request.user.id,
                "is_active_updated_on": timezone.now(),
        })