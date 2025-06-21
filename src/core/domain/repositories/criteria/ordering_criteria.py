# src/core/domain/repositories/criteria/ordering_criteria.py
from typing import List
from django.db.models import QuerySet
from .base_criteria import BaseCriteria


class OrderingCriteria(BaseCriteria):
    """Criteria for ordering results"""

    def __init__(self, order_by: List[str]):
        self.order_by = order_by

    def apply(self, queryset: QuerySet) -> QuerySet:
        return queryset.order_by(*self.order_by)

    def to_dict(self) -> dict:
        return {
            "type": "ordering",
            "order_by": self.order_by,
        }
