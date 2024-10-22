from ninja import PatchDict
from typing import Iterable, List
from asgiref.sync import sync_to_async

from django.shortcuts import _get_queryset
from ninja_extra import api_controller, route
from django.contrib.postgres.search import TrigramSimilarity

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
        response = {"description": death_cause, "period": period}
        mapping = await self.aget_object_or_none(
            Mapping,
            related_fields = ["code"],
            death_cause__description__iexact = death_cause,
            is_active = True,
            is_open = False
        )
        if mapping is None:
            mappings = Mapping.objects.filter(is_active = True, is_open = False) \
                                      .annotate(score = TrigramSimilarity(
                                          "death_cause__description", death_cause)) \
                                      .order_by("-score") \
                                      .prefetch_related("code") \
                                      [:100]
            response.update({"options": await self.retrieve_options(mappings)})
            return response
        
        queryset = mapping.code.mappings
        periods = await self.aget_object_or_none(
            Period,
            related_fields = [],
            code_input = mapping.code,
            is_active = True,
        )
        if isinstance(periods, Period):
            if period < periods.threshold:
                code = periods.code_below

            elif period == periods.threshold:
                code = periods.code_equal

            else:
                code = periods.code_above

            queryset = code.mappings

        mapping = await self.aget_object_or_none(
            queryset,
            is_option = True,
            is_active = True,
            is_open = False
        )
        response.update({"tag": mapping})
        return response

    @sync_to_async
    def retrieve_options(self, mappings: Iterable[Mapping]) -> List[Mapping]:
        """
        Retrieve option mappings with scores.

        Args:
            mappings (Iterable[Mapping]): Top N most similar mappings to query.

        Returns:
            List[Mapping]: Option mappings.
        """
        options = []
        for mapping in mappings:
            option = mapping.code.mappings.get(
                is_active = True,
                is_option = True,
                is_open = False
            )
            if option not in options:
                options.append(option)

            if len(options) == 5:
                return options
        return options

    @staticmethod
    async def aget_object_or_none(klass, related_fields: Iterable[str] = None, *args, **kwargs):
        """
        Get object if it exists, otherwise return None.

        Args:
            klass: Model, Manager of QuerySet. 
            related_fields (Iterable[str], optional): Fields for selected_related. Defaults to None.

        Raises:
            ValueError: Raised when klass is not a Model, Manager or QuerySet.

        Returns:
            Union[models.Model, None]: Model object if it exists, otherwise None.
        """
        queryset = _get_queryset(klass)
        if not hasattr(queryset, "aget"):
            klass__name = (
                klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
            )
            raise ValueError(
                "First argument to aget_object_or_none() must be a Model, Manager, or "
                f"QuerySet, not '{klass__name}'."
            )
        if related_fields is None:
            related_fields = (None,)
        try:
            return await queryset.select_related(*related_fields).aget(*args, **kwargs)
        except queryset.model.DoesNotExist:
            return None
