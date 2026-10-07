from fastapi import status
from fastapi.exceptions import HTTPException


class PermissionDeniedException(HTTPException):
    def __init__(self, detail: str = "permission denied") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "unauthorized") -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "not found") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
