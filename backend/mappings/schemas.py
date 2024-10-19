from ninja import Schema, Field
from pydantic import field_validator

from codes.models import Code
from deathcauses.models import DeathCause


class MappingSchema(Schema):
    """
    Mapping Schema.
    """
    code: str
    death_cause: str
    category: str = Field(alias = "code")

    @field_validator("code", mode = "before")
    @classmethod
    def parse_code(cls, code: Code) -> str:
        if not isinstance(code, Code):
            raise TypeError(f"{code} should be an instance of Code")
        return code.description
    
    @field_validator("death_cause", mode = "before")
    @classmethod
    def parse_death_cause(cls, death_cause: DeathCause) -> str:
        if not isinstance(death_cause, DeathCause):
            raise TypeError(f"{death_cause} should be an instance of DeathCause")
        return death_cause.description

    @field_validator("category", mode = "before")
    @classmethod
    def parse_category(cls, code: Code) -> str:
        if not isinstance(code, Code):
            raise TypeError(f"{code} should be an instance of Code")
        return code.category.description
