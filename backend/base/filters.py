from ninja import FilterSchema, Field
from typing import Optional


class BaseFilterSchema(FilterSchema):
    """
    Base Filter Schema.
    """
    active: Optional[bool] = Field(None, q = "is_active__exact")

    class Config:
        expression_connector = "AND"
