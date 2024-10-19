from typing import Optional
from ninja import FilterSchema, Field


class BaseFilterSchema(FilterSchema):
    """
    Base Filter Schema.
    """
    active: Optional[bool] = Field(None, q = "is_active__exact")

    class Config:
        expression_connector = "AND"
