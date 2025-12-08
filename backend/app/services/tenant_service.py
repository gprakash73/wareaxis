"""Tenant service - business logic for tenant management."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.tenant import Tenant, TenantSettings
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantSettingsUpdate
from app.core.config import settings


class TenantService:
    """Service for tenant operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tenant_id: UUID) -> Optional[Tenant]:
        """Get tenant by ID."""
        result = await self.db.execute(
            select(Tenant)
            .options(selectinload(Tenant.settings))
            .where(Tenant.id == tenant_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Tenant]:
        """Get tenant by slug."""
        result = await self.db.execute(
            select(Tenant)
            .options(selectinload(Tenant.settings))
            .where(Tenant.slug == slug)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: Optional[bool] = None,
    ) -> tuple[List[Tenant], int]:
        """List tenants with pagination."""
        query = select(Tenant).options(selectinload(Tenant.settings))

        if is_active is not None:
            query = query.where(Tenant.is_active == is_active)

        # Get total count
        count_query = select(func.count()).select_from(Tenant)
        if is_active is not None:
            count_query = count_query.where(Tenant.is_active == is_active)
        total = await self.db.scalar(count_query)

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(Tenant.created_at.desc())
        result = await self.db.execute(query)
        tenants = list(result.scalars().all())

        return tenants, total or 0

    async def create(self, data: TenantCreate) -> Tenant:
        """Create a new tenant."""
        schema_name = f"{settings.TENANT_SCHEMA_PREFIX}{data.slug}"

        tenant = Tenant(
            name=data.name,
            slug=data.slug,
            description=data.description,
            contact_email=data.contact_email,
            contact_phone=data.contact_phone,
            address_line1=data.address_line1,
            address_line2=data.address_line2,
            city=data.city,
            state=data.state,
            country=data.country,
            postal_code=data.postal_code,
            timezone=data.timezone,
            currency=data.currency,
            locale=data.locale,
            schema_name=schema_name,
            schema_created=False,
        )

        self.db.add(tenant)
        await self.db.flush()

        # Create tenant settings
        tenant_settings = TenantSettings(tenant_id=tenant.id)
        self.db.add(tenant_settings)

        await self.db.commit()
        await self.db.refresh(tenant)

        return tenant

    async def update(self, tenant_id: UUID, data: TenantUpdate) -> Optional[Tenant]:
        """Update a tenant."""
        tenant = await self.get_by_id(tenant_id)
        if not tenant:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tenant, field, value)

        await self.db.commit()
        await self.db.refresh(tenant)

        return tenant

    async def delete(self, tenant_id: UUID) -> bool:
        """Delete a tenant (soft delete by deactivating)."""
        tenant = await self.get_by_id(tenant_id)
        if not tenant:
            return False

        tenant.is_active = False
        await self.db.commit()

        return True

    async def create_schema(self, tenant: Tenant) -> bool:
        """Create the tenant's database schema."""
        try:
            # Create schema
            await self.db.execute(
                text(f"CREATE SCHEMA IF NOT EXISTS {tenant.schema_name}")
            )

            # Set search path to new schema
            await self.db.execute(
                text(f"SET search_path TO {tenant.schema_name}")
            )

            # Create tables in tenant schema
            # This would typically run the tenant-specific migrations
            # For now, we'll create the basic tables

            # Create users table
            await self.db.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    email VARCHAR(255) UNIQUE NOT NULL,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    display_name VARCHAR(200),
                    phone VARCHAR(50),
                    avatar_url VARCHAR(500),
                    is_active BOOLEAN DEFAULT TRUE NOT NULL,
                    is_verified BOOLEAN DEFAULT FALSE NOT NULL,
                    is_superuser BOOLEAN DEFAULT FALSE NOT NULL,
                    is_deleted BOOLEAN DEFAULT FALSE NOT NULL,
                    deleted_at TIMESTAMPTZ,
                    deleted_by VARCHAR(36),
                    last_login TIMESTAMPTZ,
                    failed_login_attempts INTEGER DEFAULT 0 NOT NULL,
                    locked_until TIMESTAMPTZ,
                    sso_provider VARCHAR(50),
                    sso_id VARCHAR(255),
                    default_warehouse_id UUID,
                    employee_id VARCHAR(50),
                    department VARCHAR(100),
                    job_title VARCHAR(100),
                    preferences JSONB DEFAULT '{}'::jsonb NOT NULL,
                    metadata JSONB DEFAULT '{}'::jsonb NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
                    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
                )
            """))

            # Create roles table
            await self.db.execute(text("""
                CREATE TABLE IF NOT EXISTS roles (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    code VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    is_system BOOLEAN DEFAULT FALSE NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
                    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
                )
            """))

            # Create permissions table
            await self.db.execute(text("""
                CREATE TABLE IF NOT EXISTS permissions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    code VARCHAR(100) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    module VARCHAR(50) NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
                    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
                )
            """))

            # Create role_permissions table
            await self.db.execute(text("""
                CREATE TABLE IF NOT EXISTS role_permissions (
                    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
                    permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
                    PRIMARY KEY (role_id, permission_id)
                )
            """))

            # Create user_roles table
            await self.db.execute(text("""
                CREATE TABLE IF NOT EXISTS user_roles (
                    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
                    assigned_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
                    assigned_by UUID,
                    PRIMARY KEY (user_id, role_id)
                )
            """))

            # Create default admin role
            await self.db.execute(text("""
                INSERT INTO roles (code, name, description, is_system)
                VALUES ('admin', 'Administrator', 'Full system access', TRUE)
                ON CONFLICT (code) DO NOTHING
            """))

            # Create default user role
            await self.db.execute(text("""
                INSERT INTO roles (code, name, description, is_system)
                VALUES ('user', 'User', 'Standard user access', TRUE)
                ON CONFLICT (code) DO NOTHING
            """))

            # Reset search path
            await self.db.execute(text("SET search_path TO public"))

            # Mark schema as created
            tenant.schema_created = True
            await self.db.commit()

            return True
        except Exception as e:
            await self.db.rollback()
            raise e

    async def update_settings(
        self, tenant_id: UUID, data: TenantSettingsUpdate
    ) -> Optional[TenantSettings]:
        """Update tenant settings."""
        result = await self.db.execute(
            select(TenantSettings).where(TenantSettings.tenant_id == tenant_id)
        )
        settings = result.scalar_one_or_none()

        if not settings:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(settings, field, value)

        await self.db.commit()
        await self.db.refresh(settings)

        return settings
