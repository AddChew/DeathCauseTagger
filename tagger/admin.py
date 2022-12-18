from tagger.models import *
from django.contrib import admin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "created_by", "created_on", "modified_by", "modified_on")
    ordering = ("pk",)
    search_fields = ("description__icontains",)


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "category", "created_by", "created_on", "modified_by", "modified_on")
    ordering = ("pk",)
    list_filter = ("category",)
    search_fields = ("description__icontains",)


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ("id", "icd_input", "threshold", "icd_below", "icd_equal", "icd_above", "created_by", "created_on", "modified_by", "modified_on")
    ordering = ("pk",)
    search_fields = (
        "icd_input__description__icontains", 
        "icd_below__description__icontains", 
        "icd_equal__description__icontains",  
        "icd_above__description__icontains", 
        "threshold"
        )


@admin.register(Mapping)
class MappingAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "code", "is_option", "optioned_by", "optioned_on", "is_approved", "approved_by", "approved_on", "created_by", "created_on", "modified_by", "modified_on")
    list_filter = ("is_option", "is_approved", "code__category")
    ordering = ("pk",)
    search_fields = ("description__icontains", "code__description__icontains")