from ninja_extra.pagination import paginate
from ninja_extra import api_controller, route

from ninja_jwt.authentication import AsyncJWTTokenUserAuth
from ninja_extra.schemas import NinjaPaginationResponseSchema

from categories.models import Category
from categories.schemas import CategorySchema


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
    queryset = Category.objects.all()

    @route.get()
    @paginate
    async def read_categories(self) -> NinjaPaginationResponseSchema[CategorySchema]:
        """
        Read categories.
        """
        return self.queryset