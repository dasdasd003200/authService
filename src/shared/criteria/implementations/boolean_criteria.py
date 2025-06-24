# src/core/domain/repositories/criteria/boolean_criteria.py
from django.db.models import QuerySet
from ..base_criteria import BaseCriteria


class BooleanCriteria(BaseCriteria):
    """Generic criteria for boolean field filtering"""

    def __init__(self, field_name: str, value: bool):
        self.field_name = field_name
        self.value = value

    def apply(self, queryset: QuerySet) -> QuerySet:
        return queryset.filter(**{self.field_name: self.value})

    def to_dict(self) -> dict:
        return {
            "type": "boolean",
            "field_name": self.field_name,
            "value": self.value,
        }
