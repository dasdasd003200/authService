from typing import Optional, Any
from django.db.models import QuerySet
from ..base_criteria import BaseCriteria


class RangeCriteria(BaseCriteria):
    def __init__(
        self,
        field_name: str,
        min_value: Optional[Any] = None,
        max_value: Optional[Any] = None,
    ):
        self.field_name = field_name
        self.min_value = min_value
        self.max_value = max_value

    def apply(self, queryset: QuerySet) -> QuerySet:
        filters = {}

        if self.min_value is not None:
            filters[f"{self.field_name}__gte"] = self.min_value

        if self.max_value is not None:
            filters[f"{self.field_name}__lte"] = self.max_value

        return queryset.filter(**filters) if filters else queryset

    def to_dict(self) -> dict:
        return {
            "type": "range",
            "field": self.field_name,
            "min_value": self.min_value,
            "max_value": self.max_value,
        }
