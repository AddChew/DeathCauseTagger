from django.db import models
from authentication.models import User


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
    created_by = CustomForeignKey(User, on_delete = models.CASCADE, related_name = "created_%(class)ss")
    created_on = models.DateTimeField(auto_now_add = True)
    updated_by = CustomForeignKey(User, on_delete = models.CASCADE, related_name = "modified_%(class)ss")
    updated_on = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True