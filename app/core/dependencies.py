from typing import Annotated

from fastapi import Depends, Query
from fastapi.security import HTTPAuthorizationCredentials

from .database import SessionLocal
from .security import security


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    pass


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class Pagination:
    def __init__(
        self,
        page: Annotated[int, Query(ge=1)] = 1,
        size: Annotated[int, Query(ge=1, le=20)] = 10,
    ) -> None:
        self.page = page
        self.size = size
