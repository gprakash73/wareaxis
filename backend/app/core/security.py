"""Security utilities - JWT, password hashing, and authentication."""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: str  # user_id
    tenant_id: str
    exp: datetime
    type: str = "access"
    roles: list[str] = []


class TokenPair(BaseModel):
    """Access and refresh token pair."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(
    user_id: str,
    tenant_id: str,
    roles: list[str] = [],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create an access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "roles": roles,
        "exp": expire,
        "type": "access",
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    user_id: str,
    tenant_id: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a refresh token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

    to_encode = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "exp": expire,
        "type": "refresh",
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_token_pair(
    user_id: str,
    tenant_id: str,
    roles: list[str] = [],
) -> TokenPair:
    """Create both access and refresh tokens."""
    access_token = create_access_token(user_id, tenant_id, roles)
    refresh_token = create_refresh_token(user_id, tenant_id)

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


def decode_token(token: str) -> Optional[TokenPayload]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return TokenPayload(
            sub=payload.get("sub"),
            tenant_id=payload.get("tenant_id"),
            exp=datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc),
            type=payload.get("type", "access"),
            roles=payload.get("roles", []),
        )
    except JWTError:
        return None


def verify_token(token: str, token_type: str = "access") -> Optional[TokenPayload]:
    """Verify a token and check its type."""
    payload = decode_token(token)
    if payload is None:
        return None
    if payload.type != token_type:
        return None
    if payload.exp < datetime.now(timezone.utc):
        return None
    return payload
