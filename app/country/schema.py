from datetime import datetime

from pydantic import BaseModel, Field


class BaseCountrySchema(BaseModel):
    country: str = Field(
        ...,
        max_length=50,
        description="country name",
        examples=["iran"],
    )


class CreateCountrySchema(BaseCountrySchema):
    pass


class CountryFiltersSchema(BaseModel):
    country: str | None = Field(None, max_length=50)


class CountryResponseSchema(BaseCountrySchema):
    id: int
    created_at: datetime
    updated_at: datetime
