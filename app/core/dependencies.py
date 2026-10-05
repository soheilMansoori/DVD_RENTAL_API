from typing import Annotated

from fastapi import Depends
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
