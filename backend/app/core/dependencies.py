"""FastAPI dependencies for authentication, authorization, and database access."""

from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db, set_tenant_schema
from app.core.security import verify_token, TokenPayload
from app.core.tenancy import get_current_tenant
from app.core.config import settings

# HTTP Bearer token security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user_token(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
) -> TokenPayload:
    """Validate JWT token and return payload."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_payload = verify_token(credentials.credentials, token_type="access")
    if token_payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_payload


async def get_optional_user_token(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
) -> Optional[TokenPayload]:
    """Get user token if present, otherwise None."""
    if credentials is None:
        return None

    return verify_token(credentials.credentials, token_type="access")


async def get_tenant_db(
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
) -> AsyncSession:
    """Get database session with tenant schema set."""
    tenant_id = getattr(request.state, "tenant_id", None) or get_current_tenant()
    if tenant_id:
        await set_tenant_schema(db, tenant_id)
    return db


def require_roles(*required_roles: str):
    """Dependency factory to require specific roles."""

    async def role_checker(
        token: Annotated[TokenPayload, Depends(get_current_user_token)],
    ) -> TokenPayload:
        user_roles = set(token.roles)
        required = set(required_roles)

        # Admin role has access to everything
        if "admin" in user_roles:
            return token

        if not required.intersection(user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {', '.join(required_roles)}",
            )
        return token

    return role_checker


def require_permissions(*required_permissions: str):
    """Dependency factory to require specific permissions."""

    async def permission_checker(
        token: Annotated[TokenPayload, Depends(get_current_user_token)],
    ) -> TokenPayload:
        # For now, check if user has admin role (full access)
        # TODO: Implement proper permission checking from database
        if "admin" in token.roles:
            return token

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Required permissions: {', '.join(required_permissions)}",
        )

    return permission_checker


# Type aliases for cleaner dependency injection
CurrentUser = Annotated[TokenPayload, Depends(get_current_user_token)]
OptionalUser = Annotated[Optional[TokenPayload], Depends(get_optional_user_token)]
TenantDB = Annotated[AsyncSession, Depends(get_tenant_db)]
DB = Annotated[AsyncSession, Depends(get_db)]
