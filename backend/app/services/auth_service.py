"""Authentication service."""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from app.models.tenant import Tenant
from app.models.user import User
from app.services.tenant_service import TenantService
from app.services.user_service import UserService
from app.schemas.tenant import TenantRegistration
from app.schemas.auth import TokenResponse
from app.core.security import create_token_pair, verify_token
from app.core.config import settings


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.tenant_service = TenantService(db)
        self.user_service = UserService(db)

    async def login(
        self, username: str, password: str, tenant_slug: Optional[str] = None
    ) -> Optional[tuple[TokenResponse, User, Tenant]]:
        """
        Authenticate user and return tokens.

        If tenant_slug is provided, validates user belongs to that tenant.
        Returns None if authentication fails.
        """
        # Get tenant
        if not tenant_slug:
            return None

        tenant = await self.tenant_service.get_by_slug(tenant_slug)
        if not tenant or not tenant.is_active:
            return None

        # Set search path to tenant schema
        await self.db.execute(
            text(f"SET search_path TO {tenant.schema_name}, public")
        )

        # Authenticate user
        user = await self.user_service.authenticate(username, password)
        if not user:
            return None

        # Create tokens
        token_pair = create_token_pair(
            user_id=str(user.id),
            tenant_id=tenant_slug,
            roles=user.role_codes,
        )

        token_response = TokenResponse(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
            token_type=token_pair.token_type,
            expires_in=token_pair.expires_in,
        )

        return token_response, user, tenant

    async def refresh_token(self, refresh_token: str) -> Optional[TokenResponse]:
        """Refresh access token using refresh token."""
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            return None

        # Get tenant
        tenant = await self.tenant_service.get_by_slug(payload.tenant_id)
        if not tenant or not tenant.is_active:
            return None

        # Set search path to tenant schema
        await self.db.execute(
            text(f"SET search_path TO {tenant.schema_name}, public")
        )

        # Get user
        user = await self.user_service.get_by_id(UUID(payload.sub))
        if not user or not user.is_active:
            return None

        # Create new tokens
        token_pair = create_token_pair(
            user_id=str(user.id),
            tenant_id=payload.tenant_id,
            roles=user.role_codes,
        )

        return TokenResponse(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
            token_type=token_pair.token_type,
            expires_in=token_pair.expires_in,
        )

    async def register_tenant(
        self, data: TenantRegistration
    ) -> tuple[Tenant, User, TokenResponse]:
        """
        Register a new tenant with admin user.

        Creates tenant, tenant schema, and admin user.
        Returns tenant, admin user, and auth tokens.
        """
        from app.schemas.tenant import TenantCreate

        # Create tenant
        tenant_data = TenantCreate(
            name=data.tenant_name,
            slug=data.tenant_slug,
            contact_email=data.contact_email,
        )
        tenant = await self.tenant_service.create(tenant_data)

        # Create tenant schema and tables
        await self.tenant_service.create_schema(tenant)

        # Set search path to tenant schema
        await self.db.execute(
            text(f"SET search_path TO {tenant.schema_name}, public")
        )

        # Create admin user
        user = await self.user_service.create_admin_user(
            email=data.admin_email,
            username=data.admin_username,
            password=data.admin_password,
            first_name=data.admin_first_name,
            last_name=data.admin_last_name,
        )

        # Create tokens
        token_pair = create_token_pair(
            user_id=str(user.id),
            tenant_id=tenant.slug,
            roles=user.role_codes,
        )

        token_response = TokenResponse(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
            token_type=token_pair.token_type,
            expires_in=token_pair.expires_in,
        )

        return tenant, user, token_response
