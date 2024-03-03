from django.db import models
from model_utils import FieldTracker

from base.models import BaseModel, BaseIsActiveModel


class State(BaseModel, BaseIsActiveModel):
    """
    State Model.
    """
    data = models.JSONField(blank = False, null = False)
    is_active_tracker = FieldTracker(fields = ["is_active"])

    class Meta:
        verbose_name_plural = "States"

    def __str__(self):
        return self.id