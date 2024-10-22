from typing import List
from ninja import Schema, Field


class MappingSchema(Schema):
    """
    Mapping Schema.
    """
    code: str = Field(alias = "code.description")
    death_cause: str = Field(alias = "death_cause.description")


class DeathCauseSchema(Schema):
    """
    Death Cause Schema.
    """
    description: str
    period: float


class TagSchema(Schema):
    """
    Tag Schema.
    """
    description: str
    period: float
    tag: MappingSchema
    options: List[MappingSchema]
