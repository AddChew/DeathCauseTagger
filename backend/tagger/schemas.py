from typing import List
from ninja import Schema


class MappingSchema(Schema):
    """
    Mapping Schema.
    """
    code: str
    death_cause: str


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
