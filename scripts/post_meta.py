"""Schema for metadata accompanying a published post."""

from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    StrictStr,
    StringConstraints,
)


NonEmptyString = Annotated[
    StrictStr,
    StringConstraints(min_length=1, strip_whitespace=True),
]


class PostMeta(BaseModel):
    """Validate the required metadata for a post."""

    model_config = ConfigDict(extra="forbid", strict=True)

    title: NonEmptyString
    LLM_description: NonEmptyString
    year: StrictInt
    month: Annotated[StrictInt, Field(ge=1, le=12)]
    day: Annotated[StrictInt, Field(ge=1, le=31)]
    active: StrictBool
    tags: list[StrictStr]
