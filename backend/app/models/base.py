"""Base model classes and mixins."""

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declared_attr, DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all models."""

    # Enable JSONB type for PostgreSQL
    type_annotation_map = {
        dict[str, Any]: JSONB,
    }


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class UUIDMixin:
    """Mixin to add UUID primary key."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )


class TenantMixin:
    """Mixin for tenant-scoped models (used in tenant schemas)."""

    @declared_attr
    def __table_args__(cls):
        return {"schema": None}  # Schema set dynamically


class AuditMixin(TimestampMixin):
    """Mixin for audit fields."""

    created_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String(36), nullable=True)


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_by: Mapped[str | None] = mapped_column(String(36), nullable=True)

    def soft_delete(self, user_id: str | None = None) -> None:
        """Mark the record as deleted."""
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)
        self.deleted_by = user_id
