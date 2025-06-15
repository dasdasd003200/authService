from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from django.db.models import QuerySet


class BaseCriteria(ABC):
    """Criterio base para búsquedas"""

    @abstractmethod
    def apply(self, queryset: QuerySet) -> QuerySet:
        """Aplicar criterio al queryset"""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serializar criterio para caching/debugging"""
        pass


class CriteriaBuilder:
    """Builder para combinar múltiples criterios"""

    def __init__(self):
        self._criteria: List[BaseCriteria] = []

    def add(self, criteria: BaseCriteria) -> "CriteriaBuilder":
        self._criteria.append(criteria)
        return self

    def build(self) -> List[BaseCriteria]:
        return self._criteria.copy()

    def apply_all(self, queryset: QuerySet) -> QuerySet:
        for criteria in self._criteria:
            queryset = criteria.apply(queryset)
        return queryset
