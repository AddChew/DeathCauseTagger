from django.db import models
from base.models import BaseModel, BaseIsActiveModel


class Category(BaseModel, BaseIsActiveModel):
    """
    Category Model.
    """    
    description = models.CharField(max_length = 200, unique = True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.description