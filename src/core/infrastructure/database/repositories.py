# src/core/infrastructure/database/repositories.py
from abc import abstractmethod
from typing import Type, Optional, List, Dict, Any, cast, TypeVar
from uuid import UUID
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async

from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.repositories.base_repository import BaseRepository
from src.core.domain.repositories.criteria.base_criteria import BaseCriteria

T = TypeVar("T", bound=BaseEntity)


class DjangoBaseRepository(BaseRepository[T]):
    """Base Django ORM repository implementation"""

    def __init__(self, model_class: Type[models.Model]):
        self.model_class = model_class

    @abstractmethod
    def _model_to_entity(self, model: models.Model) -> T:
        """Convert Django model to domain entity - must be implemented by subclasses"""
        pass

    @abstractmethod
    def _entity_to_model_data(self, entity: T) -> Dict[str, Any]:
        """Convert domain entity to Django model data - must be implemented by subclasses"""
        pass

    async def save(self, entity: T) -> T:
        """Save or update an entity"""
        data = self._entity_to_model_data(entity)

        model, _ = await sync_to_async(self.model_class.objects.update_or_create)(
            id=entity.id, defaults=data
        )

        return self._model_to_entity(model)

    async def find_by_id(self, entity_id: UUID) -> Optional[T]:
        """Find entity by ID"""
        try:
            model = await sync_to_async(self.model_class.objects.get)(id=entity_id)
            return self._model_to_entity(model)
        except ObjectDoesNotExist:
            return None

    async def find_by_criteria(self, criteria: List[BaseCriteria]) -> List[T]:
        """Find entities by criteria"""
        queryset = self.model_class.objects.all()

        # Apply criteria
        for criterion in criteria:
            queryset = criterion.apply(queryset)

        models = await sync_to_async(list)(queryset)
        return [self._model_to_entity(model) for model in models]

    async def count_by_criteria(self, criteria: List[BaseCriteria]) -> int:
        """Count entities by criteria"""
        queryset = self.model_class.objects.all()

        # Apply criteria
        for criterion in criteria:
            queryset = criterion.apply(queryset)

        return await sync_to_async(queryset.count)()

    async def delete(self, entity_id: UUID) -> bool:
        """Delete an entity"""
        try:
            deleted_count, _ = await sync_to_async(
                self.model_class.objects.filter(id=entity_id).delete
            )()
            return deleted_count > 0
        except Exception:
            return False

    async def exists_by_id(self, entity_id: UUID) -> bool:
        """Check if entity exists by ID"""
        return await sync_to_async(
            self.model_class.objects.filter(id=entity_id).exists
        )()

