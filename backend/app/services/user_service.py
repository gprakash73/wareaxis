"""User service - business logic for user management."""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User, Role, Permission, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class UserService:
    """Service for user operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(and_(User.id == user_id, User.is_deleted == False))
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(and_(User.email == email, User.is_deleted == False))
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(and_(User.username == username, User.is_deleted == False))
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: Optional[bool] = None,
        role_code: Optional[str] = None,
    ) -> tuple[List[User], int]:
        """List users with pagination."""
        query = (
            select(User)
            .options(selectinload(User.roles))
            .where(User.is_deleted == False)
        )

        if is_active is not None:
            query = query.where(User.is_active == is_active)

        if role_code:
            query = query.join(User.roles).where(Role.code == role_code)

        # Get total count
        count_query = select(func.count()).select_from(User).where(User.is_deleted == False)
        if is_active is not None:
            count_query = count_query.where(User.is_active == is_active)
        total = await self.db.scalar(count_query)

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
        result = await self.db.execute(query)
        users = list(result.scalars().unique().all())

        return users, total or 0

    async def create(self, data: UserCreate) -> User:
        """Create a new user."""
        user = User(
            email=data.email,
            username=data.username,
            password_hash=get_password_hash(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            display_name=data.display_name,
            phone=data.phone,
            default_warehouse_id=data.default_warehouse_id,
            employee_id=data.employee_id,
            department=data.department,
            job_title=data.job_title,
        )

        self.db.add(user)
        await self.db.flush()

        # Assign roles
        if data.role_ids:
            for role_id in data.role_ids:
                user_role = UserRole(user_id=user.id, role_id=role_id)
                self.db.add(user_role)

        await self.db.commit()
        await self.db.refresh(user)

        # Reload with roles
        return await self.get_by_id(user.id)

    async def create_admin_user(
        self,
        email: str,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
    ) -> User:
        """Create an admin user for a new tenant."""
        # Get admin role
        result = await self.db.execute(
            select(Role).where(Role.code == "admin")
        )
        admin_role = result.scalar_one_or_none()

        user = User(
            email=email,
            username=username,
            password_hash=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            is_superuser=True,
            is_verified=True,
        )

        self.db.add(user)
        await self.db.flush()

        # Assign admin role
        if admin_role:
            user_role = UserRole(user_id=user.id, role_id=admin_role.id)
            self.db.add(user_role)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update(self, user_id: UUID, data: UserUpdate) -> Optional[User]:
        """Update a user."""
        user = await self.get_by_id(user_id)
        if not user:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude={"role_ids"})
        for field, value in update_data.items():
            setattr(user, field, value)

        # Update roles if provided
        if data.role_ids is not None:
            # Remove existing roles
            await self.db.execute(
                UserRole.__table__.delete().where(UserRole.user_id == user_id)
            )
            # Add new roles
            for role_id in data.role_ids:
                user_role = UserRole(user_id=user.id, role_id=role_id)
                self.db.add(user_role)

        await self.db.commit()

        # Reload with roles
        return await self.get_by_id(user.id)

    async def delete(self, user_id: UUID, deleted_by: Optional[str] = None) -> bool:
        """Soft delete a user."""
        user = await self.get_by_id(user_id)
        if not user:
            return False

        user.soft_delete(deleted_by)
        await self.db.commit()

        return True

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username/email and password."""
        # Try to find by username first, then by email
        user = await self.get_by_username(username)
        if not user:
            user = await self.get_by_email(username)

        if not user:
            return None

        if not user.is_active:
            return None

        # Check if account is locked
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            return None

        if not verify_password(password, user.password_hash):
            # Increment failed login attempts
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                # Lock account for 30 minutes
                user.locked_until = datetime.now(timezone.utc).replace(
                    minute=datetime.now(timezone.utc).minute + 30
                )
            await self.db.commit()
            return None

        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.now(timezone.utc)
        await self.db.commit()

        return user

    async def change_password(
        self, user_id: UUID, current_password: str, new_password: str
    ) -> bool:
        """Change user's password."""
        user = await self.get_by_id(user_id)
        if not user:
            return False

        if not verify_password(current_password, user.password_hash):
            return False

        user.password_hash = get_password_hash(new_password)
        await self.db.commit()

        return True

    async def reset_password(self, user_id: UUID, new_password: str) -> bool:
        """Reset user's password (admin action)."""
        user = await self.get_by_id(user_id)
        if not user:
            return False

        user.password_hash = get_password_hash(new_password)
        user.failed_login_attempts = 0
        user.locked_until = None
        await self.db.commit()

        return True


class RoleService:
    """Service for role operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, role_id: UUID) -> Optional[Role]:
        """Get role by ID."""
        result = await self.db.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.id == role_id)
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Optional[Role]:
        """Get role by code."""
        result = await self.db.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.code == code)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> tuple[List[Role], int]:
        """List all roles."""
        count = await self.db.scalar(select(func.count()).select_from(Role))

        result = await self.db.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .offset(skip)
            .limit(limit)
            .order_by(Role.name)
        )
        roles = list(result.scalars().all())

        return roles, count or 0

    async def list_permissions(self) -> List[Permission]:
        """List all permissions."""
        result = await self.db.execute(
            select(Permission).order_by(Permission.module, Permission.name)
        )
        return list(result.scalars().all())
