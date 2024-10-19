from ninja import Field
from typing import Optional
from base.filters import BaseFilterSchema


class MappingFilterSchema(BaseFilterSchema):
    """
    Mapping Filter Schema.
    """
    code: Optional[str] = Field(None, q = "code__description__icontains")
    death_cause: Optional[str] = Field(None, q = "death_cause__description__search")
    category: Optional[str] = Field(None, q = "code__category__description__search")
    
    option: Optional[bool] = Field(None, q = "is_option__exact")
    open: Optional[bool] = Field(None, q = "is_open__exact")
