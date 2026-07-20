from datetime import datetime, timedelta, UTC
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.exceptions import UnauthorizedException
from app.core.config import settings
from app.schemas.auth import TokenPayload


def create_access_token(subject: str) -> str:
    payload = {
        "sub": subject,
        "type": "access",
        "exp": datetime.now(UTC)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def create_refresh_token(subject: str) -> str:
    payload = {
        "sub": subject,
        "type": "refresh",
        "exp": datetime.now(UTC)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        return TokenPayload.model_validate(payload)

    except (ExpiredSignatureError, InvalidTokenError):
        raise UnauthorizedException()