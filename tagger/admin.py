from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionMixin, ImportExportModelAdmin, ExportMixin
from .models import *


class ExportModelAdmin(ExportMixin, admin.ModelAdmin):
    """
        Custom ExportModelAdmin class

        Only supports export functionality
    """
    change_list_template = 'admin/import_export/change_list_export.html'



### Define Resource Classes
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



### Define Admin Classes
class AnnotationAdmin(ExportModelAdmin, ExportActionMixin):
    """
        Admin class for Annotation Model
    """
    list_display = ("description", "icd")
    list_filter = ("icd",)
    resource_class = AnnotationResource


class CategoryAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
        Admin class for Category Model
    """
    list_display = ("id", "description")
    resource_class = CategoryResource


class ICDAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
        Admin class for ICD Model
    """
    list_display = ("id", "code", "description", "category")
    list_filter = ("category",)
    resource_class = ICDResource


class MappingAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
        Admin class for Mapping Model
    """
    list_display = ("description", "icd")
    list_filter = ("icd",)
    resource_class = MappingResource


class PeriodAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
        Admin class for Period Model
    """
    list_display = ("icd_input", "threshold", "icd_below", "icd_equal", "icd_above")
    resource_class = PeriodResource


class UserAdmin(admin.ModelAdmin):
    """
        Admin class for User Model
    """
    list_display = ("username", "date_joined", "is_superuser", "is_active", "last_login")


# Register models to admin site
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ICD, ICDAdmin)
admin.site.register(Mapping, MappingAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(User, UserAdmin)