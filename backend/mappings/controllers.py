from ninja import Query
from ninja_extra.pagination import paginate
from ninja_extra.ordering import ordering, Ordering

from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTTokenUserAuth
from ninja_extra.schemas import NinjaPaginationResponseSchema

from mappings.models import Mapping
from mappings.schemas import MappingSchema
from mappings.filters import MappingFilterSchema


@api_controller(
    prefix_or_class = "/mappings",
    tags = ["mappings"],
    permissions = [],
    auth = AsyncJWTTokenUserAuth(),
)
class MappingController:
    """
    Mapping API Controller.
    """
    @route.get()
    @paginate
    @ordering(
        Ordering, 
        ordering_fields = [
            "code__description", "death_cause__description", 
            "code__category__description"
        ]
    )
    async def read_mappings(
        self, filters: MappingFilterSchema = Query(...)
        ) -> NinjaPaginationResponseSchema[MappingSchema]:
        """
        Read mappings.
        """
        return filters.filter(Mapping.objects.all())
