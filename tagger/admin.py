from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionMixin, ImportExportModelAdmin, ExportMixin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class ExportModelAdmin(ExportMixin, admin.ModelAdmin):
    """
        Custom ExportModelAdmin class

        Only supports export functionality
    """
    change_list_template = 'admin/import_export/change_list_export.html'



### Resource Classes
class BaseMeta:
    """
        Base Meta class for Resources
    """
    skip_unchanged = True
    report_skipped = False      


class AnnotationResource(resources.ModelResource):
    """
        Resource class for Annotation Model
    """
    class Meta(BaseMeta):
        model = Annotation
        fields = ("description", "icd")
        export_order = ("description", "icd")
        exclude = ("id",)


class MappingResource(resources.ModelResource):
    """
        Resource class for Mapping Model
    """
    class Meta(BaseMeta):
        model = Mapping
        fields = ("id", "description", "icd")
        export_order = ("id", "description", "icd")


class CategoryResource(resources.ModelResource):
    """
        Resource class for Category Model
    """
    class Meta(BaseMeta):
        model = Category
        fields = ("id", "description")
        export_order = ("id", "description")


class ICDResource(resources.ModelResource):
    """
        Resource class for ICD Model
    """
    class Meta(BaseMeta):
        model = ICD
        fields = ("id", "code", "description", "category")
        export_order = ("id", "code", "description", "category")


class PeriodResource(resources.ModelResource):
    """
        Resource class for Period Model
    """
    class Meta(BaseMeta):
        model = Period
        fields = ("id", "icd_input", "threshold", "icd_below", "icd_equal", "icd_above")
        export_order = ("id", "icd_input", "threshold", "icd_below", "icd_equal", "icd_above")



### Admin Classes
@admin.register(Annotation)
class AnnotationAdmin(ExportModelAdmin, ExportActionMixin):
    """
        Admin class for Annotation Model
    """
    list_display = ("description", "icd")
    list_filter = ("icd__category",)
    search_fields = (
        "description__icontains",
        "icd__description__icontains", 
        "icd__code__icontains", 
        )
    resource_class = AnnotationResource


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
        Admin class for Category Model
    """
    list_display = ("id", "description")
    search_fields = (
        "description__icontains",
        )
    resource_class = CategoryResource


@admin.register(ICD)
class ICDAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
        Admin class for ICD Model
    """
    list_display = ("id", "code", "description", "category")
    list_filter = ("category",)
    search_fields = (
        "description__icontains",
        "code__icontains", 
        )
    resource_class = ICDResource


@admin.register(Mapping)
class MappingAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
        Admin class for Mapping Model
    """
    list_display = ("description", "icd")
    list_filter = ("icd__category",)
    search_fields = (
        "description__icontains",
        "icd__description__icontains", 
        "icd__code__icontains", 
        )
    resource_class = MappingResource


@admin.register(Period)
class PeriodAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
        Admin class for Period Model
    """
    list_display = ("icd_input", "threshold", "icd_below", "icd_equal", "icd_above")
    list_filter = ("threshold",)
    search_fields = (
        "icd_input__description__icontains", 
        "icd_input__code__icontains", 
        "icd_below__description__icontains", 
        "icd_below__code__icontains", 
        "icd_equal__description__icontains", 
        "icd_equal__code__icontains", 
        "icd_above__description__icontains", 
        "icd_above__code__icontains", 
        "threshold"
        )
    resource_class = PeriodResource

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(UserAdmin):
    """
        Admin class for User Model
    """
    list_display = ("username", "date_joined", "is_superuser", "is_active", "last_login")
    list_filter = ("is_active", "is_superuser")
    search_fields = ("username__startswith",)