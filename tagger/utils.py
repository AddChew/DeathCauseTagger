from django.db import models
from django.db.models import Q
from django.http import Http404
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.request import clone_request
from django_filters.rest_framework import FilterSet
from tagger import constants
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


class BaseMappingFilterSet(FilterSet):
    active_option_cond = Q(is_option = True) & Q(status__description = constants.Status.ACTIVE)


class CustomSlugRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            return self.get_queryset().create(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('Invalid data type or value.')


class PutAsCreateMixin:
    """
    The following mixin class may be used in order to support
    PUT-as-create behavior for incoming requests.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        data = {field: value.upper() for field, value in request.data.items()}
        
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        status_code = status.HTTP_201_CREATED
        extra_kwargs = {'updated_by': request.user}

        if instance is None:
            extra_kwargs.update({'created_by': request.user})
            status_code = status.HTTP_204_NO_CONTENT

        serializer.save(**extra_kwargs)
        return Response(serializer.data, status = status_code)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request. This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise