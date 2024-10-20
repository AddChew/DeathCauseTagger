from ninja import Schema, Field


class MappingSchema(Schema):
    """
    Mapping Schema.
    """
    code: str = Field(alias = "code_description")
    death_cause: str = Field(alias = "death_cause_description")
    category: str = Field(alias = "category")
