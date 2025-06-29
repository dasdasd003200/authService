from typing import Optional, List
from uuid import UUID
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from src.core.infrastructure.database.repositories import DjangoBaseRepository
from src.feature.sessions.domain.entities.session import Session
from src.feature.sessions.domain.repositories.session_repository import SessionRepository
from src.feature.sessions.domain.value_objects.token_type import TokenType
from src.feature.sessions.domain.value_objects.session_status import SessionStatus
from src.feature.sessions.infrastructure.database.models import SessionModel
from src.feature.sessions.infrastructure.database.mappers.session_mapper import SessionEntityMapper


class DjangoSessionRepository(DjangoBaseRepository[Session], SessionRepository):
    def __init__(self):
        mapper = SessionEntityMapper()
        super().__init__(SessionModel, mapper)

    async def save(self, entity: Session) -> Session:
        data = self.mapper.entity_to_model_data(entity)

        try:
            model = await sync_to_async(SessionModel.objects.get)(id=entity.id)
            for key, value in data.items():
                setattr(model, key, value)
            await sync_to_async(model.save)()
        except ObjectDoesNotExist:
            data["user_id"] = entity.user_id
            model = await sync_to_async(SessionModel.objects.create)(**data)

        return self.mapper.model_to_entity(model)

    async def find_by_user_id(self, user_id: UUID) -> List[Session]:
        models = await sync_to_async(list)(SessionModel.objects.filter(user_id=user_id).order_by("-created_at"))
        return self.mapper.models_to_entities(models)

    async def find_active_sessions_by_user_id(self, user_id: UUID) -> List[Session]:
        now = timezone.now()
        models = await sync_to_async(list)(SessionModel.objects.filter(user_id=user_id, status=SessionModel.StatusChoices.ACTIVE, expires_at__gt=now).order_by("-created_at"))
        return self.mapper.models_to_entities(models)

    async def find_by_user_and_token_type(self, user_id: UUID, token_type: TokenType) -> List[Session]:
        models = await sync_to_async(list)(SessionModel.objects.filter(user_id=user_id, token_type=token_type.value).order_by("-created_at"))
        return self.mapper.models_to_entities(models)

    async def revoke_all_user_sessions(self, user_id: UUID) -> int:
        updated_count = await sync_to_async(SessionModel.objects.filter(user_id=user_id, status=SessionModel.StatusChoices.ACTIVE).update)(status=SessionModel.StatusChoices.REVOKED, updated_at=timezone.now())

        return updated_count

    async def revoke_user_sessions_by_type(self, user_id: UUID, token_type: TokenType) -> int:
        updated_count = await sync_to_async(SessionModel.objects.filter(user_id=user_id, token_type=token_type.value, status=SessionModel.StatusChoices.ACTIVE).update)(status=SessionModel.StatusChoices.REVOKED, updated_at=timezone.now())

        return updated_count

    async def cleanup_expired_sessions(self) -> int:
        now = timezone.now()
        deleted_count, _ = await sync_to_async(SessionModel.objects.filter(expires_at__lt=now).delete)()

        return deleted_count

    async def count_active_sessions_by_user(self, user_id: UUID) -> int:
        now = timezone.now()
        count = await sync_to_async(SessionModel.objects.filter(user_id=user_id, status=SessionModel.StatusChoices.ACTIVE, expires_at__gt=now).count)()

        return count
