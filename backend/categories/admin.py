from django.contrib import admin
from base.admin import BaseAdmin
from categories.models import Category


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    """
    Admin Class for Category Model.
    """
    actions = ("mark_active", "mark_inactive")

    @admin.action(description = "Mark selected Categories as active")
    def mark_active(self, request, queryset):
        """
        Mark selected categories as active.
        """
        super().mark_active(request, queryset)

    @admin.action(description = "Mark selected Categories as inactive")
    def mark_inactive(self, request, queryset):
        """
        Mark selected categories as inactive.
        """
        super().mark_inactive(request, queryset)
