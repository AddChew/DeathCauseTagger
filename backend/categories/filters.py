from ninja import Field
from typing import Optional
from base.filters import BaseFilterSchema


class CategoryFilterSchema(BaseFilterSchema):
    """
    Category Filter Schema.
    """
    description: Optional[str] = Field(None, q = "description__search")
