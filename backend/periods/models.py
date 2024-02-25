from django.db import models
from model_utils import FieldTracker

from base.models import BaseModel, BaseIsActiveModel
from codes.models import Code


class Period(BaseModel, BaseIsActiveModel):
    """
    Period Model.
    """
    code_input = models.OneToOneField(Code, on_delete = models.CASCADE, related_name = "period")
    threshold = models.PositiveSmallIntegerField()

    code_below = models.ForeignKey(Code, on_delete = models.CASCADE, related_name = "below")
    code_equal = models.ForeignKey(Code, on_delete = models.CASCADE, related_name = "equal")
    code_above = models.ForeignKey(Code, on_delete = models.CASCADE, related_name = "above")

    is_active_tracker = FieldTracker(fields = ["is_active"])

    class Meta:
        verbose_name_plural = "Periods"
