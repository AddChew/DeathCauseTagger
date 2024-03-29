import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from model_utils.fields import MonitorField


User = get_user_model()


class BaseModel(models.Model):
    """
    Base Model.
    """
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

    created_by = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "created_%(class)ss",
        default = User.get_default_user,
        editable = False
    )
    created_on = models.DateTimeField(auto_now_add = True)

    updated_by = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "modified_%(class)ss",
        default = User.get_default_user,
        editable = False
    )
    updated_on = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


class BaseIsActiveModel(models.Model):
    """
    Base Is Active Model.
    """
    is_active = models.BooleanField(verbose_name = _("active"), default = True)
    is_active_updated_by = models.ForeignKey(
        User,
        verbose_name = _("active updated by"),
        on_delete = models.CASCADE,
        related_name = "is_active_updated_%(class)ss",
        default = User.get_default_user,
        editable = False
    )
    is_active_updated_on = MonitorField(
        verbose_name = _("active updated on"),
        monitor = "is_active",
        editable = False
    )

    class Meta:
        abstract = True
