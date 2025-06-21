from typing import List, Any
from django.db.models import QuerySet
from .base_criteria import BaseCriteria


class InCriteria(BaseCriteria):
    """Criteria for 'field IN values' filtering"""

    def __init__(self, field_name: str, values: List[Any]):
        self.field_name = field_name
        self.values = values

    def apply(self, queryset: QuerySet) -> QuerySet:
        if not self.values:
            return queryset
        return queryset.filter(**{f"{self.field_name}__in": self.values})

    def to_dict(self) -> dict:
        return {
            "type": "in",
            "field_name": self.field_name,
            "values": self.values,
        }
