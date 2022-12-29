from django.db import models
from django.contrib import admin
from authentication.models import User


class CustomForeignKey(models.ForeignKey):
    """
        Custom Foreign Key Field
    """
    def contribute_to_class(self, cls, name, private_only = False, **kwargs):
        super().contribute_to_class(cls, name, private_only, **kwargs)
        related_name = self.remote_field.related_name
        check_func = related_name.endswith
        if check_func('ys'):
            self.remote_field.related_name = f'{related_name[:-2]}ies'
        elif check_func('ss'):
            if check_func(')ss'):
                pass
            else:
                self.remote_field.related_name = f'{related_name[:-1]}es'

     
class BaseModel(models.Model):
    """
        Base Model for inheritance
    """
    created_by = CustomForeignKey(User, on_delete = models.CASCADE, related_name = "created_%(class)ss", default = User.get_default_user, editable = False)
    created_on = models.DateTimeField(auto_now_add = True)

    updated_by = CustomForeignKey(User, on_delete = models.CASCADE, related_name = "modified_%(class)ss", default = User.get_default_user, editable = False)
    updated_on = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


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