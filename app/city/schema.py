from datetime import datetime

from pydantic import BaseModel, Field


class BaseCitySchema(BaseModel):
    city: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="city name",
        examples=["karaj"],
    )

    country_id: int = Field(
        ...,
        gt=0,
        description="country id",
    )


class CreateCitySchema(BaseCitySchema):
    pass


class CityFiltersSchema(BaseModel):
    city: str | None = Field(None, max_length=50)
    country_id: int | None = Field(None, gt=0)


class CityResponseSchema(BaseCitySchema):
    id: int
    created_at: datetime
    updated_at: datetime
