"""Async database configuration with SQLAlchemy 2.0."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy import text

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """Context manager for database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def set_tenant_schema(session: AsyncSession, tenant_id: str) -> None:
    """Set the search_path to tenant's schema."""
    schema_name = f"{settings.TENANT_SCHEMA_PREFIX}{tenant_id}"
    await session.execute(text(f"SET search_path TO {schema_name}, public"))


async def reset_schema(session: AsyncSession) -> None:
    """Reset search_path to public schema."""
    await session.execute(text("SET search_path TO public"))


async def create_tenant_schema(session: AsyncSession, tenant_id: str) -> None:
    """Create a new schema for a tenant."""
    schema_name = f"{settings.TENANT_SCHEMA_PREFIX}{tenant_id}"
    await session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
    await session.commit()


async def drop_tenant_schema(session: AsyncSession, tenant_id: str) -> None:
    """Drop a tenant's schema (use with caution)."""
    schema_name = f"{settings.TENANT_SCHEMA_PREFIX}{tenant_id}"
    await session.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE"))
    await session.commit()


async def init_db() -> None:
    """Initialize database - create all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()
