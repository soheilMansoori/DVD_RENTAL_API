from datetime import datetime

from pydantic import BaseModel, Field

from app.country.schema import CountryResponseSchema


class CityBaseSchema(BaseModel):
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


class CreateCitySchema(CityBaseSchema):
    pass


class CityFiltersSchema(BaseModel):
    city: str | None = Field(None, max_length=50)
    country_id: int | None = Field(None, gt=0)


class CityBaseResponseSchema(BaseModel):
    id: int
    city: str
    country_id: int
    created_at: datetime
    updated_at: datetime


class CityResponseSchema(CityBaseResponseSchema):
    pass


class CityDetailResponseSchema(CityResponseSchema):
    country: CountryResponseSchema | None
