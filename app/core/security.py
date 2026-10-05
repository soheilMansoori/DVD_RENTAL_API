from fastapi.security import HTTPBearer

security = HTTPBearer()


def verify_access_token(access_token: str) -> int:
    pass


def verify_refresh_token(refresh_token: str) -> int:
    pass


def generate_access_token(user_id: int) -> str:
    pass


def generate_refresh_token(user_id: int) -> str:
    pass
