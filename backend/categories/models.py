from django.db import models
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField, MonitorField

from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    """
    Category Model.
    """
    STATUS = Choices(
        (0, "approved"),
        (1, "rejected"),
        (2, "pending"),
    )

    description = models.CharField(max_length = 200, unique = True)
    status = StatusField(default = 0)

    created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "created_categories", default = User.get_default_user, editable = False)
    created_on = models.DateTimeField(auto_now_add = True)

    updated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "modified_categories", default = User.get_default_user, editable = False)
    updated_on = models.DateTimeField(auto_now = True)

    status_updated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "status_updated_categories", default = User.get_default_user, editable = False)
    status_updated_on = MonitorField(monitor = "status", editable = False)

    fields_tracker = FieldTracker()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.description