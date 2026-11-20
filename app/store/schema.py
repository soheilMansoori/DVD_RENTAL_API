from datetime import datetime

from pydantic import BaseModel, Field


class BaseStoreSchema(BaseModel):
    manager_staff_id: int | None = Field(None, gt=0)
    address_id: int = Field(..., gt=0)


class CreateStoreSchema(BaseStoreSchema):
    pass


class UpdateStoreSchema(BaseStoreSchema):
    pass


class PatchStoreSchema(BaseModel):
    manager_staff_id: int | None = Field(None, gt=0)
    address_id: int | None = Field(None, gt=0)


class StoreFiltersSchema(PatchStoreSchema):
    pass


class StoreResponseSchema(BaseStoreSchema):
    id: int = Field(..., gt=0)
    created_at: datetime
    updated_at: datetime
