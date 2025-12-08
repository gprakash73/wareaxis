"""Tenant management API routes."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import CurrentUser, require_roles
from app.schemas.tenant import (
    TenantCreate,
    TenantUpdate,
    TenantResponse,
    TenantSettingsUpdate,
    TenantSettingsResponse,
)
from app.schemas.common import PaginatedResponse, Message
from app.services.tenant_service import TenantService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[TenantResponse])
async def list_tenants(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(require_roles("superadmin")),
):
    """
    List all tenants (superadmin only).

    This is a platform-level operation for managing tenants.
    """
    tenant_service = TenantService(db)
    tenants, total = await tenant_service.list(
        skip=(page - 1) * page_size,
        limit=page_size,
        is_active=is_active,
    )

    return PaginatedResponse.create(
        items=[TenantResponse.model_validate(t) for t in tenants],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/current", response_model=TenantResponse)
async def get_current_tenant(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Get current tenant details."""
    tenant_service = TenantService(db)
    tenant = await tenant_service.get_by_slug(current_user.tenant_id)

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    return TenantResponse.model_validate(tenant)


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(require_roles("superadmin")),
):
    """Get tenant by ID (superadmin only)."""
    tenant_service = TenantService(db)
    tenant = await tenant_service.get_by_id(tenant_id)

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    return TenantResponse.model_validate(tenant)


@router.post("", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    data: TenantCreate,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(require_roles("superadmin")),
):
    """Create a new tenant (superadmin only)."""
    tenant_service = TenantService(db)

    # Check if slug already exists
    existing = await tenant_service.get_by_slug(data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant with this slug already exists",
        )

    try:
        tenant = await tenant_service.create(data)
        await tenant_service.create_schema(tenant)
        return TenantResponse.model_validate(tenant)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create tenant: {str(e)}",
        )


@router.patch("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: UUID,
    data: TenantUpdate,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(require_roles("superadmin")),
):
    """Update tenant details (superadmin only)."""
    tenant_service = TenantService(db)
    tenant = await tenant_service.update(tenant_id, data)

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    return TenantResponse.model_validate(tenant)


@router.patch("/current/settings", response_model=TenantSettingsResponse)
async def update_current_tenant_settings(
    data: TenantSettingsUpdate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Update current tenant's settings (admin only)."""
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    tenant_service = TenantService(db)
    tenant = await tenant_service.get_by_slug(current_user.tenant_id)

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    settings = await tenant_service.update_settings(tenant.id, data)

    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant settings not found",
        )

    return TenantSettingsResponse.model_validate(settings)


@router.delete("/{tenant_id}", response_model=Message)
async def delete_tenant(
    tenant_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(require_roles("superadmin")),
):
    """
    Deactivate a tenant (superadmin only).

    This soft-deletes the tenant by marking it as inactive.
    The schema and data are preserved.
    """
    tenant_service = TenantService(db)
    success = await tenant_service.delete(tenant_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    return Message(message="Tenant deactivated successfully")
