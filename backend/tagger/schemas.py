from ninja import Schema, Field
from typing import List, Optional
from pydantic import AliasChoices


class MappingSchema(Schema):
    """
    Mapping Schema.
    """
    code: str = Field(validation_alias = AliasChoices("code.description", "code"))
    death_cause: str = Field(validation_alias = AliasChoices("death_cause.description", "death_cause"))


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
    tag: Optional[MappingSchema] = None
    options: Optional[List[MappingSchema]] = None


class PeriodSchema(Schema):
    """
    Period Schema.
    """
    threshold: float
    code: str = Field(alias = "code_input.description")
    code_below: str = Field(alias = "code_below.description")
    code_equal: str = Field(alias = "code_equal.description")
    code_above: str = Field(alias = "code_above.description")
