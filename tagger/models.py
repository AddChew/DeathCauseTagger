from django.db import models
from django.contrib.postgres.indexes import GinIndex
from model_utils import FieldTracker
from model_utils.fields import MonitorField
from authentication.models import User
from tagger import constants


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

    @classmethod
    def get_default_status(cls):
        default_status, _ = cls.objects.get_or_create(
            description = constants.Status.PENDING_REVIEW
        )
        return default_status.id


class Category(BaseModel):
    """
        Category Model
    """
    description = models.CharField(max_length = 200, unique = True)

    status = models.ForeignKey(Status, on_delete = models.CASCADE, related_name = "categories", default = Status.get_default_status)
    status_updated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "status_updated_categories", default = User.get_default_user, editable = False)
    status_updated_on = MonitorField(monitor = "status", editable = False)

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

    status = models.ForeignKey(Status, on_delete = models.CASCADE, related_name = "causes", default = Status.get_default_status)
    status_updated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "status_updated_causes", default = User.get_default_user, editable = False)
    status_updated_on = MonitorField(monitor = "status", editable = False)

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

    status = models.ForeignKey(Status, on_delete = models.CASCADE, related_name = "codes", default = Status.get_default_status)
    status_updated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "status_updated_codes", default = User.get_default_user, editable = False)
    status_updated_on = MonitorField(monitor = "status", editable = False)

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

    status = models.ForeignKey(Status, on_delete = models.CASCADE, related_name = "periods", default = Status.get_default_status)
    status_updated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "status_updated_periods", default = User.get_default_user, editable = False)
    status_updated_on = MonitorField(monitor = "status", editable = False)

    fields_tracker = FieldTracker()


class Mapping(BaseModel):
    """
        Mapping Model
    """
    description = models.ForeignKey(DeathCause, on_delete = models.CASCADE, related_name = "mappings")
    code = models.ForeignKey(Code, on_delete = models.CASCADE, related_name = "mappings")

    is_option = models.BooleanField(default = False)
    is_option_updated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "is_option_updated_mappings", default = User.get_default_user, editable = False)
    is_option_updated_on = MonitorField(monitor = "is_option", editable = False)

    status = models.ForeignKey(Status, on_delete = models.CASCADE, related_name = "mappings", default = Status.get_default_status)
    status_updated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "status_updated_mappings", default = User.get_default_user, editable = False)
    status_updated_on = MonitorField(monitor = "status", editable = False)

    fields_tracker = FieldTracker()
 
    def __str__(self):
        return f'{self.description}: {self.code}'