# src/feature/users/infrastructure/database/repositories.py - LIMPIO
from typing import Optional
from uuid import UUID
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from src.core.domain.value_objects.email import Email
from src.core.infrastructure.database.repositories import DjangoBaseRepository
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.infrastructure.database.models import UserModel
from src.feature.users.infrastructure.database.mappers.user_mapper import UserEntityMapper


class DjangoUserRepository(DjangoBaseRepository[User], UserRepository):
    """
    User-specific repository - SOLO operaciones específicas de User

    Responsabilidades:
    - Queries específicas de User (find_by_email, etc.)
    - Operaciones de password con Django
    - Delegar conversiones al UserEntityMapper

    NO responsabilidades:
    - Conversión de datos (delegado a UserEntityMapper)
    - Operaciones CRUD genéricas (heredado de DjangoBaseRepository)
    """

    def __init__(self):
        mapper = UserEntityMapper()
        super().__init__(UserModel, mapper)

    # ===== USER-SPECIFIC QUERIES =====
    async def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email - specific to User domain"""
        try:
            model = await sync_to_async(UserModel.objects.get)(email=str(email))
            return self.mapper.model_to_entity(model)
        except ObjectDoesNotExist:
            return None

    async def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email - specific to User domain"""
        return await sync_to_async(UserModel.objects.filter(email=str(email)).exists)()

    # ===== PASSWORD OPERATIONS (Django-specific) =====
    async def save_with_password(self, entity: User, plain_password: str) -> User:
        """Save user with password hashing - specific to User domain"""
        data = self.mapper.entity_to_model_data(entity)

        model, created = await sync_to_async(self.model_class.objects.update_or_create)(id=entity.id, defaults=data)

        model.set_password(plain_password)
        await sync_to_async(model.save)()

        return self.mapper.model_to_entity(model)

    async def verify_password(self, user_id: UUID, plain_password: str) -> bool:
        """Verify password - specific to User domain"""
        try:
            model = await sync_to_async(UserModel.objects.get)(id=user_id)
            return model.check_password(plain_password)
        except ObjectDoesNotExist:
            return False

    async def change_password(self, user_id: UUID, new_plain_password: str) -> bool:
        """Change password - specific to User domain"""
        try:
            model = await sync_to_async(UserModel.objects.get)(id=user_id)
            model.set_password(new_plain_password)
            await sync_to_async(model.save)()
            return True
        except ObjectDoesNotExist:
            return False

