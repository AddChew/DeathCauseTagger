from django.contrib import admin
from django.utils import timezone

from base.admin import BaseAdmin
from mappings.models import Mapping


@admin.register(Mapping)
class MappingAdmin(BaseAdmin):
    """
    Admin Class for Mapping Model.
    """
    list_display = (
        "code", "death_cause", "code__category",
        "created_by", "created_on", 
        "updated_by", "updated_on", 
        "is_option", "is_option_updated_by", "is_option_updated_on",
        "is_active", "is_active_updated_by", "is_active_updated_on",
        "is_open", "is_open_updated_by", "is_open_updated_on",
    )
    list_filter = ("is_option", "is_active", "is_open", "code__category")

    ordering = ("code__description",)
    search_fields = ("code__description__icontains", "death_cause__description__icontains")

    actions = ("mark_active", "mark_inactive")

    def save_model(self, request, obj, form, change):
        """
        Save Model.
        """
        user = request.user

        if obj.is_option_tracker.has_changed("is_option"):
            obj.is_option_updated_by = user

        if obj.is_open_tracker.has_changed("is_open"):
            obj.is_open_updated_by = user

        super().save_model(request, obj, form, change)

    @admin.action(description = "Mark selected Mappings as option")
    def mark_option(self, request, queryset):
        """
        Mark selected mappings as option.
        """
        self.action(
            request, queryset, action = "option",
            update_fields = {
                "is_option": True,
                "is_option_updated_by": request.user.id,
                "is_option_updated_on": timezone.now(),
        })

    @admin.action(description = "Mark selected Mappings as non-option")
    def mark_non_option(self, request, queryset):
        """
        Mark selected mappings as non-option.
        """
        self.action(
            request, queryset, action = "non-option",
            update_fields = {
                "is_option": False,
                "is_option_updated_by": request.user.id,
                "is_option_updated_on": timezone.now(),
        })

    @admin.action(description = "Mark selected Mappings as active")
    def mark_active(self, request, queryset):
        """
        Mark selected mappings as active.
        """
        super().mark_active(request, queryset)

    @admin.action(description = "Mark selected Mappings as inactive")
    def mark_inactive(self, request, queryset):
        """
        Mark selected mappings as inactive.
        """
        super().mark_inactive(request, queryset)
