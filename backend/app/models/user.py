"""User, Role, and Permission models - stored in tenant schemas."""

import uuid
from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import String, Boolean, Text, ForeignKey, Table, Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin, SoftDeleteMixin


class Permission(Base, UUIDMixin, TimestampMixin):
    """Permission model - defines granular access rights."""

    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    module: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # e.g., inventory, inbound, outbound
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    roles: Mapped[List["Role"]] = relationship(
        "Role", secondary="role_permissions", back_populates="permissions"
    )

    def __repr__(self) -> str:
        return f"<Permission {self.code}>"


class Role(Base, UUIDMixin, TimestampMixin):
    """Role model - groups permissions for assignment to users."""

    __tablename__ = "roles"

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)  # System roles can't be deleted
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    permissions: Mapped[List["Permission"]] = relationship(
        "Permission", secondary="role_permissions", back_populates="roles"
    )
    users: Mapped[List["User"]] = relationship(
        "User", secondary="user_roles", back_populates="roles"
    )

    def __repr__(self) -> str:
        return f"<Role {self.code}>"


class RolePermission(Base):
    """Association table for Role-Permission many-to-many relationship."""

    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )


class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """User model - warehouse system users."""

    __tablename__ = "users"

    # Authentication
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Profile
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Authentication tracking
    last_login: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    failed_login_attempts: Mapped[int] = mapped_column(default=0, nullable=False)
    locked_until: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # SSO
    sso_provider: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # keycloak, azure_ad, google
    sso_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Warehouse assignment
    default_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    # Worker profile
    employee_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    job_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Preferences & metadata
    preferences: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSONB, default=dict, nullable=False
    )

    # Relationships
    roles: Mapped[List["Role"]] = relationship(
        "Role", secondary="user_roles", back_populates="users"
    )

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def role_codes(self) -> List[str]:
        """Get list of role codes."""
        return [role.code for role in self.roles]

    def has_role(self, role_code: str) -> bool:
        """Check if user has a specific role."""
        return role_code in self.role_codes

    def has_permission(self, permission_code: str) -> bool:
        """Check if user has a specific permission through their roles."""
        for role in self.roles:
            for permission in role.permissions:
                if permission.code == permission_code:
                    return True
        return False

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class UserRole(Base):
    """Association table for User-Role many-to-many relationship."""

    __tablename__ = "user_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    assigned_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(),
        nullable=False,
    )
    assigned_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
