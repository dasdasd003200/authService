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
    def __init__(self):
        mapper = UserEntityMapper()
        super().__init__(UserModel, mapper)

    async def find_by_email(self, email: Email) -> Optional[User]:
        try:
            model = await sync_to_async(UserModel.objects.get)(email=str(email))
            return self.mapper.model_to_entity(model)
        except ObjectDoesNotExist:
            return None

    async def exists_by_email(self, email: Email) -> bool:
        return await sync_to_async(UserModel.objects.filter(email=str(email)).exists)()

    async def save_with_password(self, entity: User, plain_password: str) -> User:
        data = self.mapper.entity_to_model_data(entity)
        model, _ = await sync_to_async(self.model_class.objects.update_or_create)(id=entity.id, defaults=data)
        model.set_password(plain_password)
        await sync_to_async(model.save)()
        return self.mapper.model_to_entity(model)

    async def delete_by_id(self, user_id: UUID) -> bool:
        return await super().delete(user_id)
