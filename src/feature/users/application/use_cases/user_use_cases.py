# src/feature/users/application/use_cases/user_use_cases.py
from typing import List, Optional, Tuple
from uuid import UUID

from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from src.core.domain.value_objects.email import Email  # ✅ CORRECTO: Email está en core
from ...domain.value_objects.user_status import UserStatus
from src.core.exceptions.base_exceptions import ValidationException, NotFoundError  # ✅ CORRECTO: Exceptions están en core


class UserUseCases:
    """
    Application Layer - Use Cases

    RESPONSABILIDADES:
    - Coordinar el flujo de la aplicación
    - Validaciones de negocio
    - Orquestar domain entities y services
    - NO conocer detalles de infrastructure
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    # ===== COMMANDS (Write Operations) =====
    async def create_user(self, email: str, password: str, first_name: str, last_name: str, email_verified: bool = False) -> User:
        """Use Case: Create new user with business validations"""

        # 1. Input validations
        if not email or not password:
            raise ValidationException("Email and password are required")

        if not first_name or not last_name:
            raise ValidationException("First name and last name are required")

        # 2. Business rules validation
        email_vo = Email(email)  # This validates email format

        if await self.user_repository.exists_by_email(email_vo):
            raise ValidationException(f"User with email {email} already exists")

        # 3. Create domain entity (business logic)
        user = User(
            email=email_vo,
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            status=UserStatus.PENDING_VERIFICATION if not email_verified else UserStatus.ACTIVE,
            email_verified=email_verified,
        )

        # 4. Persist via repository interface
        return await self.user_repository.save_with_password(user, password)

    async def update_user(self, user_id: UUID, first_name: Optional[str] = None, last_name: Optional[str] = None) -> User:
        """Use Case: Update existing user"""

        # 1. Find user
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")

        # 2. Apply business logic (Domain method)
        user.update_profile(first_name=first_name, last_name=last_name)

        # 3. Persist changes
        return await self.user_repository.save(user)

    async def delete_user(self, user_id: UUID) -> bool:
        """Use Case: Delete user"""

        # 1. Check existence first
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")

        # 2. Business rule: could add additional checks here
        # Example: if user has active subscriptions, prevent deletion

        # 3. Delete
        return await self.user_repository.delete_by_id(user_id)

    # ===== QUERIES (Read Operations) =====
    async def find_user_by_id(self, user_id: UUID) -> User:
        """Use Case: Find user by ID"""
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        return user

    async def find_user_by_email(self, email: str) -> User:
        """Use Case: Find user by email"""
        email_vo = Email(email)  # Validates email format
        user = await self.user_repository.find_by_email(email_vo)
        if not user:
            raise NotFoundError(f"User with email {email} not found")
        return user

    async def find_users_with_criteria(self, criteria: List) -> Tuple[List[User], int]:
        """Use Case: Find users with filtering and pagination"""
        users = await self.user_repository.find_by_criteria(criteria)
        total_count = await self.user_repository.count_by_criteria(criteria)
        return users, total_count

    async def check_user_exists_by_email(self, email: str) -> bool:
        """Use Case: Check if user exists by email"""
        email_vo = Email(email)
        return await self.user_repository.exists_by_email(email_vo)

