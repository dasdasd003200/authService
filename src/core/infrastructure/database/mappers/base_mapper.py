from abc import ABC, abstractmethod
from typing import Dict, Any, TypeVar, List, Generic
from django.db import models

from src.core.domain.entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)
M = TypeVar("M", bound=models.Model)


class BaseEntityMapper(ABC, Generic[T, M]):
    @abstractmethod
    def model_to_entity(self, model: M) -> T:
        pass

    @abstractmethod
    def entity_to_model_data(self, entity: T) -> Dict[str, Any]:
        pass

    def models_to_entities(self, models: List[M]) -> List[T]:
        return [self.model_to_entity(model) for model in models]

    def entities_to_model_data_list(self, entities: List[T]) -> List[Dict[str, Any]]:
        return [self.entity_to_model_data(entity) for entity in entities]
