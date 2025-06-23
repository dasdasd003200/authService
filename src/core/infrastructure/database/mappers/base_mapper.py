# src/core/infrastructure/database/mappers/base_mapper.py - CORREGIDO
from abc import ABC, abstractmethod
from typing import Dict, Any, TypeVar, List, Generic  # ← AGREGAR Generic
from django.db import models

from src.core.domain.entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)
M = TypeVar("M", bound=models.Model)


class BaseEntityMapper(ABC, Generic[T, M]):  # ← Ahora Generic está disponible
    """
    Base mapper interface - SOLO conversión de datos

    Responsabilidad ÚNICA: transformar datos entre capas
    """

    @abstractmethod
    def model_to_entity(self, model: M) -> T:
        """Convert Django model to domain entity"""
        pass

    @abstractmethod
    def entity_to_model_data(self, entity: T) -> Dict[str, Any]:
        """Convert domain entity to Django model data dict"""
        pass

    def models_to_entities(self, models: List[M]) -> List[T]:
        """Convert list of models to entities"""
        return [self.model_to_entity(model) for model in models]

    def entities_to_model_data_list(self, entities: List[T]) -> List[Dict[str, Any]]:
        """Convert list of entities to model data dicts"""
        return [self.entity_to_model_data(entity) for entity in entities]
