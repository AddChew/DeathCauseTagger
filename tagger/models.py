from django.db import models
from django.contrib.postgres.indexes import GinIndex
from model_utils import FieldTracker
from model_utils.fields import MonitorField
from authentication.models import User
from tagger import constants
from tagger.utils import BaseModel


class Status(BaseModel):
    """
        Status Model
    """
    description = models.CharField(max_length = 50, unique = True)
    fields_tracker = FieldTracker()

    class Meta:
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.description


class Category(BaseModel):
    """
        Category Model
    """
    description = models.CharField(max_length = 200, unique = True)
    fields_tracker = FieldTracker()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.description


class DeathCause(BaseModel):
    """
        Death Cause Model
    """
    description = models.CharField(max_length = 200, unique = True)
    fields_tracker = FieldTracker()

    class Meta:
        verbose_name_plural = "Death Causes"
        indexes = [
            GinIndex(name = 'tagger_deathcause_desc_gin_idx', fields = ['description'], opclasses = ['gin_trgm_ops'])
        ]

    def __str__(self):
        return self.description


class Code(BaseModel):
    """
        Code Model 
    """
    description = models.CharField(max_length = 4, unique = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "codes")
    fields_tracker = FieldTracker()

    def __str__(self):
        return self.description


class Period(BaseModel):
    """
        Period Model
    """
    icd_input =  models.OneToOneField(Code, on_delete = models.CASCADE, related_name = "period") 
    threshold = models.PositiveSmallIntegerField()

    icd_below = models.ForeignKey(Code, on_delete = models.CASCADE, related_name = "below") 
    icd_equal = models.ForeignKey(Code, on_delete = models.CASCADE, related_name = "equal")
    icd_above = models.ForeignKey(Code, on_delete = models.CASCADE, related_name = "above")

    fields_tracker = FieldTracker()


class Mapping(BaseModel):
    """
        Mapping Model
    """
    description = models.ForeignKey(DeathCause, on_delete = models.CASCADE, related_name = "mappings")
    code = models.ForeignKey(Code, on_delete = models.CASCADE, related_name = "mappings")

    is_option = models.BooleanField(default = False)
    is_option_updated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "is_option_updated_mappings", to_field = "username", default = constants.SUPERUSER_USERNAME, editable = False)
    is_option_updated_on = MonitorField(monitor = "is_option", editable = False)

    status = models.ForeignKey(Status, on_delete = models.CASCADE, related_name = "mappings", to_field = "description", default = constants.Status.PENDING_REVIEW)
    status_updated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "status_updated_mappings", to_field = "username", default = constants.SUPERUSER_USERNAME, editable = False)
    status_updated_on = MonitorField(monitor = "status", editable = False)

    fields_tracker = FieldTracker()
 
    def __str__(self):
        return f'{self.description}: {self.code}'