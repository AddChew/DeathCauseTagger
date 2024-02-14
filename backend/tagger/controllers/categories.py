from typing import List, Dict
from ninja_extra import api_controller, http_get


@api_controller(
    prefix_or_class = "/categories",
    tags = ["Categories"],
    permissions = [],
)
class CategoryController:

    @http_get()
    def read_categories(self) -> List[Dict]: # TODO:
        """Read categories"""
        return [
            {'code': 'A00', 'description': 'testing'}
        ]