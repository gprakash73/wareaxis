"""Common schemas used across the application."""

from typing import Any, Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.config import settings

T = TypeVar("T")


class Message(BaseModel):
    """Simple message response."""

    message: str


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(
        default=settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Items per page",
    )

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""

    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def create(
        cls, items: List[T], total: int, page: int, page_size: int
    ) -> "PaginatedResponse[T]":
        pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
        )


class IDResponse(BaseModel):
    """Response containing just an ID."""

    id: UUID


class BulkDeleteRequest(BaseModel):
    """Request for bulk delete operation."""

    ids: List[UUID] = Field(..., min_length=1, max_length=100)


class BulkDeleteResponse(BaseModel):
    """Response for bulk delete operation."""

    deleted: int
    failed: List[UUID] = []


class ErrorDetail(BaseModel):
    """Error detail for validation errors."""

    loc: List[str]
    msg: str
    type: str


class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str
    errors: Optional[List[ErrorDetail]] = None
