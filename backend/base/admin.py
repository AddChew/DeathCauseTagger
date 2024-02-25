from django.utils import timezone
from django.contrib import admin, messages


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
    ordering = ("description",)
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

    def action(self, request, queryset, action, update_fields):
        """
        Base Admin Action.
        """
        meta = self.model._meta
        count = queryset.update(
            updated_by = request.user.id,
            updated_on = timezone.now(),
            **update_fields
        )
        model_name = meta.verbose_name_plural if count > 1 else meta.verbose_name
        message = f"Successfully marked {count} {model_name.lower()} as {action}"
        self.message_user(
            request = request,
            message = message,
            level = messages.SUCCESS
        )
