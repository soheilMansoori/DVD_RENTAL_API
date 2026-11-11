from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel, computed_field

T = TypeVar("T")


class PaginatedResponseSchema(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int

    @computed_field
    @property
    def total_pages(self) -> int:
        return ceil(self.total / self.size) if self.size > 0 else 0
