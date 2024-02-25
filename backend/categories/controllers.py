from typing import List
from django.db.models import Case, When, Value

from ninja_extra import api_controller, http_get
from ninja_jwt.authentication import AsyncJWTTokenUserAuth

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

    @http_get()
    async def read_categories(self, description: str = None) -> List[CategorySchema]:
        """
        Read categories.
        """
        if description is not None:
            return self.queryset.annotate(
                search_rank = Case(
                    When(description__iexact = description, then = Value(0)),
                    When(description__istartswith = description, then = Value(1)),
                    When(description__icontains = description, then = Value(2)),
                    default = Value(99),
                )
            ).exclude(search_rank = 99) \
            .order_by("search_rank")
        return self.queryset
