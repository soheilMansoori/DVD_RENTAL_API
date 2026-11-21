from datetime import datetime

from pydantic import BaseModel, Field


class BaseInventorySchema(BaseModel):
    film_id: int = Field(..., gt=0)
    store_id: int = Field(..., gt=0)


class CreateInventorySchema(BaseInventorySchema):
    pass


class InventoryFiltersSchema(BaseModel):
    film_id: int | None = Field(None, gt=0)
    store_id: int | None = Field(None, gt=0)


class InventoryResponseSchema(BaseInventorySchema):
    id: int
    created_at: datetime
    updated_at: datetime
