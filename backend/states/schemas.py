from typing import List
from pydantic import BaseModel, conlist, model_validator


class Empty(BaseModel):
    """
    Empty Schema.
    """
    class Config:
        extra = "forbid"


class Match(Empty):
    """
    Match Schema.
    """
    description: str
    code: str


class Option(Match):
    """
    Option Schema.
    """
    score: float


class Mapping(BaseModel):
    """
    Mapping Schema.
    """
    description: str
    duration: float
    match: Match | Empty
    options: conlist(Option, min_length = 0)

    @model_validator(mode = "after")
    def validate_match_options(self) -> 'Mapping':
        """
        Validate that only 1 of match and options fields is populated.

        Raises:
            ValueError: raised when both match and options are empty.
            ValueError: raised when both match and options are populated.

        Returns:
            Mapping: validated mapping object.
        """
        if type(self.match) is Empty and not len(self.options):
            raise ValueError("Both match and options are empty")
        
        if isinstance(self.match, Match) and len(self.options):
            raise ValueError("Only one of match or options can be populated")

        return self


class Mappings(Empty):
    """
    Mappings Schema.
    """
    mappings: List[Mapping]
    page: int


# TODO: input and output model for mappings