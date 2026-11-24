from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.city.schema import CityResponseSchema


class AddressBaseSchema(BaseModel):
    address: str = Field(..., min_length=10, max_length=50)
    district: str = Field(..., min_length=10, max_length=20)
    phone: str = Field(..., max_length=20)
    city_id: int = Field(..., gt=0)
    address2: str | None = Field(None, min_length=10, max_length=50)
    postal_code: str | None = Field(None, max_length=10)


class CreateAddressSchema(AddressBaseSchema):
    pass


class UpdateAddressSchema(AddressBaseSchema):
    pass


class PatchAddressSchema(BaseModel):
    address: str | None = Field(None, min_length=10, max_length=50)
    district: str | None = Field(None, min_length=10, max_length=20)
    phone: str | None = Field(None, max_length=20)
    city_id: int | None = Field(None, gt=0)
    address2: str | None = Field(None, min_length=10, max_length=50)
    postal_code: str | None = Field(None, max_length=10)


class AddressFiltersSchema(PatchAddressSchema):
    pass


class AddressBaseResponseSchema(BaseModel):
    id: int
    address: str
    district: str
    phone: str
    city_id: int
    address2: str | None
    postal_code: str | None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AddressResponseSchema(AddressBaseResponseSchema):
    pass



class AddressDetailResponseSchema(AddressBaseResponseSchema):
    city: CityResponseSchema | None = None
