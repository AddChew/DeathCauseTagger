from django.db import models
from model_utils import FieldTracker

from codes.models import Code
from deathcauses.models import DeathCause
from base.models import BaseModel, BaseIsOptionModel, BaseIsActiveModel, BaseIsOpenModel


class Mapping(BaseModel, BaseIsOptionModel, BaseIsActiveModel, BaseIsOpenModel):
    """
    Mapping Model.
    """
    code = models.ForeignKey(Code, on_delete = models.CASCADE, related_name = "mappings")
    death_cause = models.ForeignKey(DeathCause, on_delete = models.CASCADE, related_name = "mappings")

    is_option_tracker = FieldTracker(fields = ["is_option"])
    is_active_tracker = FieldTracker(fields = ["is_active"])
    is_open_tracker = FieldTracker(fields = ["is_open"])

    class Meta:
        verbose_name_plural = "Mappings"

    def __str__(self) -> str:
        return f"{self.code} - {self.death_cause}"
