from django.contrib import admin

from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin Class for Category Model.
    """
    list_display = (
        "description", "status", "created_by", "created_on", "updated_by", 
        "updated_on", "status_updated_by", "status_updated_on",
    )
    list_filter = ("status",)
    search_fields = ("description__icontains",)