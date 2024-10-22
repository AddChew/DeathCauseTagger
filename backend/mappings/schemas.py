from ninja import Schema, Field


class MappingSchema(Schema):
    """
    Mapping Schema.
    """
    code: str = Field(alias = "code.description")
    death_cause: str = Field(alias = "death_cause.description")
    category: str = Field(alias = "code.category.description")
