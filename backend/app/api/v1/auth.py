"""Authentication API routes."""

from fastapi import APIRouter, HTTPException, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import CurrentUser, get_current_user_token
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    PasswordChangeRequest,
)
from app.schemas.tenant import TenantRegistration, TenantResponse
from app.schemas.user import UserResponse
from app.schemas.common import Message
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.core.tenancy import get_current_tenant

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate user and return access tokens.

    Requires tenant_slug in request body or via subdomain/header.
    """
    auth_service = AuthService(db)
    result = await auth_service.login(
        username=request.username,
        password=request.password,
        tenant_slug=request.tenant_slug,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or tenant",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_response, user, tenant = result
    return token_response


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token using refresh token."""
    auth_service = AuthService(db)
    result = await auth_service.refresh_token(request.refresh_token)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result


@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
async def register_tenant(
    request: TenantRegistration,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new tenant with admin user.

    Creates:
    - New tenant organization
    - Tenant database schema
    - Admin user account
    - Returns authentication tokens
    """
    auth_service = AuthService(db)

    try:
        tenant, user, tokens = await auth_service.register_tenant(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create tenant: {str(e)}",
        )

    return {
        "tenant": TenantResponse.model_validate(tenant),
        "user": UserResponse.model_validate(user),
        "tokens": tokens,
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: CurrentUser,
    http_request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Get current authenticated user."""
    from sqlalchemy import text

    tenant_id = current_user.tenant_id
    if tenant_id:
        from app.core.config import settings
        schema_name = f"{settings.TENANT_SCHEMA_PREFIX}{tenant_id}"
        await db.execute(text(f"SET search_path TO {schema_name}, public"))

    user_service = UserService(db)
    user = await user_service.get_by_id(current_user.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.post("/change-password", response_model=Message)
async def change_password(
    request: PasswordChangeRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Change current user's password."""
    from sqlalchemy import text
    from uuid import UUID

    tenant_id = current_user.tenant_id
    if tenant_id:
        from app.core.config import settings
        schema_name = f"{settings.TENANT_SCHEMA_PREFIX}{tenant_id}"
        await db.execute(text(f"SET search_path TO {schema_name}, public"))

    user_service = UserService(db)
    success = await user_service.change_password(
        user_id=UUID(current_user.sub),
        current_password=request.current_password,
        new_password=request.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid current password",
        )

    return Message(message="Password changed successfully")


@router.post("/logout", response_model=Message)
async def logout(current_user: CurrentUser):
    """
    Logout current user.

    Note: JWT tokens are stateless. This endpoint is for client-side cleanup.
    For full logout, implement token blacklisting with Redis.
    """
    # TODO: Implement token blacklisting if needed
    return Message(message="Logged out successfully")
