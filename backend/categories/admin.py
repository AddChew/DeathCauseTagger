from django.contrib import admin

from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin Class for Category Model.
    """
    list_display = (
        "description", "get_status_display", "created_by", "created_on", "updated_by", 
        "updated_on", "status_updated_by", "status_updated_on",
    )
    list_filter = ("status",)
    search_fields = ("description__icontains",)

    def get_status_display(self, obj):
        return obj.get_status_display()
    
    get_status_display.short_description = "status"

    def save_model(self, request, obj, form, change):
        user = request.user

        if not change:
            obj.created_by = user

        if obj.fields_tracker.has_changed("status"):
            obj.status_updated_by = user
        
        obj.updated_by = user

        super().save_model(request, obj, form, change)

# TODO: message when status change
# TODO: bulk change status action + message