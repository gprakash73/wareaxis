"""Pydantic schemas for request/response validation."""

from app.schemas.common import PaginationParams, PaginatedResponse, Message
from app.schemas.tenant import (
    TenantCreate,
    TenantUpdate,
    TenantResponse,
    TenantSettingsUpdate,
    TenantSettingsResponse,
)
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    RoleCreate,
    RoleResponse,
    PermissionResponse,
)
from app.schemas.auth import (
    TokenResponse,
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordChangeRequest,
)

__all__ = [
    "PaginationParams",
    "PaginatedResponse",
    "Message",
    "TenantCreate",
    "TenantUpdate",
    "TenantResponse",
    "TenantSettingsUpdate",
    "TenantSettingsResponse",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "RoleCreate",
    "RoleResponse",
    "PermissionResponse",
    "TokenResponse",
    "LoginRequest",
    "RegisterRequest",
    "RefreshTokenRequest",
    "PasswordResetRequest",
    "PasswordChangeRequest",
]
