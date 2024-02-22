from django.db import models
from model_utils import FieldTracker
from django.contrib.postgres.indexes import GinIndex

from base.models import BaseModel, BaseIsActiveModel


class DeathCause(BaseModel, BaseIsActiveModel):
    """
    Death Cause Model.
    """    
    description = models.CharField(max_length = 200, unique = True)
    is_active_tracker = FieldTracker(fields = ["is_active"])

    class Meta:
        verbose_name_plural = "Death Causes"
        indexes = [
            GinIndex(name = "death_cause_desc_gin_idx", fields = ["description"], opclasses = ["gin_trgm_ops"])
        ]

    def __str__(self):
        return self.description