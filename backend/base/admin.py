from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """
    Base Admin Class for Model.
    """
    list_display = (
        "description", 
        "created_by", "created_on", 
        "updated_by", "updated_on", 
        "is_active", "is_active_updated_by", "is_active_updated_on",
    )
    list_filter = ("is_active",)
    search_fields = ("description__icontains",)

    def save_model(self, request, obj, form, change):
        """
        Save Model.
        """
        user = request.user

        if not change:
            obj.created_by = user

        if obj.is_active_tracker.has_changed("is_active"):
            obj.is_active_updated_by = user
        
        obj.updated_by = user

        super().save_model(request, obj, form, change)

# TODO: bulk change is_active action x 2 + message