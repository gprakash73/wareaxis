"""User management API routes."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_db
from app.core.config import settings
from app.core.dependencies import CurrentUser, TenantDB, require_roles
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserProfileUpdate,
    RoleResponse,
    PermissionResponse,
)
from app.schemas.common import PaginatedResponse, Message
from app.services.user_service import UserService, RoleService

router = APIRouter()


async def get_tenant_db_session(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> AsyncSession:
    """Get database session with tenant schema."""
    if current_user.tenant_id:
        schema_name = f"{settings.TENANT_SCHEMA_PREFIX}{current_user.tenant_id}"
        await db.execute(text(f"SET search_path TO {schema_name}, public"))
    return db


@router.get("", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = None,
    role: Optional[str] = None,
    current_user: CurrentUser = Depends(),
    db: AsyncSession = Depends(get_tenant_db_session),
):
    """List users in current tenant."""
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    user_service = UserService(db)
    users, total = await user_service.list(
        skip=(page - 1) * page_size,
        limit=page_size,
        is_active=is_active,
        role_code=role,
    )

    return PaginatedResponse.create(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/roles", response_model=list[RoleResponse])
async def list_roles(
    current_user: CurrentUser = Depends(),
    db: AsyncSession = Depends(get_tenant_db_session),
):
    """List all roles in current tenant."""
    role_service = RoleService(db)
    roles, _ = await role_service.list()
    return [RoleResponse.model_validate(r) for r in roles]


@router.get("/permissions", response_model=list[PermissionResponse])
async def list_permissions(
    current_user: CurrentUser = Depends(),
    db: AsyncSession = Depends(get_tenant_db_session),
):
    """List all permissions."""
    role_service = RoleService(db)
    permissions = await role_service.list_permissions()
    return [PermissionResponse.model_validate(p) for p in permissions]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    current_user: CurrentUser = Depends(),
    db: AsyncSession = Depends(get_tenant_db_session),
):
    """Get user by ID."""
    # Users can view their own profile, admins can view anyone
    if str(user_id) != current_user.sub and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponse.model_validate(user)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    current_user: CurrentUser = Depends(),
    db: AsyncSession = Depends(get_tenant_db_session),
):
    """Create a new user (admin only)."""
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    user_service = UserService(db)

    # Check if email/username already exists
    existing = await user_service.get_by_email(data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    existing = await user_service.get_by_username(data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )

    user = await user_service.create(data)
    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    current_user: CurrentUser = Depends(),
    db: AsyncSession = Depends(get_tenant_db_session),
):
    """Update user (admin only, or self for limited fields)."""
    is_self = str(user_id) == current_user.sub
    is_admin = "admin" in current_user.roles

    if not is_self and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    # Non-admins can only update limited fields on their own profile
    if is_self and not is_admin:
        allowed_fields = {"first_name", "last_name", "display_name", "phone", "preferences"}
        update_data = data.model_dump(exclude_unset=True)
        for field in update_data:
            if field not in allowed_fields:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cannot update field: {field}",
                )

    user_service = UserService(db)
    user = await user_service.update(user_id, data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponse.model_validate(user)


@router.delete("/{user_id}", response_model=Message)
async def delete_user(
    user_id: UUID,
    current_user: CurrentUser = Depends(),
    db: AsyncSession = Depends(get_tenant_db_session),
):
    """Delete user (admin only)."""
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    # Prevent self-deletion
    if str(user_id) == current_user.sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )

    user_service = UserService(db)
    success = await user_service.delete(user_id, deleted_by=current_user.sub)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return Message(message="User deleted successfully")


@router.post("/{user_id}/reset-password", response_model=Message)
async def reset_user_password(
    user_id: UUID,
    new_password: str = Query(..., min_length=8),
    current_user: CurrentUser = Depends(),
    db: AsyncSession = Depends(get_tenant_db_session),
):
    """Reset user's password (admin only)."""
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    user_service = UserService(db)
    success = await user_service.reset_password(user_id, new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return Message(message="Password reset successfully")


@router.post("/{user_id}/activate", response_model=Message)
async def activate_user(
    user_id: UUID,
    current_user: CurrentUser = Depends(),
    db: AsyncSession = Depends(get_tenant_db_session),
):
    """Activate a user account (admin only)."""
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    user_service = UserService(db)
    user = await user_service.update(user_id, UserUpdate(is_active=True))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return Message(message="User activated successfully")


@router.post("/{user_id}/deactivate", response_model=Message)
async def deactivate_user(
    user_id: UUID,
    current_user: CurrentUser = Depends(),
    db: AsyncSession = Depends(get_tenant_db_session),
):
    """Deactivate a user account (admin only)."""
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    # Prevent self-deactivation
    if str(user_id) == current_user.sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account",
        )

    user_service = UserService(db)
    user = await user_service.update(user_id, UserUpdate(is_active=False))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return Message(message="User deactivated successfully")
