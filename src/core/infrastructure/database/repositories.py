# ===== 1. FIXED CORE REPOSITORY (src/core/infrastructure/database/repositories.py) =====
from typing import Type, Optional, List, Dict, Any, TypeVar
from uuid import UUID
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.repositories.base_repository import BaseRepository
from src.core.infrastructure.database.mappers.base_mapper import BaseEntityMapper

T = TypeVar("T", bound=BaseEntity)


class DjangoBaseRepository(BaseRepository[T]):
    def __init__(self, model_class: Type[models.Model], mapper: BaseEntityMapper[T, models.Model]):
        self.model_class = model_class
        self.mapper = mapper

    # ===== CORE OPERATIONS =====
    async def save(self, entity: T) -> T:
        """Save entity using mapper"""
        data = self.mapper.entity_to_model_data(entity)
        model, _ = await sync_to_async(self.model_class.objects.update_or_create)(id=entity.id, defaults=data)
        return self.mapper.model_to_entity(model)

    async def find_by_id(self, entity_id: UUID) -> Optional[T]:
        """Find entity by ID"""
        try:
            model = await sync_to_async(self.model_class.objects.get)(id=entity_id)
            return self.mapper.model_to_entity(model)
        except ObjectDoesNotExist:
            return None

    async def delete(self, entity_id: UUID) -> bool:
        """Delete entity by ID"""
        try:
            deleted_count, _ = await sync_to_async(self.model_class.objects.filter(id=entity_id).delete)()
            return deleted_count > 0
        except Exception:
            return False

    async def exists_by_id(self, entity_id: UUID) -> bool:
        """Check if entity exists by ID"""
        return await sync_to_async(self.model_class.objects.filter(id=entity_id).exists)()

    # ===== NEW METHODS FOR GENERIC CRITERIA =====
    async def find_with_criteria(self, criteria) -> List[T]:
        """Find entities using generic Criteria"""
        from src.shared.criteria.converter import CriteriaConverter

        queryset = self.model_class.objects.all()

        # Apply criteria using generic converter
        filtered_queryset = CriteriaConverter.apply_criteria(queryset, criteria)

        # Execute query
        models = await sync_to_async(list)(filtered_queryset)
        return self.mapper.models_to_entities(models)

    async def find_one_with_criteria(self, criteria) -> Optional[T]:
        """Find one entity using generic Criteria"""
        from src.shared.criteria.converter import CriteriaConverter
        from src.shared.criteria.base_criteria import Criteria

        queryset = self.model_class.objects.all()

        # Apply criteria (without pagination for findOne)
        criteria_no_pagination = Criteria(
            filters=criteria.filters,
            orders=criteria.orders,
            projection=criteria.projection,
            options=criteria.options,
            # No limit/offset
        )

        filtered_queryset = CriteriaConverter.apply_criteria(queryset, criteria_no_pagination)

        try:
            model = await sync_to_async(filtered_queryset.first)()
            return self.mapper.model_to_entity(model) if model else None
        except ObjectDoesNotExist:
            return None

    async def count_with_criteria(self, criteria) -> int:
        """Count entities using generic Criteria"""
        from src.shared.criteria.converter import CriteriaConverter
        from src.shared.criteria.base_criteria import Criteria

        queryset = self.model_class.objects.all()

        # Apply only filters and orders (no pagination/projection for count)
        count_criteria = Criteria(filters=criteria.filters, orders=criteria.orders, options=criteria.options)

        filtered_queryset = CriteriaConverter.apply_criteria(queryset, count_criteria)
        return await sync_to_async(filtered_queryset.count)()
