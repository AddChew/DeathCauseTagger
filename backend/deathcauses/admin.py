from django.contrib import admin

from base.admin import BaseAdmin
from deathcauses.models import DeathCause


@admin.register(DeathCause)
class DeathCauseAdmin(BaseAdmin):
    """
    Admin Class for DeathCause Model.
    """
    actions = ("mark_active", "mark_inactive")

    @admin.action(description = "Mark selected Death Causes as active")
    def mark_active(self, request, queryset):
        """
        Mark selected death causes as active.
        """
        super().mark_active(request, queryset)

    @admin.action(description = "Mark selected Death Causes as inactive")
    def mark_inactive(self, request, queryset):
        """
        Mark selected death causes as inactive.
        """
        super().mark_inactive(request, queryset)
