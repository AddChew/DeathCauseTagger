from django.contrib import admin

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
        "code_above",
        "created_by", "created_on", 
        "updated_by", "updated_on", 
        "is_active", "is_active_updated_by", "is_active_updated_on",
    )
    search_fields = (
        "code_input__description__icontains", 
        "code_below__description__icontains", 
        "code_equal__description__icontains",  
        "code_above__description__icontains", 
        "threshold",
    )
    ordering = ("code_input__description",)
    actions = ("mark_active", "mark_inactive")

    @admin.action(description = "Mark selected Periods as active")
    def mark_active(self, request, queryset):
        """
        Mark selected periods as active.
        """
        super().mark_active(request, queryset)

    @admin.action(description = "Mark selected Periods as inactive")
    def mark_inactive(self, request, queryset):
        """
        Mark selected periods as inactive.
        """
        super().mark_inactive(request, queryset)
