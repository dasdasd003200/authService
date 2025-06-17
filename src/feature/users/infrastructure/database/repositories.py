# src/feature/users/infrastructure/database/repositories.py
from typing import Optional, List
from uuid import UUID

from django.db.models import QuerySet
from asgiref.sync import sync_to_async

from src.core.domain.value_objects.email import Email
from src.core.domain.repositories.criteria.base_criteria import BaseCriteria
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.value_objects.password import Password
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.infrastructure.database.models import UserModel


class DjangoUserRepository(UserRepository):
    """Implementación del repositorio de usuarios con Django ORM"""

    def _model_to_entity(self, model: UserModel) -> User:
        """Convierte modelo Django a entidad de dominio"""
        return User(
            id=model.id,
            email=Email(model.email),
            password=Password.from_hash(model.password_hash, model.password_salt),
            first_name=model.first_name,
            last_name=model.last_name,
            status=UserStatus.from_string(model.status),
            email_verified=model.email_verified,
            last_login=model.last_login,
            failed_login_attempts=model.failed_login_attempts,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _entity_to_model_data(self, user: User) -> dict:
        """Convierte entidad de dominio a datos para modelo Django"""
        return {
            "id": user.id,
            "email": str(user.email),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "status": user.status.value,
            "email_verified": user.email_verified,
            "last_login": user.last_login,
            "failed_login_attempts": user.failed_login_attempts,
            "password_hash": user.password.hashed_value,
            "password_salt": user.password.salt,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    async def save(self, user: User) -> User:
        """Guarda o actualiza un usuario"""
        data = self._entity_to_model_data(user)

        model, created = await sync_to_async(UserModel.objects.update_or_create)(
            id=user.id, defaults=data
        )

        return self._model_to_entity(model)

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Busca usuario por ID"""
        try:
            model = await sync_to_async(UserModel.objects.get)(id=user_id)
            return self._model_to_entity(model)
        except UserModel.DoesNotExist:
            return None

    async def find_by_email(self, email: Email) -> Optional[User]:
        """Busca usuario por email"""
        try:
            model = await sync_to_async(UserModel.objects.get)(email=str(email))
            return self._model_to_entity(model)
        except UserModel.DoesNotExist:
            return None

    async def exists_by_email(self, email: Email) -> bool:
        """Verifica si existe un usuario con el email"""
        return await sync_to_async(UserModel.objects.filter(email=str(email)).exists)()

    async def find_by_criteria(self, criteria: List[BaseCriteria]) -> List[User]:
        """Busca usuarios por criterios"""
        queryset = UserModel.objects.all()

        # Aplicar criterios
        for criterion in criteria:
            queryset = criterion.apply(queryset)

        models = await sync_to_async(list)(queryset)
        return [self._model_to_entity(model) for model in models]

    async def delete(self, user_id: UUID) -> bool:
        """Elimina un usuario (soft delete)"""
        try:
            await sync_to_async(UserModel.objects.filter(id=user_id).update)(
                status=UserStatus.INACTIVE.value
            )
            return True
        except Exception:
            return False

    async def count_by_criteria(self, criteria: List[BaseCriteria]) -> int:
        """Cuenta usuarios por criterios"""
        queryset = UserModel.objects.all()

        # Aplicar criterios
        for criterion in criteria:
            queryset = criterion.apply(queryset)

        return await sync_to_async(queryset.count)()
