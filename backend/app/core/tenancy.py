"""Multi-tenancy middleware and utilities."""

from typing import Optional
from contextvars import ContextVar

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.core.security import decode_token

# Context variable to store current tenant
current_tenant_id: ContextVar[Optional[str]] = ContextVar("current_tenant_id", default=None)


def get_current_tenant() -> Optional[str]:
    """Get the current tenant ID from context."""
    return current_tenant_id.get()


def set_current_tenant(tenant_id: Optional[str]) -> None:
    """Set the current tenant ID in context."""
    current_tenant_id.set(tenant_id)


class TenantMiddleware(BaseHTTPMiddleware):
    """Middleware to extract and set tenant context from requests."""

    # Paths that don't require tenant context
    PUBLIC_PATHS = [
        "/",
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        f"{settings.API_V1_PREFIX}/auth/login",
        f"{settings.API_V1_PREFIX}/auth/register",
        f"{settings.API_V1_PREFIX}/auth/refresh",
        f"{settings.API_V1_PREFIX}/tenants/register",
    ]

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Skip tenant extraction for public paths
        if self._is_public_path(request.url.path):
            return await call_next(request)

        # Try to extract tenant from various sources
        tenant_id = await self._extract_tenant(request)

        if tenant_id:
            set_current_tenant(tenant_id)
            # Store tenant_id in request state for easy access
            request.state.tenant_id = tenant_id
        else:
            # For protected paths, tenant is required
            if not self._is_public_path(request.url.path):
                set_current_tenant(None)
                request.state.tenant_id = None

        response = await call_next(request)

        # Clear tenant context after request
        set_current_tenant(None)

        return response

    def _is_public_path(self, path: str) -> bool:
        """Check if path is public (doesn't require tenant)."""
        for public_path in self.PUBLIC_PATHS:
            if path.startswith(public_path) or path == public_path:
                return True
        return False

    async def _extract_tenant(self, request: Request) -> Optional[str]:
        """Extract tenant ID from request (JWT, header, or subdomain)."""
        # 1. Try to get from JWT token
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = decode_token(token)
            if payload and payload.tenant_id:
                return payload.tenant_id

        # 2. Try to get from X-Tenant-ID header (for API clients)
        tenant_header = request.headers.get("X-Tenant-ID")
        if tenant_header:
            return tenant_header

        # 3. Try to get from subdomain (e.g., tenant1.wms.example.com)
        host = request.headers.get("Host", "")
        if "." in host:
            subdomain = host.split(".")[0]
            if subdomain and subdomain not in ["www", "api", "app"]:
                return subdomain

        return None


async def set_tenant_search_path(session: AsyncSession, tenant_id: str) -> None:
    """Set PostgreSQL search_path to tenant's schema."""
    schema_name = f"{settings.TENANT_SCHEMA_PREFIX}{tenant_id}"
    await session.execute(
        text(f"SET search_path TO {schema_name}, public")
    )


async def get_tenant_session(
    session: AsyncSession, tenant_id: Optional[str] = None
) -> AsyncSession:
    """Get a session configured for the tenant's schema."""
    tid = tenant_id or get_current_tenant()
    if tid:
        await set_tenant_search_path(session, tid)
    return session


def require_tenant(request: Request) -> str:
    """Dependency to require and return tenant ID."""
    tenant_id = getattr(request.state, "tenant_id", None) or get_current_tenant()
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant ID is required",
        )
    return tenant_id
