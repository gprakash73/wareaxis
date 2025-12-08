"""Tenant models - stored in public schema."""

import uuid
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Tenant(Base, UUIDMixin, TimestampMixin):
    """Tenant (organization) model - stored in public schema."""

    __tablename__ = "tenants"
    __table_args__ = {"schema": "public"}

    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Contact
    contact_email: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Address
    address_line1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Regional settings
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    locale: Mapped[str] = mapped_column(String(10), default="en-US", nullable=False)

    # Schema info
    schema_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    schema_created: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Metadata
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSONB, default=dict, nullable=False
    )

    # Relationships
    settings: Mapped["TenantSettings"] = relationship(
        "TenantSettings", back_populates="tenant", uselist=False, lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<Tenant {self.slug}>"


class TenantSettings(Base, UUIDMixin, TimestampMixin):
    """Tenant-specific settings - stored in public schema."""

    __tablename__ = "tenant_settings"
    __table_args__ = {"schema": "public"}

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.tenants.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # Feature flags
    features: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    # Integration settings
    erp_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # sap_ecc, sap_s4, oracle, dynamics
    erp_config: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    # Inventory settings
    allow_negative_stock: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    default_stock_type: Mapped[str] = mapped_column(String(20), default="unrestricted", nullable=False)

    # UI settings
    ui_theme: Mapped[str] = mapped_column(String(20), default="light", nullable=False)
    ui_config: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    # Custom fields schema
    custom_fields: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    # Relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="settings")

    def __repr__(self) -> str:
        return f"<TenantSettings tenant_id={self.tenant_id}>"
