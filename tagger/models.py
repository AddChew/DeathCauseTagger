from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class Category(models.Model):
    """
        ICD Category Model
    """
    description = models.CharField(max_length = 110, unique = True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("pk",)

    def __str__(self):
        return self.description


class ICD(models.Model):
    """
        ICD Death Cause Model
    """
    code = models.CharField(max_length = 4, unique = True)
    description = models.CharField(max_length = 160, unique = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "death_causes")

    class Meta:
        verbose_name_plural = "ICD"
        ordering = ("code",)

    def __str__(self):
        return f"{self.code} - {self.description}"


class Mapping(models.Model):
    """
        Mapping Model
    """
    description = models.CharField(max_length = 200, unique = True)
    icd = models.ForeignKey(ICD, on_delete = models.CASCADE, related_name = "mappings")
    search_vector = SearchVectorField(null = True)

    class Meta:
        ordering = ("icd__code",)
        indexes = [
            GinIndex(fields=['search_vector']), 
            GinIndex(name='tagger_mapping_desc_gin_idx', fields=['description'], opclasses=['gin_trgm_ops'])
        ]

    def __str__(self):
        return f"{self.description} - {self.icd.code}"


class Period(models.Model):
    """
        Time Period Model
    """
    icd_input =  models.OneToOneField(ICD, on_delete = models.CASCADE, related_name = "period") 
    threshold = models.PositiveSmallIntegerField()

    icd_below = models.ForeignKey(ICD, on_delete = models.CASCADE, related_name = "below") 
    icd_equal = models.ForeignKey(ICD, on_delete = models.CASCADE, related_name = "equal")
    icd_above = models.ForeignKey(ICD, on_delete = models.CASCADE, related_name = "above")

    class Meta:
        ordering = ("icd_input__code",)

    def __str__(self):
        return f"{self.icd_input.code} - {self.threshold}"


class Annotation(models.Model):
    """
        Annotation Model
    """
    description = models.CharField(max_length = 200, unique = True)
    icd = models.ForeignKey(ICD, on_delete = models.CASCADE, related_name = "annotations")

    class Meta:
        ordering = ("icd__code",)

    def __str__(self):
        return f"{self.description} - {self.icd.code}"


class NewCategory(models.Model):
    """
        New Category Model
    """
    description = models.CharField(max_length = 200, unique = True)
    search_vector = SearchVectorField(null = True)
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "created_categories")
    created_on = models.DateTimeField(auto_now_add = True)
    modified_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "modified_categories")
    modified_on = models.DateTimeField(auto_now = True)

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]

    def __str__(self):
        return self.description