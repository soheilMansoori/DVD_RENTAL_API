from datetime import datetime

from pydantic import BaseModel, Field


class ActorBaseSchema(BaseModel):
    first_name: str = Field(
        ...,
        min_length=4,
        max_length=45,
        description="actor first_name",
        examples=["soheil"],
    )

    last_name: str = Field(
        ...,
        min_length=4,
        max_length=45,
        description="actor last_name",
        examples=["mansoori"],
    )


class ActorFiltersSchema(BaseModel):
    first_name: str | None = Field(None, min_length=4)
    last_name: str | None = Field(None, min_length=4)


class CreateActorSchema(ActorBaseSchema):
    pass


class UpdateActorSchema(ActorBaseSchema):
    pass


class PatchActorSchema(BaseModel):
    first_name: str | None = Field(
        None,
        min_length=4,
        max_length=45,
        description="actor first_name",
        examples=["soheil"],
    )

    last_name: str | None = Field(
        None,
        min_length=4,
        max_length=45,
        description="actor last_name",
        examples=["mansoori"],
    )


class ActorResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime
