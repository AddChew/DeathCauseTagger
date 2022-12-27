from tagger.models import *
from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    list_display = ("description", "created_by", "created_on", "updated_by", "updated_on")
    ordering = ("pk",)
    search_fields = ("description__icontains",)

    def save_model(self, request, obj, form, change):
        if obj.fields_tracker.changed():
            if not change:
                obj.created_by = request.user
            obj.updated_by = request.user
            super().save_model(request, obj, form, change)


@admin.register(Status)
class StatusAdmin(BaseAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    pass


@admin.register(DeathCause)
class DeathCauseAdmin(BaseAdmin):
    pass


@admin.register(Code)
class CodeAdmin(BaseAdmin):
    list_display = ("description", "category", "created_by", "created_on", "updated_by", "updated_on")
    list_filter = ("category",)


@admin.register(Period)
class PeriodAdmin(BaseAdmin):
    list_display = ("icd_input", "threshold", "icd_below", "icd_equal", "icd_above", "created_by", "created_on", "updated_by", "updated_on")
    search_fields = (
        "icd_input__description__icontains", 
        "icd_below__description__icontains", 
        "icd_equal__description__icontains",  
        "icd_above__description__icontains", 
        "threshold"
    )


@admin.register(Mapping)
class MappingAdmin(BaseAdmin):
    list_display = (
        "description", "code", "is_option", "is_option_updated_by", "is_option_updated_on", 
        "status", "status_updated_by", "status_updated_on",
        "created_by", "created_on", "updated_by", "updated_on"
    )
    list_filter = ("status", "is_option", "code__category")
    search_fields = ("description__description__icontains", "code__description__icontains")

    def save_model(self, request, obj, form, change):
        if obj.fields_tracker.has_changed('status_id'):
            obj.status_updated_by = request.user

        if obj.fields_tracker.has_changed('is_option'):
            obj.is_option_updated_by = request.user

        super().save_model(request, obj, form, change)