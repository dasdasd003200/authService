# ===== MODIFICAR: src/feature/users/infrastructure/database/repositories.py =====
from typing import Optional, List  # ✅ Agregar List aquí
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
    def __init__(self):
        mapper = UserEntityMapper()
        super().__init__(UserModel, mapper)

    # ===== USER-SPECIFIC QUERIES =====
    async def find_by_email(self, email: Email) -> Optional[User]:
        try:
            model = await sync_to_async(UserModel.objects.get)(email=str(email))
            return self.mapper.model_to_entity(model)
        except ObjectDoesNotExist:
            return None

    async def exists_by_email(self, email: Email) -> bool:
        return await sync_to_async(UserModel.objects.filter(email=str(email)).exists)()

    # ===== PASSWORD OPERATIONS (Django-specific) =====
    async def save_with_password(self, entity: User, plain_password: str) -> User:
        data = self.mapper.entity_to_model_data(entity)

        model, _ = await sync_to_async(self.model_class.objects.update_or_create)(  # ✅ Usar _ en lugar de created
            id=entity.id, defaults=data
        )

        model.set_password(plain_password)
        await sync_to_async(model.save)()

        return self.mapper.model_to_entity(model)

    # ===== NEW METHODS FOR CLEAN ARCHITECTURE =====
    async def find_by_criteria(self, criteria: List) -> List[User]:  # ✅ List ya importado
        """Find users by criteria - adapter for new architecture"""
        return await super().find_by_criteria(criteria)

    async def count_by_criteria(self, criteria: List) -> int:  # ✅ List ya importado
        """Count users by criteria - adapter for new architecture"""
        return await super().count_by_criteria(criteria)

    async def delete_by_id(self, user_id: UUID) -> bool:
        """Delete user by ID - adapter for new architecture"""
        return await super().delete_by_id(user_id)
