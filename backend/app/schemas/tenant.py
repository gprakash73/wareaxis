"""Tenant schemas."""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class TenantBase(BaseModel):
    """Base tenant schema."""

    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    contact_email: EmailStr
    contact_phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    timezone: str = "UTC"
    currency: str = "USD"
    locale: str = "en-US"


class TenantCreate(TenantBase):
    """Schema for creating a tenant."""

    slug: str = Field(..., min_length=2, max_length=100)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$", v):
            raise ValueError(
                "Slug must be lowercase, start and end with alphanumeric, "
                "and contain only letters, numbers, and hyphens"
            )
        return v


class TenantUpdate(BaseModel):
    """Schema for updating a tenant."""

    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    timezone: Optional[str] = None
    currency: Optional[str] = None
    locale: Optional[str] = None
    is_active: Optional[bool] = None


class TenantResponse(TenantBase):
    """Schema for tenant response."""

    id: UUID
    slug: str
    is_active: bool
    is_verified: bool
    schema_name: str
    schema_created: bool
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = {}

    class Config:
        from_attributes = True


class TenantSettingsBase(BaseModel):
    """Base tenant settings schema."""

    features: Dict[str, Any] = {}
    erp_type: Optional[str] = None
    erp_config: Dict[str, Any] = {}
    allow_negative_stock: bool = False
    default_stock_type: str = "unrestricted"
    ui_theme: str = "light"
    ui_config: Dict[str, Any] = {}
    custom_fields: Dict[str, Any] = {}


class TenantSettingsUpdate(BaseModel):
    """Schema for updating tenant settings."""

    features: Optional[Dict[str, Any]] = None
    erp_type: Optional[str] = None
    erp_config: Optional[Dict[str, Any]] = None
    allow_negative_stock: Optional[bool] = None
    default_stock_type: Optional[str] = None
    ui_theme: Optional[str] = None
    ui_config: Optional[Dict[str, Any]] = None
    custom_fields: Optional[Dict[str, Any]] = None


class TenantSettingsResponse(TenantSettingsBase):
    """Schema for tenant settings response."""

    id: UUID
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TenantRegistration(BaseModel):
    """Schema for tenant self-registration with admin user."""

    # Tenant info
    tenant_name: str = Field(..., min_length=2, max_length=255)
    tenant_slug: str = Field(..., min_length=2, max_length=100)
    contact_email: EmailStr

    # Admin user info
    admin_email: EmailStr
    admin_username: str = Field(..., min_length=3, max_length=100)
    admin_password: str = Field(..., min_length=8, max_length=100)
    admin_first_name: str = Field(..., min_length=1, max_length=100)
    admin_last_name: str = Field(..., min_length=1, max_length=100)

    @field_validator("tenant_slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$", v):
            raise ValueError(
                "Slug must be lowercase, start and end with alphanumeric, "
                "and contain only letters, numbers, and hyphens"
            )
        return v

    @field_validator("admin_username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v
