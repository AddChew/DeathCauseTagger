from django.db import models
from model_utils import FieldTracker

from codes.models import Code
from deathcauses.models import DeathCause
from base.models import BaseModel, BaseIsOptionModel, BaseIsActiveModel, BaseIsPendingModel


class Mapping(BaseModel, BaseIsOptionModel, BaseIsActiveModel, BaseIsPendingModel):
    """
    Mapping Model.
    """
    code = models.ForeignKey(Code, on_delete = models.CASCADE, related_name = "mappings")
    description = models.ForeignKey(DeathCause, on_delete = models.CASCADE, related_name = "mappings")

    is_option_tracker = FieldTracker(fields = ["is_option"])
    is_active_tracker = FieldTracker(fields = ["is_active"])
    is_pending_tracker = FieldTracker(fields = ["is_pending"])

    class Meta:
        verbose_name_plural = "Mappings"

    def __str__(self):
        return f"{self.code}-{self.description}"
