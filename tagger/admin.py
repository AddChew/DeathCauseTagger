from django.db.models import Q
from django.contrib import admin
from tagger.models import *
from tagger import constants
from tagger.utils import BaseAdmin


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

            if obj.status.description == constants.Status.ACTIVE:
                rejected_status = Status.objects.get(description = constants.Status.REJECTED)
                self.model.objects.filter(
                    Q(description = obj.description) & Q(status__description = constants.Status.PENDING_REVIEW)
                ).update(status = rejected_status)

        if obj.fields_tracker.has_changed('is_option'):
            obj.is_option_updated_by = request.user

            if obj.is_option:
                self.model.objects.filter(
                    Q(code = obj.code) & Q(is_option = True)
                ).update(is_option = False)

        super().save_model(request, obj, form, change)

    # TODO: Admin actions to mass approve mappings
    # TODO: Raise error if two share the same description