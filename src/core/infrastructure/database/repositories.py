# src/core/infrastructure/database/repositories.py - IMPLEMENTACIÓN COMPLETA
from typing import Type, Optional, List, Dict, Any, TypeVar
from uuid import UUID
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async

from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.repositories.base_repository import BaseRepository
from src.shared.criteria.base_criteria import BaseCriteria
from src.core.infrastructure.database.mappers.base_mapper import BaseEntityMapper

T = TypeVar("T", bound=BaseEntity)


class DjangoBaseRepository(BaseRepository[T]):
    """Django implementation - TODAS las operaciones CRUD"""

    def __init__(self, model_class: Type[models.Model], mapper: BaseEntityMapper[T, models.Model]):
        self.model_class = model_class
        self.mapper = mapper

    # ===== CREATE OPERATIONS =====
    async def save(self, entity: T) -> T:
        """Save entity using mapper"""
        data = self.mapper.entity_to_model_data(entity)
        model, _ = await sync_to_async(self.model_class.objects.update_or_create)(id=entity.id, defaults=data)
        return self.mapper.model_to_entity(model)

    async def save_many(self, entities: List[T]) -> List[T]:
        """Bulk save multiple entities"""
        saved_models = []
        for entity in entities:
            data = self.mapper.entity_to_model_data(entity)
            model, _ = await sync_to_async(self.model_class.objects.update_or_create)(id=entity.id, defaults=data)
            saved_models.append(model)
        return self.mapper.models_to_entities(saved_models)

    # ===== READ OPERATIONS =====
    async def find_by_id(self, entity_id: UUID) -> Optional[T]:
        """Find entity by ID"""
        try:
            model = await sync_to_async(self.model_class.objects.get)(id=entity_id)
            return self.mapper.model_to_entity(model)
        except ObjectDoesNotExist:
            return None

    async def find_by_criteria(self, criteria: List[BaseCriteria]) -> List[T]:
        """Find entities by criteria"""
        queryset = self.model_class.objects.all()
        for criterion in criteria:
            queryset = criterion.apply(queryset)
        models = await sync_to_async(list)(queryset)
        return self.mapper.models_to_entities(models)

    async def find_first(self, criteria: List[BaseCriteria]) -> Optional[T]:
        """Find first entity matching criteria"""
        queryset = self.model_class.objects.all()
        for criterion in criteria:
            queryset = criterion.apply(queryset)
        try:
            model = await sync_to_async(queryset.first)()
            return self.mapper.model_to_entity(model) if model else None
        except ObjectDoesNotExist:
            return None

    async def find_all(self) -> List[T]:
        """Find all entities"""
        models = await sync_to_async(list)(self.model_class.objects.all())
        return self.mapper.models_to_entities(models)

    # ===== UPDATE OPERATIONS =====
    async def update_by_id(self, entity_id: UUID, updates: Dict[str, Any]) -> Optional[T]:
        """Update specific fields by ID"""
        try:
            await sync_to_async(self.model_class.objects.filter(id=entity_id).update)(**updates)
            model = await sync_to_async(self.model_class.objects.get)(id=entity_id)
            return self.mapper.model_to_entity(model)
        except ObjectDoesNotExist:
            return None

    async def update_many(self, entity_ids: List[UUID], updates: Dict[str, Any]) -> int:
        """Bulk update multiple entities"""
        return await sync_to_async(self.model_class.objects.filter(id__in=entity_ids).update)(**updates)

    # ===== DELETE OPERATIONS =====
    async def delete_by_id(self, entity_id: UUID) -> bool:
        """Delete entity by ID"""
        try:
            deleted_count, _ = await sync_to_async(self.model_class.objects.filter(id=entity_id).delete)()
            return deleted_count > 0
        except Exception:
            return False

    async def delete_many(self, entity_ids: List[UUID]) -> int:
        """Bulk delete multiple entities"""
        try:
            deleted_count, _ = await sync_to_async(self.model_class.objects.filter(id__in=entity_ids).delete)()
            return deleted_count
        except Exception:
            return 0

    async def delete_by_criteria(self, criteria: List[BaseCriteria]) -> int:
        """Delete entities by criteria"""
        try:
            queryset = self.model_class.objects.all()
            for criterion in criteria:
                queryset = criterion.apply(queryset)
            deleted_count, _ = await sync_to_async(queryset.delete)()
            return deleted_count
        except Exception:
            return 0

    # ===== QUERY OPERATIONS =====
    async def count_by_criteria(self, criteria: List[BaseCriteria]) -> int:
        """Count entities by criteria"""
        queryset = self.model_class.objects.all()
        for criterion in criteria:
            queryset = criterion.apply(queryset)
        return await sync_to_async(queryset.count)()

    async def exists_by_id(self, entity_id: UUID) -> bool:
        """Check if entity exists by ID"""
        return await sync_to_async(self.model_class.objects.filter(id=entity_id).exists)()

    async def exists_by_criteria(self, criteria: List[BaseCriteria]) -> bool:
        """Check if any entity exists matching criteria"""
        queryset = self.model_class.objects.all()
        for criterion in criteria:
            queryset = criterion.apply(queryset)
        return await sync_to_async(queryset.exists)()

    # ===== LEGACY COMPATIBILITY =====
    async def delete(self, entity_id: UUID) -> bool:
        """Legacy delete method - delegates to delete_by_id"""
        return await self.delete_by_id(entity_id)
