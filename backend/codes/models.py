from django.db import models
from model_utils import FieldTracker

from base.models import BaseModel, BaseIsActiveModel
from categories.models import Category


class Code(BaseModel, BaseIsActiveModel):
    """
    Code Model.
    """
    description = models.CharField(max_length = 200, unique = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "codes")

    is_active_tracker = FieldTracker(fields = ["is_active"])

    class Meta:
        verbose_name_plural = "Codes"

    def __str__(self):
        return self.description
