from datetime import datetime

from pydantic import BaseModel, Field


class BaseLanguageSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description="language name",
        examples=["english"],
    )


class CreateLanguageSchema(BaseLanguageSchema):
    pass


class LanguageResponseSchema(BaseLanguageSchema):
    id: int
    created_at: datetime
    updated_at: datetime
