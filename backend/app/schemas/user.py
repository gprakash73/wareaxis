"""User, Role, and Permission schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class PermissionResponse(BaseModel):
    """Schema for permission response."""

    id: UUID
    code: str
    name: str
    description: Optional[str]
    module: str
    is_active: bool

    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    """Base role schema."""

    code: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Schema for creating a role."""

    permission_ids: List[UUID] = []

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not re.match(r"^[a-z][a-z0-9_]*$", v):
            raise ValueError(
                "Code must be lowercase, start with a letter, "
                "and contain only letters, numbers, and underscores"
            )
        return v


class RoleUpdate(BaseModel):
    """Schema for updating a role."""

    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    permission_ids: Optional[List[UUID]] = None


class RoleResponse(RoleBase):
    """Schema for role response."""

    id: UUID
    is_system: bool
    is_active: bool
    permissions: List[PermissionResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoleBrief(BaseModel):
    """Brief role info for user response."""

    id: UUID
    code: str
    name: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    display_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=8, max_length=100)
    role_ids: List[UUID] = []
    default_warehouse_id: Optional[UUID] = None
    employee_id: Optional[str] = None
    department: Optional[str] = None
    job_title: Optional[str] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    display_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    role_ids: Optional[List[UUID]] = None
    default_warehouse_id: Optional[UUID] = None
    employee_id: Optional[str] = None
    department: Optional[str] = None
    job_title: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class UserResponse(BaseModel):
    """Schema for user response."""

    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    full_name: str
    display_name: Optional[str]
    phone: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    is_verified: bool
    is_superuser: bool
    last_login: Optional[datetime]
    default_warehouse_id: Optional[UUID]
    employee_id: Optional[str]
    department: Optional[str]
    job_title: Optional[str]
    roles: List[RoleBrief] = []
    preferences: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""

    username: str
    password: str


class UserProfile(BaseModel):
    """Schema for user profile (self)."""

    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    full_name: str
    display_name: Optional[str]
    phone: Optional[str]
    avatar_url: Optional[str]
    roles: List[RoleBrief] = []
    preferences: Dict[str, Any] = {}

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    """Schema for updating own profile."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    display_name: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
