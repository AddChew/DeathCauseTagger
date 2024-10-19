from ninja import Query
from ninja_extra.ordering import ordering
from ninja_extra.pagination import paginate

from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTTokenUserAuth
from ninja_extra.schemas import NinjaPaginationResponseSchema

from categories.models import Category
from categories.schemas import CategorySchema
from categories.filters import CategoryFilterSchema


@api_controller(
    prefix_or_class = "/categories",
    tags = ["categories"],
    permissions = [],
    auth = AsyncJWTTokenUserAuth(),
)
class CategoryController:
    """
    Category API Controller.
    """
    @route.get()
    @paginate
    @ordering
    async def read_categories(
        self, filters: CategoryFilterSchema = Query(...)
        ) -> NinjaPaginationResponseSchema[CategorySchema]:
        """
        Read categories.
        """
        return filters.filter(Category.objects.all())
