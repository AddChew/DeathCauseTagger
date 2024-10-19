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
        """
        Retrieve code description.

        Args:
            code (Code): Code ORM object.

        Raises:
            TypeError: Raised when code is not a Code object.

        Returns:
            str: Code description.
        """
        if not isinstance(code, Code):
            raise TypeError(f"{code} should be an instance of Code")
        return code.description
    
    @field_validator("death_cause", mode = "before")
    @classmethod
    def parse_death_cause(cls, death_cause: DeathCause) -> str:
        """
        Retrieve death cause.

        Args:
            death_cause (DeathCause): Death cause ORM object.

        Raises:
            TypeError: Raised when death cause is not a DeathCause object.

        Returns:
            str: Death cause description.
        """
        if not isinstance(death_cause, DeathCause):
            raise TypeError(f"{death_cause} should be an instance of DeathCause")
        return death_cause.description

    @field_validator("category", mode = "before")
    @classmethod
    def parse_category(cls, code: Code) -> str:
        """
        Retrieve code category description.

        Args:
            code (Code): Code ORM object.

        Raises:
            TypeError: Raised when code is not a Code object.

        Returns:
            str: Code category description.
        """
        if not isinstance(code, Code):
            raise TypeError(f"{code} should be an instance of Code")
        return code.category.description
