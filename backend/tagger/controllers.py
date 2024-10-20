from ninja import PatchDict
from asgiref.sync import sync_to_async
from django.db import models
from django.forms.models import model_to_dict

from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTTokenUserAuth

from periods.models import Period
from mappings.models import Mapping
from tagger.schemas import TagSchema


@api_controller(
    prefix_or_class = "/tag",
    tags = ["tag"],
    permissions = [],
)
class TaggerController:
    """
    Tagger API Controller.
    """
    @route.get()
    async def tag_single(self, death_cause: str, period: float) -> PatchDict[TagSchema]:
        """
        Tag single death cause.
        """
        try:
            mapping = await Mapping.objects.select_related("code").aget(
                death_cause__description__iexact = death_cause, 
                is_active = True, 
                is_open = False
            ) # TODO: period
            if not mapping.is_option:
                mapping = await mapping.code.mappings.aget(
                    is_option = True, 
                    is_active = True, 
                    is_open = False
                )
            return {
                "description": death_cause,
                "period": period,
                "tag": await self.model_to_dict(mapping, fields = ["code", "death_cause"])
            }

        except Mapping.DoesNotExist:
            pass # TODO: retrieve options
        
    @staticmethod
    @sync_to_async
    def model_to_dict(instance: models.Model, fields: list = None, exclude: list = None) -> dict:
        """
        Convert model to dict.

        Args:
            instance (models.Model): Instance of ORM model object.
            fields (list, optional): Fields to include in model dict. Defaults to None.
            exclude (list, optional): Fields to exclude from model dict. Defaults to None.

        Returns:
            dict: Model dict.
        """
        opts = instance._meta.fields
        modeldict = model_to_dict(instance, fields = fields, exclude = exclude)
        for m in opts:
            if fields is not None and m.name not in fields:
                continue
            if exclude and m.name in exclude:
                continue
            if m.is_relation:
                foreignkey = getattr(instance, m.name)
                if foreignkey:
                    try:
                        modeldict[m.name] = str(foreignkey)
                    except:
                        pass
        return modeldict
